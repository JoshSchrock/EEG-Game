import pyedflib
import numpy as np
import matplotlib.pyplot as plt
import time

f = pyedflib.EdfReader(r"D:\Pycharm Projects\EEG-Game\BCI Evasion 2\EEGExports\EEG-Game_Josh Schrock_EPOCFLEX-F0000172_EPOCFLEX_123045_2022.06.15T16.11.10.04.00.edf")
n = f.signals_in_file
print(n)
signal_labels = f.getSignalLabels()
sigbufs = np.zeros((n, f.getNSamples()[0]))

for i in np.arange(n):
    fig = plt.figure()
    ax = plt.axes()
    sigbufs[i, :] = f.readSignal(i)
    ax.plot(f.readSignal(i))
    plt.show()
    time.sleep(3)