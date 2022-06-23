import os
import numpy as np
import mne
import matplotlib.pyplot as plt
#  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6088222/
import scipy.io

annot_kwargs = dict(fontsize=12, fontweight='bold',
                    xycoords="axes fraction", ha='right', va='center')

try:
    mne.set_config('MNE_USE_CUDA', 'true')
except TypeError as err:
    print(err)

def set_matplotlib_defaults():
    fontsize = 8
    params = {'font.size': fontsize,
              'axes.labelsize': fontsize,
              'legend.fontsize': fontsize,
              'xtick.labelsize': fontsize,
              'ytick.labelsize': fontsize,
              'axes.titlesize': fontsize + 2,
              'figure.max_open_warning': 200,
              'axes.spines.top': False,
              'axes.spines.right': False,
              'axes.grid': True,
              'lines.linewidth': 1
              }
    plt.rcParams.update(params)

# good channels: [4,5,6,7,8,9,10,11,12,13,14,15,16,17]
# all channels ['TIME_STAMP_s', 'TIME_STAMP_ms', 'COUNTER', 'INTERPOLATED', 'AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4', 'HighBitFlex', 'SaturationFlag', 'RAW_CQ', 'BATTERY', 'BATTERY_PERCENT', 'MarkerIndex', 'MarkerType', 'MarkerValueInt', 'MARKER_HARDWARE', 'CQ_AF3', 'CQ_F7', 'CQ_F3', 'CQ_FC5', 'CQ_T7', 'CQ_P7', 'CQ_O1', 'CQ_O2', 'CQ_P8', 'CQ_T8', 'CQ_FC6', 'CQ_F4', 'CQ_F8', 'CQ_AF4', 'CQ_OVERALL', 'EQ_SampleRateQua', 'EQ_OVERALL', 'EQ_AF3', 'EQ_F7', 'EQ_F3', 'EQ_FC5', 'EQ_T7', 'EQ_P7', 'EQ_O1', 'EQ_O2', 'EQ_P8', 'EQ_T8', 'EQ_FC6', 'EQ_F4', 'EQ_F8', 'EQ_AF4', 'CQ_CMS', 'CQ_DRL']
stim_channels = ['MarkerIndex', 'MarkerType', 'MarkerValueInt', 'MARKER_HARDWARE']
exclude = ['TIME_STAMP_s', 'TIME_STAMP_ms', 'COUNTER', 'INTERPOLATED', 'HighBitFlex', 'SaturationFlag', 'RAW_CQ', 'BATTERY', 'BATTERY_PERCENT', 'CQ_AF3', 'CQ_F7', 'CQ_F3', 'CQ_FC5', 'CQ_T7', 'CQ_P7', 'CQ_O1', 'CQ_O2', 'CQ_P8', 'CQ_T8', 'CQ_FC6', 'CQ_F4', 'CQ_F8', 'CQ_AF4', 'CQ_OVERALL', 'EQ_SampleRateQua', 'EQ_OVERALL', 'EQ_AF3', 'EQ_F7', 'EQ_F3', 'EQ_FC5', 'EQ_T7', 'EQ_P7', 'EQ_O1', 'EQ_O2', 'EQ_P8', 'EQ_T8', 'EQ_FC6', 'EQ_F4', 'EQ_F8', 'EQ_AF4', 'CQ_CMS', 'CQ_DRL']
#  eog_channels = ['AF3', 'AF4']


#  create raw object with only eeg and markers, exculde all other info
edf_file_name = 'EEG-Game_Josh Schrock_EPOCFLEX-F0000172_EPOCFLEX_123045_2022.06.15T16.01.52.04.00'
data_raw_file = f"{os.getcwd()}\\BCI Evasion 2\\EEGExports\\{edf_file_name}.edf"
raw = mne.io.read_raw_edf(data_raw_file, stim_channel=stim_channels, exclude=exclude, preload=True)

# Form the 10-20 montage
mont1020 = mne.channels.make_standard_montage('standard_1020')
# Choose what channels you want to keep
# Make sure that these channels exist e.g. T1 does not exist in the standard 10-20 EEG system!
kept_channels = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']
ind = [i for (i, channel) in enumerate(mont1020.ch_names) if channel in kept_channels]
mont1020_new = mont1020.copy()
# Keep only the desired channels
mont1020_new.ch_names = [mont1020.ch_names[x] for x in ind]
kept_channel_info = [mont1020.dig[x+3] for x in ind]
# Keep the first three rows as they are the fiducial points information
mont1020_new.dig = mont1020.dig[0:3]+kept_channel_info
mont1020_new.plot()
raw = raw.set_montage(mont1020_new)
raw.plot()

def custom_plot_psd(raw_eeg):

    # The line colors for the bad channels will be red.
    bads = []
    colors = ['k'] * raw_eeg.info['nchan']
    for b in bads:
        colors[raw_eeg.info['ch_names'].index(b)] = 'r'

    ###############################################################################
    # First we show the log scale to spot bad sensors.

    fig, axes = plt.subplots(1, 2, figsize=(7, 2.25))
    set_matplotlib_defaults()
    ax = axes[0]
    raw_eeg.plot_psd(
        average=False, line_alpha=0.6, fmin=0, fmax=64, xscale='log',
        spatial_colors=False, show=False, ax=[ax])
    ax.set(xlabel='Frequency (Hz)', title='')
    # A little hack fix for matplotlib bug on some systems
    for text in fig.axes[0].texts:
        pos = text.get_position()
        if pos[0] <= 0:
            text.set_position([0.1, pos[1]])

    for l, c in zip(ax.get_lines(), colors):
        if c == 'r':
            l.set_color(c)
            l.set_zorder(3)
        else:
            l.set_zorder(4)

    # Next, the linear scale to check power line frequency

    ax = axes[1]
    raw_eeg.plot_psd(
        average=False, line_alpha=0.6, n_fft=2048, n_overlap=1024, fmin=0,
        fmax=64, xscale='linear', spatial_colors=False, show=False, ax=[ax])
    ax.set(xlabel='Frequency (Hz)', ylabel='', title='')
    ax.axvline(50., linestyle='--', alpha=0.25, linewidth=2)
    ax.axvline(50., linestyle='--', alpha=0.25, linewidth=2)

    for ai, (ax, label) in enumerate(zip(axes, 'AB')):
        ax.annotate(label, (-0.15 if ai == 0 else -0.1, 1), **annot_kwargs)

    fig.tight_layout()
    plt.show()

raw.plot_psd(fmax=50)
custom_plot_psd(raw)
# Band-pass the data channels (EEG)
filtered_raw = raw.copy().filter(
    1, 40, l_trans_bandwidth='auto', h_trans_bandwidth='auto',
    filter_length='auto', phase='zero', fir_window='hamming',
    fir_design='firwin')
custom_plot_psd(filtered_raw)

mat = {}
arr = []

for x in kept_channels:
    arr.append(filtered_raw.get_data(picks=[x]))
matlab = np.concatenate(arr)
mat['arr'] = np.array(matlab.transpose())


save_mat = f"{os.getcwd()}\\MATExports\\{edf_file_name}.mat"
scipy.io.savemat(save_mat, mat)

# from mne.datasets import fetch_fsaverage
# fs_dir = fetch_fsaverage(verbose=True)
# subjects_dir = os.path.dirname(fs_dir)
#
# # src = os.path.join(fs_dir, 'bem', 'fsaverage-ico-5-src.fif')
# src = mne.setup_volume_source_space()
# trans = 'fsaverage'  # MNE has a built-in fsaverage transformation
# # Check that the locations of EEG electrodes is correct with respect to MRI
# mne.viz.plot_alignment(
#     raw.info, src=src, eeg=['original', 'projected'], trans=trans,
#     show_axes=True, mri_fiducials=True, dig='fiducials')
#
# # plot------------------------------
# for matrix in corr_matrix:
#     new_matrix = []
#     for i in matrix:
#         list = []
#         for j in i:
#             list.append(j[0])
#         new_matrix.append(list)
#
#     print(matrix)
#     print(new_matrix)
#     print(src[0])
#
#     degree = mne_connectivity.degree(new_matrix, 0.15)
#     stc = mne.VolSourceEstimate(degree, [src[0]['vertno']], 0, 1, 'bst_resting')
#     brain = stc.plot(
#         src, clim=dict(kind='percent', lims=[75, 85, 95]), colormap='gnuplot',
#         subjects_dir=subjects_dir, mode='glass_brain')
