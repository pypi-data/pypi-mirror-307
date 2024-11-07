from .pipeline import Interpolate, AutoICA, Sequence, Rereference, Resample, CheckEvents, Cropping, FilterBandpass
from .pipeline import SetMontage, BadChannelsDetector, Raw2Epoch, BadEpochsDetector, DetrendEpochs, BaselineEpochs
from .scenarious import get_file_info
import mne 


class EpochsAnalysier():
    def __init__(self, scenarious_name, stimulus_list, roi, tmin, tmax, baseline=(None, 0), detrend_type='linear'):
        self.stimulus_list = stimulus_list
        self.scenarious_name = scenarious_name
        self.tmin = tmin
        self.tmax = tmax
        self.baseline = baseline
        self.roi = roi
        self.detrend_type = detrend_type
        self.epochs_store = []
        self.pathes = {}

    def compute(self, record, epoch_path):
        self.epoch_path = epoch_path
        mne.set_log_level('ERROR')
        raw = mne.io.read_raw_fif(record, preload=True)
        mne.set_log_level('WARNING')
        self.precompute_epochs = Sequence(
                        raw2epoch = Raw2Epoch(self.stimulus_list, self.scenarious_name, tmin=self.tmin, tmax=self.tmax, baseline=None),
                        detector = BadEpochsDetector(self.roi),
                        baseliner = BaselineEpochs(baseline=self.baseline),
                        detrender = DetrendEpochs(detrend_type=self.detrend_type),
                        )
        self.precompute_epochs(raw)
        self.pathes['detector'] = self.precompute_epochs.detector.save_report(self.epoch_path, pref='detector_')
        self.pathes['detrender'] = self.precompute_epochs.detrender.save_report(self.epoch_path, pref='detrender_')
        self.pathes['baseliner'] = self.precompute_epochs.baseliner.save_report(self.epoch_path, pref='baseliner_')
        return self.precompute_epochs.insts
    
    def get_report(self):
        report_images = {
            'detector_SNR_hist_image': self.pathes['detector'][0],
            'detrend_SNR_hist_image': self.pathes['detrender'][0],
            'baseline_SNR_hist_image': self.pathes['baseliner'][0],
            'detector_spectrum_hist_image': self.pathes['detector'][1],
            'detrend_spectrum_hist_image': self.pathes['detrender'][1],
            'baseline_spectrum_hist_image': self.pathes['baseliner'][1],
        }
        raw2epoch_report, _  = self.precompute_epochs.raw2epoch.get_transform_report()
        detector_report, _ = self.precompute_epochs.detector.get_transform_report()
        detrender_report, _ = self.precompute_epochs.detrender.get_transform_report()
        baseliner_report, _ = self.precompute_epochs.baseliner.get_transform_report()
        merged_dict = {**raw2epoch_report, **detector_report,  **detrender_report, **baseliner_report, **report_images}
        return merged_dict

class AutoCleaner():
    def __init__(self, scenarious_name, reref, n_components, l_freq, h_freq, 
                 notch_freq, down_sfreq, excluded_channels, output_path=None):
        
        self.scenarious_name = scenarious_name
        self.reref = reref
        self.n_components = n_components
        self.l_freq = l_freq
        self.h_freq = h_freq
        self.notch_freq = notch_freq
        self.down_sfreq = down_sfreq
        self.excluded_channels = excluded_channels
        self.pathes = {}
        self.output_path = output_path

    def clean(self, file_path, elc_file, bad_channels, progress_bar=None):
        self.file_path = file_path
        raw = mne.io.read_raw_brainvision(self.file_path, preload=True)
        raw = raw.drop_channels(self.excluded_channels)

        raw.info['bads'] = bad_channels
        self.prep_pipe = Sequence(
                        setter_montage = SetMontage('waveguard64', elc_file, mode='Cz', threshold=0.019, interpolate=False),
                        filter = FilterBandpass(l_freq=self.l_freq, h_freq=self.h_freq, notch_freq=self.notch_freq, report=True),
                        cropper = Cropping(scenarious_name=self.scenarious_name, report=False),
                        rerefer = Rereference(self.reref, exclude='bads', report=True),
                        resampler = Resample(sfreq=self.down_sfreq),
                        ica = AutoICA(n_components=self.n_components, method='picard', report=True),
                        interpolater = Interpolate()
                        )
        self.prep_pipe(raw, progress_bar)
        self.pathes['filter'] = self.prep_pipe.filter.save_report(self.output_path, pref='filter_')
        self.pathes['reref'] = self.prep_pipe.rerefer.save_report(self.output_path, pref='reref_')
        self.pathes['ica'] = self.prep_pipe.ica.save_report(self.output_path, pref='ica_')
        return self.prep_pipe.insts
    
    def get_report(self,):
        ica_info, _ = self.prep_pipe.ica.get_transform_report()
        report_images = {
            'filter_spectrum_image': self.pathes['filter'][0],
            'reref_spectrum_image': self.pathes['reref'][0],
            'ica_all_comp_image': self.pathes['ica'][-2],
            'ica_each_comp_images': self.pathes['ica'][0:-2],
            'ica_spectrum_image':self.pathes['ica'][-1]
        }
        merged_dict = {**{'Record':self.file_path}, **ica_info, **report_images}
        return merged_dict
    
class QualityChecker():
    def __init__(self, excluded_channels, l_freq, h_freq, notch_freq, noise_detector):
        self.excluded_channels = excluded_channels
        self.l_freq = l_freq
        self.h_freq = h_freq
        self.notch_freq = notch_freq
        self.noise_detector = noise_detector
        self.file_path = None
        self.elc_path = None
        self.scenarious_name = None
        self.checker = None
        self.detector = None
        self.qc_path = None
        self.pathes = {}

    def check(self, file_path, elc_path, qc_path, scenarious_name, progress_bar=None):
        self.file_path = file_path
        self.elc_path = elc_path
        self.scenarious_name = scenarious_name
        self.qc_path = qc_path
        # Стандартный препроцессинг согласно Quality Check
        progress_bar.set_postfix(статус='Reading file...')
        raw = mne.io.read_raw_brainvision(self.file_path, preload=True, verbose=False)
        raw = raw.drop_channels(self.excluded_channels)        
        
        self.qc_pipe = Sequence(
                                setter_montage = SetMontage('waveguard64', self.elc_path, mode='Cz', threshold=0.019, interpolate=False),
                                autofilter = FilterBandpass(l_freq=self.l_freq, h_freq=self.h_freq, notch_freq=self.notch_freq, report=True),
                                cropper = Cropping(scenarious_name=self.scenarious_name, report=True),
                                checker = CheckEvents(scenarious_name=self.scenarious_name, report=True),
                                detector = BadChannelsDetector(method=self.noise_detector, report=True),
                                )
        self.qc_pipe(raw, progress_bar)
        progress_bar.set_postfix(status='Saving reports...')
        self.pathes['filter'] = self.qc_pipe.autofilter.save_report(self.qc_path, pref='filter_')
        self.pathes['events'] = self.qc_pipe.checker.save_report(self.qc_path, pref='events_')
        self.pathes['detector'] = self.qc_pipe.detector.save_report(self.qc_path, pref='detector_')

    def get_report(self,):
        # Получение основной информации о файле
        data = get_file_info(self.file_path, self.elc_path)
        events_info, _ = self.qc_pipe.checker.get_transform_report()
        detector_info, _ = self.qc_pipe.detector.get_transform_report()
        QC_images = {
            'filter_image': self.pathes['filter'][0],
            'clusters_image': self.pathes['detector'][0],
            'hist_bridges_image': self.pathes['detector'][1],
            'Noised_channels_image': self.pathes['detector'][2],
        }
        # Сохранение переменных для отчёта
        events_info['Record'] = self.file_path
        merged_dict = {**events_info, **detector_info, **data, **QC_images}
        merged_dict['N_bad_channels'] = len(set(merged_dict['HighAmp']) | set(merged_dict['LowAmp']) | set(merged_dict['Bridged']) | set(merged_dict['Noise_Rate']))
        return merged_dict