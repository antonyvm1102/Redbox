"""
This example displays the routine used to obtain a proper result from a FFT-analysis

Choosing a sampling space T as a certain particle of 2 * pi or many samples will result in best signal.
Also a number of samples equal to a power of 2 (e.g. 16,32,64 ...) wil improve the results

Just the first part {range 0 to 1/ (2 * T)} of the FFT result has a relevant outcome.
with steps of (4 * T) / N [Hz].

amplitude of a certain value of the frequency is the maximum occuring amplitude at that frequency.
this value can be calculated from the FFT result in the form of a + b i. A = (2 / N) * (a**2 + b**2)**(1/2)
Beware of a certain error because time steps never are a particle of 2* pi (about 2-5%)

"""

import numpy as np
import math
from scipy import fftpack
import matplotlib.pyplot as plt

# RMS
def rms_time_dom(signal):
    N = len(signal)
    return math.sqrt(np.sum(np.power(signal,2))/N)

def rms_freq_dom(amplitude):
    return math.sqrt(2*np.sum(np.power(amplitude, 2))/np.power(len(amplitude),2))

f = 50      # Frequency, in cycles per second, or Hertz
f_s = 256  # Sampling rate, or number of measurements per second
a = 50      # Amplitude

t = np.linspace(0, 2, 2*f_s, endpoint=False)
x = a * np.sin(f * 2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(t, x)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Signal amplitude')

X_sci = fftpack.rfft(x)
X_np = np.fft.rfft(x)
freqs_sci = fftpack.rfftfreq(len(x)) * f_s
freqs_np = np.fft.rfftfreq(len(x)) *f_s
print('Magnitude: length of scipy is %s. Length of np is %s' %X_sci.size, X_np.size))
print('Frequencies: length of scipy is %s. Length of np is %s' %(freqs_sci.size, freqs_np.size))


fig, ax = plt.subplots()

ax.bar(freqs_sci, np.abs(X_sci)/f_s, 'r')
ax.bar(freqs_np, np.abs(X_np)/f_s, 'b')
ax.set_xlabel('Frequency in Hertz [Hz]')
ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
ax.set_xlim(-f_s / 2, f_s / 2)
ax.set_ylim(-5, 110)

rms_theory = a / np.sqrt(2)
rms_time = rms_time_dom(x)
rms_freq = rms_freq_dom(X)

print(rms_theory, rms_time, rms_freq)

plt.show()

