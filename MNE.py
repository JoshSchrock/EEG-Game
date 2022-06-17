import os
import numpy as np
import mne

data_raw_file = r"D:\Pycharm Projects\EEG-Game\BCI Evasion 2\EEGExports\EEG-Game_Josh Schrock_EPOCFLEX-F0000172_EPOCFLEX_123045_2022.06.15T16.01.52.04.00.edf"
raw = mne.io.read_raw_edf(data_raw_file)

raw.plot_psd(fmax=50)
raw.plot(duration=5, n_channels=30)

mag_channels = mne.pick_types(raw.info, meg='mag')
raw.plot(duration=60, order=mag_channels, n_channels=len(mag_channels),
         remove_dc=False)