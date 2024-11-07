import numpy as np 
import mne 

def get_ANT_ROI():
    P1_ROI = ['P3', 'Pz', 'P4', 'POz', 'P1', 'P2']
    N1_ROI = ['P3', 'Pz', 'P4', 'O1', 'Oz', 'O2']
    CNV_ROI = ['FCz', 'Cz']
    N2_ROI = ['P3', 'Pz', 'P4', 'POz', 'P1', 'P2']
    P3_ROI = ['P3', 'Pz', 'P4', 'POz', 'P1', 'P2']
    COMPONENTS_ROI = {'P1': P1_ROI,
           'N1': N1_ROI,
           'CNV': CNV_ROI,
           'N2': N2_ROI,
           'P3': P3_ROI}
    return COMPONENTS_ROI

def make_ANT_events(raw, target_stimulus):
    events, event_id = mne.events_from_annotations(raw, verbose=False)
    desired_stimulus = 'Stimulus/s200'
    target_stimuli_codes = dict(list(zip(event_id.values(), event_id.keys())))
    filtered_events = []
    for i in range(0, len(events) - 1):
        current_event = events[i]
        next_event = events[i + 1]
        if target_stimuli_codes[current_event[2]] in target_stimulus:
            if target_stimuli_codes[next_event[2]] == desired_stimulus:
                filtered_events.append(current_event)
    filtered_event_id = {stimulus: event_id[stimulus] for stimulus in target_stimulus if stimulus in event_id}
    filtered_events = np.array(filtered_events)
    epochs = mne.Epochs(raw, filtered_events, event_id=filtered_event_id, tmin=-0.2, tmax=1.0, preload=True, 
                        baseline=(None, 0), event_repeated='merge', verbose=False)
    return epochs, filtered_event_id, filtered_events


def make_RiTi_events(raw, stimulus_list, tmin, tmax, baseline, filt=False):
    # Получаем события и идентификаторы
    events, event_id = mne.events_from_annotations(raw, verbose=False)
    inverted_dict = {v: k for k, v in event_id.items()}  # Инвертируем event_id для удобства
    if filt:
        filtered_events = []
        for event in events:
            stimulus = inverted_dict[event[2]]
            if stimulus in stimulus_list:
                filtered_events.append(event)
        # Преобразуем отфильтрованные события в numpy массив
        filtered_events = np.array(filtered_events, dtype=int)
    else:    
        filtered_events = np.array(events, dtype=int)

    # Инициализируем список для будущих событий-дуплетов и словарь для имен и кодов дуплетов
    duplet_events = []
    duplet_names = {}
    
    duplet_code = 1  # Начальный код для дуплетов

    # Проходим по событиям, начиная со второго (index 1)
    for i in range(1, len(filtered_events)):
        current_stimulus = inverted_dict[filtered_events[i, 2]]  # Текущий стимул
        previous_stimulus = inverted_dict[filtered_events[i - 1, 2]]  # Предыдущий стимул

        # Проверяем, что текущий и предыдущий стимулы в списке и они различны
        if (current_stimulus in stimulus_list) and (previous_stimulus in stimulus_list) and (current_stimulus != previous_stimulus):
            # Создаем имя для дуплета, например, 'Stimulus/s11_s12'
            duplet_name = f'{previous_stimulus[9:]}_{current_stimulus[9:]}'
            # Если дуплет еще не был добавлен в словарь, присваиваем ему код
            if duplet_name not in duplet_names:
                duplet_names[duplet_name] = duplet_code
                duplet_code += 1

            # Добавляем событие с кодом второго стимула дуплета
            duplet_events.append([filtered_events[i, 0], 0, duplet_names[duplet_name]])

    # Преобразуем duplet_events в numpy массив для использования в MNE
    duplet_events = np.array(duplet_events, dtype=int)

    # Создание event_id для дуплетов
    event_id_duplets = {name: code for name, code in duplet_names.items()}

    # Создаем epochs на основе полученных событий-дуплетов
    epochs = mne.Epochs(raw, events=duplet_events, event_id=event_id_duplets, tmin=tmin, tmax=tmax, 
                        baseline=baseline, preload=True, verbose=False)

    return epochs

