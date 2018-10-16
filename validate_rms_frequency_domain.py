import signal_processing as sp
import time
import matplotlib.pyplot as plt
import numpy as np
import math

"""
Validate translation of known time signal to RMS values per 1/3 octave band frequencies
"""

start_time = time.time()

sampling_rate = 400
n_samples = 2**19
                                        # generate sum of sine functions with known frequencies and amplitudes
f = [4., 8., 16., 31.5, 63.]            # list of frequencies [Hz]
a = [10., 50., 30., 20., 5.]            # list of amplitudes [mm/s]
t = np.linspace(start = 0., stop = n_samples / sampling_rate, num = n_samples, endpoint = False)
z = np.zeros_like(t)
rms_theory = [0,0,0,0,0]
for i in range(len(f)):
    z += a[i] * np.sin(2.*math.pi*f[i]*t)
    rms_theory[i] = a[i]/math.sqrt(2)

ampl, freq = sp.FFT(z[0:n_samples], dT=t[1]-t[0])
rms , freqband = sp.FFT_to_OneThird_Octave(ampl,freq[1]-freq[0],0.625/2**(1/3),80)
# max_vel_z = np.append(max_vel_z, sp.n_minutes_max(z,n=5,dt=t[1]-t[0]))

end_time = time.time()
dtime = end_time-start_time
print("elapsed time = %s" %dtime)

plt.subplot(2,1,1)
plt.plot(freqband, rms, '-', label = 'Numerical result')
plt.plot(f,rms_theory, 'x', label = 'Theoretical result')
plt.xscale('log')
plt.xlim([1,100])
plt.grid(which = 'both')
#plt.yscale('log')
plt.xlabel('1/3 octave band frequency [Hz]')
plt.ylabel('RMS of amplitude [mm/s]')
plt.legend(bbox_to_anchor=(-0.05,-0.2))
plt.subplot(2,1,2)
plt.plot(freq, ampl, '-')
plt.plot(f,a, 'x')
plt.xscale('log')
plt.xlim([1,100])
plt.grid(which = 'both')
plt.xlabel('frequency [Hz]')
plt.ylabel('FFT amplitude [mm/s]')
plt.plot()
plt.subplots_adjust(top=0.95, bottom=0.1, left=0.15, right=0.95, hspace=0.3)
plt.suptitle('Comparison of numerical and theoretical result for self-generated input signal')
plt.show()