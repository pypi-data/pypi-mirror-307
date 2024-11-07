import mne 
import os
import numpy as np

from tqdm import tqdm
import matplotlib.pyplot as plt
from collections import defaultdict
from mne.preprocessing import compute_bridged_electrodes
from itertools import chain

from autoreject import Ransac 
from joblib import Parallel, delayed
from .savers import bridge_save, event_saver, plot_clusters
from .metrics import isolation_forest, check_volt_of_epochs 
from .scenarious import get_riti_seq, verificate_events, is_subsequence
from .montages import create_custom_montage, read_elc, align_head

def compute_bad_epochs(epochs, snr_matrix, roi_channels=None, threshold_ep=-22, threshold_ch=-30):
    n_trials, n_channels, n_times = epochs._data.shape
    ch_names = epochs.ch_names 
    #--------------SNR---------------#
    rej_dict = {}
    
    rej_dict['SNR_over_channels'] = np.where(np.mean(snr_matrix, axis=1) < threshold_ep)[0] # Нахождение индексов эпох, где средняя поканальная зашумлённость превышает порог
    rej_dict['SNR_channel'] = []
    for epoch_idx in range(n_trials):
        channel_names_above_threshold = [ch_names[ch] for ch in np.where(snr_matrix[epoch_idx] < threshold_ch)[0]] #Если децибел на канале превысил порог
        if channel_names_above_threshold:
            rej_dict['SNR_channel'].append((epoch_idx, channel_names_above_threshold)) # Добавляем канал и  эпоху в список для удаления

    #-------ISOLATION_FOREST---------#
    rej_dict['Isol_forest_all_chns'] = isolation_forest(epochs.copy(), mode='ep')
    if roi_channels:
        rej_dict['Isol_forest_tar_chns'] = isolation_forest(epochs.copy().pick(roi_channels), mode='ep')

    #------------VOLT----------------#
    volt_max=dict(eeg=130e-6)
    volt_min=dict(eeg=1e-6)
    rej_dict['Volt_max'] = check_volt_of_epochs(epochs, reject=volt_max, flat=None)
    rej_dict['Volt_flat'] = check_volt_of_epochs(epochs, reject=None, flat=volt_min)

    #--------------FINAL-------------#
    snr_all_channels_indices = set(rej_dict['SNR_over_channels'])
    snr_channel_indices = set(epoch for epoch, _ in rej_dict['SNR_channel'])
    volt_max_indices = set(rej_dict['Volt_max'])
    volt_min_indices = set(rej_dict['Volt_flat'])
    isol_forest_all_indices = set(rej_dict['Isol_forest_all_chns'])
    isol_forest_tar_indices = set(rej_dict['Isol_forest_tar_chns'])
    combined_indices = snr_all_channels_indices | snr_channel_indices | volt_max_indices | isol_forest_tar_indices | isol_forest_all_indices | volt_min_indices
    rej_dict['FINAL'] = sorted(list(combined_indices))
    rej_dict['Percentage_removed_trials'] = len(rej_dict['FINAL'])/epochs._data.shape[0]*100
    return rej_dict

def set_montage(raw, montage, elc_file, mode, threshold, verbose=False, interpolate=None, vis=None):
    '''
    Функция предназначенная для вложения в info данных о монтаже записи raw
    montage - тип стандартного монтажа который будет использоваться либо будет являться целевым в случае интерполяции
    elc_file - путь до индивидуального монтажа
    mode - тип центрирования монтажа, может быть mean и электрод
    threshold - линейное расстояние за которое не должен выходить электрод от наложения целевого в случае интерполирования
    interpolate - флаг для интерполяции
    vis - флаг для графического отрабражения итогового монтажа
    '''
    if montage=='waveguard64':
        montage = create_custom_montage(montage)
    elif montage == 'personal':
        ch_dict, nasion, lpa, rpa, hsp = read_elc(elc_file)
        if interpolate:
            ch_dict, nasion, lpa, rpa, hsp = align_head(ch_dict, nasion, np.array(lpa), np.array(rpa), np.array(hsp), standard='waveguard64', 
                                                    mode=mode, threshold=threshold)
        montage = mne.channels.make_dig_montage(ch_pos=ch_dict, nasion=nasion, lpa=lpa, rpa=rpa, hsp=hsp, coord_frame='head')
    else:
        montage = mne.channels.make_standard_montage(montage)
    
    channels_to_drop = list((set(raw.info['ch_names'])) - (set(raw.info['ch_names']) & set(montage.ch_names)))
    channels_to_drop = [x for x in channels_to_drop if x not in {'BIP1', 'EOG'}]
    if verbose:
        print(f'CHANNELS DROPPED: {channels_to_drop}')
    raw.drop_channels(channels_to_drop)
    raw.set_montage(montage, verbose=False)
    if vis:
        fig = montage.plot(show_names=True, kind='3d')
        for ax in fig.get_axes():
            if ax.name == '3d':
                ax.set_xlim([-0.1, 0.1])
                ax.set_ylim([-0.1, 0.1])
                ax.set_zlim([-0.1, 0.1])
    return raw

def detect_bad_channels(raw, method):
    bad_channels = []
    scores = []
    electrodesD = {}
    flat_chans, noisy_channels = get_flat_channels(raw)
    clusters, bridge_figs = search_bridge_cluster(raw, method='corr', threshold_bridge=0.98, threshold_cluster=0.95)
    bridged_electrodes = list(chain.from_iterable(clusters))
    
    if method == 'ransac':
        bad_channels, scores, noised_fig = DNC_ransac(raw)
    elif method == 'ed':
        bad_channels, scores, noised_fig = DNC_electrical_distance(raw)
    elif method == 'corr':
        bad_channels, scores, noised_fig = DNC_corr(raw)
    elif method in ['auto', 'SN_rate']:
        bad_channels, scores, noised_fig = DNC_SN_rate(raw)
    else:
        raise ValueError(f"Unknown method '{method}'. Please use 'ransac', 'neighbours', 'psd', 'ed', 'corr' or 'auto'")
    
    electrodesD['HighAmp'] = noisy_channels
    electrodesD['LowAmp'] = flat_chans
    electrodesD['Bridged'] = bridged_electrodes
    electrodesD['Noise_Rate'] = bad_channels
    return electrodesD, clusters, bridge_figs, noised_fig


def preprocessing_events(raw, scenarious='RiTi'):
    if scenarious == 'RiTi':
        seq_list = get_riti_seq()
        events, event_id = mne.events_from_annotations(raw, verbose=False)
        reverse_event_id = dict(zip(event_id.values(), event_id.keys()))
        new_events = verificate_events(raw, seq_list)
        filtered_seq = [reverse_event_id[new_events[j, 2]] for j in range(len(new_events))]
        subseq, match_idxs, tr = is_subsequence(filtered_seq, seq_list)
        repo_data = {
                    'Initial_Events': len(events),
                    'Filtered_Events': len(new_events),
                    'Expected_Events': len(seq_list),
                    'SubSeq_Flag': subseq, 
                    'Match_Indexes': match_idxs,
                    'Transitions': tr
                    }
        return new_events, reverse_event_id, repo_data
    else:
        print('Не готово!')
        return None
    

def get_flat_channels(raw):
    data = raw.get_data()
    channel_names = raw.ch_names
    threshold_min_amplitude = 3e-6
    threshold_max_amplitude = 300e-6
    threshold_length = 0.5
    empty_channels = [ch for idx, ch in enumerate(channel_names) if np.mean(np.abs(data[idx]) < threshold_min_amplitude) > threshold_length]
    empty_scores = [np.mean(np.abs(data[idx] - data[idx].mean(keepdims=True)) < threshold_min_amplitude) for idx, ch in enumerate(channel_names) if np.mean(np.abs(data[idx]) < threshold_min_amplitude) > threshold_length]
    noisy_channels = [ch for idx, ch in enumerate(channel_names) if np.mean(np.abs(data[idx]) > threshold_max_amplitude) > threshold_length]
    noisy_scores = [np.mean(np.abs(data[idx]) > threshold_max_amplitude) for idx, ch in enumerate(channel_names) if np.mean(np.abs(data[idx]) > threshold_max_amplitude) > threshold_length]
    return empty_channels, noisy_channels

def search_bridge_cluster(raw, method='corr', threshold_bridge=0.98, threshold_cluster=0.95):
    data = raw.get_data()
    adjacency_list = defaultdict(list)
    ch_names = raw.ch_names

    ch_name_to_idx = {ch: idx for idx, ch in enumerate(ch_names)}

    if method == 'corr':
        correlation_matrix = np.corrcoef(data)
        for i in range(len(raw.ch_names)):
            for j in range(i + 1, len(raw.ch_names)):  # проверяем только верхний треугольник
                if correlation_matrix[i, j] > threshold_bridge:
                    adjacency_list[raw.ch_names[i]].append(raw.ch_names[j])
                    adjacency_list[raw.ch_names[j]].append(raw.ch_names[i])
               
    elif method in ['auto', 'ed']:
        bridged_idx, _ = compute_bridged_electrodes(raw, verbose=False)
        for pair in bridged_idx:
            ch1, ch2 = pair
            adjacency_list[raw.ch_names[ch1]].append(raw.ch_names[ch2])
            adjacency_list[raw.ch_names[ch2]].append(raw.ch_names[ch1])

    def dfs(electrode, cluster, markers):
        idx_electrode = ch_name_to_idx[electrode]
        # Добавляем электрод в кластер только если он коррелирует со всеми электродами в кластере
        can_add = True
        for existing_electrode in cluster:
            idx_existing = ch_name_to_idx[existing_electrode]
            corr = correlation_matrix[idx_electrode, idx_existing]
            if corr < threshold_cluster:
                can_add = False
                break
        if can_add:
            cluster.append(electrode)
            markers.add(electrode)
            for neighbor in adjacency_list[electrode]:
                if neighbor not in markers:
                    dfs(neighbor, cluster, markers)
        
    # Поиск всех кластеров
    clusters = []
    markers = set()

    for electrode in raw.ch_names:
        if (electrode not in markers) and (electrode in adjacency_list):
            cluster = []
            dfs(electrode, cluster, markers)
            clusters.append(cluster)

    # Создаем маску для выделения мостиковых электродов
    is_bridged = [False] * len(ch_names)
    
    for cluster in clusters:
        for ch in cluster:
            if ch in ch_name_to_idx:
                idx = ch_name_to_idx[ch]
                is_bridged[idx] = True

    if method == 'corr':
        clusters_avg = []
        clusters_max = []
        clusters_min = []
        for idx, cluster in enumerate(clusters, 1):
            cluster_indices = [ch_name_to_idx[ch] for ch in cluster]
            # Извлекаем подматрицу корреляций для текущего кластера
            cluster_corr_matrix = correlation_matrix[np.ix_(cluster_indices, cluster_indices)]
            # Извлекаем значения корреляций из верхнего треугольника подматрицы
            triu_indices = np.triu_indices_from(cluster_corr_matrix, k=1)
            cluster_corr_values = cluster_corr_matrix[triu_indices]
            if len(cluster_corr_values) > 0:
                min_corr = np.min(cluster_corr_values)
                avg_corr = np.mean(cluster_corr_values)
                max_corr = np.max(cluster_corr_values)
            clusters_avg.append(avg_corr)
            clusters_max.append(max_corr)
            clusters_min.append(min_corr)

    # Получаем позиции электродов
    ch_pos = np.array([raw.info['chs'][i]['loc'][:2] for i in range(raw.info['nchan'])])
    upper_triangle_indices = np.triu_indices_from(correlation_matrix, k=1)
    correlation_values = correlation_matrix[upper_triangle_indices]

    
    figs = plot_clusters(clusters, clusters_avg, clusters_max, clusters_min,
                ch_names, ch_pos, correlation_values)

    return clusters, figs

def event_check(raw, mind_stimulus, proc_stimulus, saving_dir=None, vis=False):
    proc_count = 0
    mind_count = 0
    other_count = 0
    events, event_id = mne.events_from_annotations(raw, verbose=False)
    rev_event_id = dict(list(zip(event_id.values(), event_id.keys())))
    mind_counter = {stimulus: 0 for stimulus in mind_stimulus}
    proc_counter = {stimulus: 0 for stimulus in proc_stimulus}
    strange_list = set()
    for event in events:
        if rev_event_id[event[2]] in proc_counter.keys():
            for key in proc_counter.keys():
                if rev_event_id[event[2]] == key:
                    proc_counter[key]+=1
                    proc_count += 1
        elif rev_event_id[event[2]] in mind_counter.keys():
            for key in mind_counter.keys():
                if rev_event_id[event[2]] == key:
                    mind_counter[key]+=1
                    mind_count += 1
        else:
            strange_list.add(rev_event_id[event[2]])
            other_count += 1
    event_saver(proc_counter, mind_counter, saving_dir, vis)

def bridging_test(raw, saving_dir=None, vis=False):
    raw = raw.copy()
    bridged_idx, ed_matrix = compute_bridged_electrodes(raw, verbose=False)
    correlation_matrix = np.corrcoef(raw.get_data())
    bridge_save(raw, correlation_matrix, bridged_idx, ed_matrix, saving_dir, vis=vis)
    return bridged_idx

def find_adj_neighbors(raw, ch_name):
    """Функция для поиска соседей для заданного канала ch_name"""
    montage = raw.get_montage()
    adjacency, ch_names = mne.channels.find_ch_adjacency(raw.info, 'eeg')
    adjacency = adjacency.toarray()
    idx = raw.ch_names.index(ch_name)
    neighbors_idx = np.where(adjacency[idx])[0]
    neighbors = [ch_names[i] for i in neighbors_idx]
    return neighbors

def calculate_correlations(raw, duration=1, overlap=0.5):
    epochs = mne.make_fixed_length_epochs(raw, duration=duration, overlap=overlap)
    data = epochs.get_data()
    n_trials, n_channels, n_times = epochs.get_data().shape
    adjacency, ch_names = mne.channels.find_ch_adjacency(raw.info, 'eeg')
    adjacency = adjacency.toarray()
    neighbors_indices = [np.where(adjacency[i])[0] for i in range(n_channels)]
    correlations = np.zeros((n_trials, n_channels))  # Для хранения корреляций
    # Проходим по всем эпохам и каналам
    for i in range(n_trials):
        epoch_data = data[i]  # Данные для конкретной эпохи
        for j in range(n_channels):
            # Интерполируем данные канала по соседям
            neighbor_data = np.mean(epoch_data[neighbors_indices[j]], axis=0)
            channel_data = epoch_data[j]
            # Рассчитываем корреляцию между каналом и интерполированным сигналом
            corr = np.corrcoef(channel_data, neighbor_data)[0, 1]
            correlations[i, j] = corr  # Сохраняем результат
    return correlations


def DNC_SN_rate(raw, optimized=False):
    def compute_snr(signal, noise):
        snr = 10 * np.log10(np.mean(signal ** 2) / np.mean(noise ** 2))
        return snr
    def snr_db_to_probability(snr_db):
        snr_linear = 10 ** (snr_db / 10)
        probability = snr_linear / (1 + snr_linear)
        return probability
    def plot_topomap(probabilities, raw, high_prob, high_prob_channels):
        """Plot topomap of SNR probabilities."""
        montage = raw.get_montage()
        ch_pos_dict = montage.get_positions()['ch_pos']
        ch_pos = np.array([ch_pos_dict[ch_name][:2] for ch_name in raw.ch_names])
        fig, ax = plt.subplots()
        im, _ = mne.viz.plot_topomap(
            probabilities, ch_pos, axes=ax, show=False,
            names=raw.ch_names, cmap='viridis', vlim=(0.5, 1)
        )
        ax.set_title('SNR Probability Topomap')
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('SNR Probability Coefficient')
        noisy_text = "Noisy Electrodes:\n" + "\n".join(
            [f"{ch_name}: {prob:.2f}" for ch_name, prob in zip(high_prob_channels, high_prob)]
        )
        fig.text(1.1, 0.5, noisy_text, va='center', ha='left', fontsize=10)
        return fig
    
    ch_names = raw.ch_names
    original_data = raw.get_data()
    
    def process_channel(ch_idx):
        ch_name = ch_names[ch_idx]
        raw_channel = raw.copy().load_data()
        raw_channel.pick_channels(ch_names)
        raw_channel.info['bads'] = [ch_name]
        noised_data = original_data[ch_idx, :].copy()
        raw_channel.interpolate_bads(reset_bads=False, verbose=False)
        interpolated_data = raw_channel.get_data(picks=[ch_name])[0]
        snr = compute_snr(interpolated_data, noised_data)
        proba = snr_db_to_probability(-snr)
        return ch_name, snr, proba
    
    snr_values = {}
    snr_probabilities = {}
    high_prob_channels = []
    high_prob = []

    if optimized:
        results = Parallel(n_jobs=4)(
            delayed(process_channel)(ch_idx) for ch_idx in range(len(ch_names))
        )
    else:
        results = []
        for ch_idx in range(len(ch_names)):
            result = process_channel(ch_idx)
            results.append(result)
            
    for ch_name, snr, proba in results:
        snr_values[ch_name] = snr
        snr_probabilities[ch_name] = proba
        if proba > 0.8:
            high_prob_channels.append(ch_name)
            high_prob.append(proba)
    
    fig = plot_topomap(list(snr_probabilities.values()), raw, high_prob, high_prob_channels)
    plt.close(fig)
    return high_prob_channels, high_prob, fig

def DNC_corr(raw, threshold_corr=0.65, threshold_perc=5):
    correlations = calculate_correlations(raw)
    
    def plot_topomap(correlations, raw):
        """Построить topomap для значений корреляций"""
        montage = raw.get_montage()
        ch_pos = np.array([raw.info['chs'][i]['loc'][:2] for i in range(raw.info['nchan'])])
        fig, ax = plt.subplots()
        im, _ = mne.viz.plot_topomap(np.abs(correlations), ch_pos, axes=ax, show=False, names=raw.ch_names, cmap='viridis', vlim = (0.5, 1))
        ax.set_title('Топомапа корреляций')
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Correlation Coefficient')
        return fig
    
    fig = plot_topomap(np.mean(correlations, axis=0), raw)

    result = np.mean(correlations, axis=0)
    p5 = np.percentile(correlations, threshold_perc, axis=(0, 1))
    artefacts_indexes = result < p5

    binary_matrix = correlations < threshold_corr
    probs = binary_matrix.mean(axis=0)
    noised_channels = ((np.array(raw.ch_names)[artefacts_indexes]).tolist())
    score = probs[artefacts_indexes]
    return noised_channels, score, [fig]


def normalization(x):
    q75 = np.percentile(x, 75, axis=(0, 1), keepdims=True)
    q25 = np.percentile(x, 25, axis=(0, 1), keepdims=True)
    iqr = q75 - q25
    x_norm = x/iqr
    return x_norm 



def DNC_electrical_distance(raw, vis=False, thr_std=3):

    def sigmoid(x):
        return 1/(1 + np.exp(-x))
    
    bridged_idx, ed_matrix = compute_bridged_electrodes(raw, verbose=False)
  
    ed_matrix = ed_matrix.copy()
    picks = mne.pick_types(raw.info, eeg=True)
    tril_idx = np.tril_indices(picks.size)
    for epo_idx in range(ed_matrix.shape[0]):
        ed_matrix[epo_idx][tril_idx] = ed_matrix[epo_idx].T[tril_idx]
    channel_names = np.array([raw.ch_names[i] for i in picks])

    ed_matrix = np.nanmin(ed_matrix, axis=1)

    ed_matrix_norm = normalization(ed_matrix)
    elec_dists = np.median(ed_matrix_norm, axis=0)
    
    picks = mne.pick_types(raw.info, eeg=True)
    ch_names = raw.ch_names

    results = (ed_matrix_norm - elec_dists).mean(axis=0)
    probs = sigmoid(results)
    artefact_indices = results > thr_std

    fig, ax = plt.subplots()
    pos = np.array([raw.info['chs'][i]['loc'][:2] for i in range(raw.info['nchan'])])
    mne.viz.plot_topomap(
        probs, pos, show=True, cmap='RdBu_r', vlim=(0, 1.0),
        names=raw.ch_names, axes=ax
    )
    ax.set_title('Топомапа вероятности')
    plt.tight_layout()
    plt.close(fig)
    return (channel_names[artefact_indices]).tolist(), probs[artefact_indices], [fig]

def DNC_ransac(raw):  
    ransac = Ransac(verbose=False)
    epochs = mne.make_fixed_length_epochs(raw, duration=10, overlap=0.5, preload=True)
    _ = ransac.fit_transform(epochs)
    probabilities = ransac.bad_log.mean(axis=0)
    bad_channels = ransac.bad_chs_
    scores = probabilities[mne.pick_channels(raw.info['ch_names'], bad_channels)]
    fig, ax = plt.subplots()
    pos = np.array([raw.info['chs'][i]['loc'][:2] for i in range(raw.info['nchan'])])
    mne.viz.plot_topomap(
        probabilities, pos, show=True, cmap='RdBu_r', vlim=(0, 1.0),
        names=raw.ch_names, axes=ax
    )
    ax.set_title('Топомапа вероятности')
    plt.tight_layout()
    return bad_channels, scores, fig

def compared_spectrum(inst1, inst2, l_freq=0.5, h_freq=80, fmin=0, fmax=100):
    psd_before = inst1.compute_psd(fmin=fmin, fmax=fmax, 
                            remove_dc=False, verbose=False
    )
    psd_after = inst2.compute_psd(fmin=fmin, fmax=fmax, 
                            remove_dc=False, verbose=False
    )
    if isinstance(inst1, mne.Epochs) and isinstance(inst2, mne.Epochs):
        psd_before = psd_before.average()
        psd_after = psd_after.average()
    # Преобразование PSD в dB с корректным масштабированием
    mean_psd_before = 10*np.log10(psd_before.get_data() * 1e12)
    mean_psd_after = 10*np.log10(psd_after.get_data() * 1e12)

    # Получение частот
    freqs = psd_before.freqs

    # Определение диапазонов ритмов ЭЭГ
    bands = {
        'Delta': (max(l_freq, 0.5), 4),
        'Theta': (4, 8),
        'Alpha': (8, 13),
        'Beta': (13, 30),
        'Gamma': (30, min(h_freq, 80))
    }

    # Создание списка PSD и соответствующих названий для цикла
    psd_list = [mean_psd_before, mean_psd_after]
    titles = ['Spectrum before', 'Spectrum after']
    colors = ['b', 'g']

    ymin = np.floor(min(mean_psd_before.min(), mean_psd_after.min()) / 10) * 10
    ymax = np.ceil(max(mean_psd_before.max(), mean_psd_after.max()) / 10) * 10

    # Создание фигуры и осей
    fig, axs = plt.subplots(2, 1, figsize=(14, 10), sharex=False)

    # Цикл по PSD до и после фильтрации
    for idx, (mean_psd, title, color) in enumerate(zip(psd_list, titles, colors)):
        ax = axs[idx]
        y_mean = np.mean(mean_psd, axis=0)
        y_std = np.std(mean_psd, axis=0)
        
        # Построение графика
        ax.plot(freqs, y_mean, color=color)
        ax.fill_between(freqs, y_mean - y_std, y_mean + y_std, color=color, alpha=0.3)
        ax.set_title(title)
        ax.set_ylabel('PSD (dB/µV²/Hz)')
        ax.grid(True)
        
        # Расчёт и отображение средней мощности в каждом диапазоне
        band_powers = {}
        for band_name, (fmin, fmax) in bands.items():
            idx_band = np.logical_and(freqs >= fmin, freqs <= fmax)
            band_power = y_mean[idx_band].mean()
            band_powers[band_name] = band_power
            
            # Добавление вертикальных пунктирных линий и заливки диапазонов
            ax.axvline(fmin, color='red', linestyle='--', linewidth=1)
            ax.axvline(fmax, color='red', linestyle='--', linewidth=1)
            ax.fill_betweenx([ymin, ymax], fmin, fmax, color='grey', alpha=0.05)
            
            # Отображение названия диапазона и средней мощности
            ax.text((fmin + fmax) / 2, ymax - 2, f"{band_name}\n{band_power:.1f} dB",
                    horizontalalignment='center', verticalalignment='top', fontsize=9, zorder=4)
        
        # Установка одинаковых пределов по оси Y
        ax.set_ylim(ymin, ymax)
        ax.set_xlim(freqs.min(), freqs.max())
        ax.set_xticks(np.arange(freqs.min(), freqs.max()+1, 2))
        ax.set_yticks(np.arange(ymin, ymax+1, 5))
        ax.set_xlabel('Частота (Гц)')

    # Настройка макета и отображение графика
    plt.tight_layout()
    plt.close(fig)
    return fig
