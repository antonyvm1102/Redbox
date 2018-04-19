
import signal_processing as sp
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime

start_time = time.time()
folder = r"C:\Users\mel\Documents\Python\Betacampus_pos1"
files = sp.obtain_files(folder)
filename = folder + "\\" + files[2]

# max_vel_z = np.zeros(1)
t,x,y,z = sp.obtain_data(filename)

ampl, freq = sp.FFT(z[0:2**19], dT=t[1]-t[0])
rms , freqband = sp.FFT_to_OneThird_Octave(ampl,freq[1]-freq[0],0.1,100)
# max_vel_z = np.append(max_vel_z, sp.n_minutes_max(z,n=5,dt=t[1]-t[0]))

end_time = time.time()
dtime = end_time-start_time
print("elapsed time = %s" %dtime)

plt.subplot(2,1,1)
plt.plot(freqband, rms, '-')
plt.xscale('log')
plt.xlim([0.1, 100])
plt.yscale('log')
plt.xlabel('frequency')
plt.ylabel('RMS of amplitude [mm/s]')
plt.subplot(2,1,2)
plt.plot(freq, ampl, '-')
plt.xscale('log')
plt.xlim([0.1,100])
plt.plot()
plt.show()



