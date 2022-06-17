import pyedflib
import numpy as np
import matplotlib.pyplot as plt
import time
import os

edf_file_name = 'EEG-Game_Josh Schrock_EPOCFLEX-F0000172_EPOCFLEX_123045_2022.06.15T16.01.52.04.00'
data_raw_file = f"{os.getcwd()}\\BCI Evasion 2\\EEGExports\\{edf_file_name}.edf"
f = pyedflib.EdfReader(data_raw_file)
n = f.signals_in_file
print(n)
signal_labels = f.getSignalLabels()
print(signal_labels)
sigbufs = np.zeros((n, f.getNSamples()[0]))
fig = plt.figure()
ax = plt.axes()
ax.plot(f.readSignal(26))
plt.show()


# for i in np.arange(n):
#     fig = plt.figure()
#     ax = plt.axes()
#     sigbufs[i, :] = f.readSignal(i)
#     ax.plot(f.readSignal(i))
#     plt.show()
#     time.sleep(3)