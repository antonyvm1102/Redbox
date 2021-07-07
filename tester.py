import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time as time
import os
import csv
import Redbox_v2.signal_processing as dsp

# file = r"C:\Users\mdk\Desktop\93307\Ruwe trillingsdata\positie_1\20181001112633000195.txt"

# start = time.time()
# data = np.loadtxt(file,delimiter=' ')
# elapsed_time = time.time()-start
# print(data)
# print(elapsed_time)

# start = time.time()
# data = pd.read_csv(file,sep=' ',comment= '#', header = None,names=('t','x','y','z'))
# elapsed_time = time.time()-start
# print(data)
# print(elapsed_time)

# number of samples
N = 2 ** 11
# Sampling space
T = 1. / 400
# frequency
w = 5
# Amplitude
A = 1


t = np.linspace(0, N * T, N, endpoint=False)
x = A * np.sin(w * 2 * np.pi * t)

ampl, freq =  dsp.FFT(x,T)

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax1.plot(t,x)
ax2 = fig.add_subplot(2,1,2)
ax2.stem(freq[0:70],ampl[0:70],markerfmt='-')
plt.show()