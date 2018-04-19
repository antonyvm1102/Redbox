import signal_processing as sp
import numpy as np
import sys
import time
import matplotlib.pyplot as plt

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * float(count) / float(total), 2)
    bar = '+' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s ...%s' % (bar, percents, '%', status))
    sys.stdout.flush()

def largest_power_of_base(n, base = 2):
    """
    Returns the largest power of base in a number of samples
    :param n:       (integer) number of samples
    :param base:    (integer) base of power to be considered, default is 2
    :return:        (integer) largest power of base
    """
    count = 1
    while n // base > 1:
        count += 1
        n = n // base
    return base ** count

stime = time.time()

dir_path = "C:\\Users\\mel\\Documents\\Python\\Betacampus_pos1\\"

file_list = sp.obtain_files(dir_path)

f_band = sp.OneThird_octave(0.625 / 2**(1/3), 80 * 2**(1/3))

rms_x_array = np.zeros((len(f_band), len(file_list)))
rms_y_array = np.zeros((len(f_band), len(file_list)))
rms_z_array = np.zeros((len(f_band), len(file_list)))

for i in range(11):
    filename = dir_path + file_list[i]
    t,x,y,z = np.loadtxt(filename, dtype="float", comments="#", unpack=True)
    n = largest_power_of_base(len(t))
    xf, f = sp.FFT(x[:n], dT=t[1] - t[0])
    yf = sp.FFT_amplitude(y[:n])
    zf = sp.FFT_amplitude(z[:n])
    rms_x_array[..., i] = sp.FFT_to_OneThird_Octave2(xf, f[1] - f[0], f_band)
    rms_y_array[..., i] = sp.FFT_to_OneThird_Octave2(yf, f[1] - f[0], f_band)
    rms_z_array[..., i] = sp.FFT_to_OneThird_Octave2(zf, f[1] - f[0], f_band)
    progress(i, len(file_list), "processing %s of %s" % (i, len(file_list)))
    if i%10 == 0:
        np.savetxt("14208_betacampus_pos1_rms_x_%s.txt" % i, rms_x_array)
        np.savetxt("14208_betacampus_pos1_rms_y_%s.txt" % i, rms_y_array)
        np.savetxt("14208_betacampus_pos1_rms_z_%s.txt" % i, rms_z_array)

rms_x_all = np.zeros((len(f_band), 5))
rms_y_all = np.zeros((len(f_band), 5))
rms_z_all = np.zeros((len(f_band), 5))

rms_x_all[..., 1] = rms_x_array.min(axis = 1)
rms_x_all[..., 2] = rms_x_array.mean(axis = 1) - rms_x_array.std(axis = 1)
rms_x_all[..., 3] = rms_x_array.mean(axis = 1)
rms_x_all[..., 4] = rms_x_array.mean(axis = 1) + rms_x_array.std(axis = 1)
rms_x_all[..., 5] = rms_x_array.max(axis = 1)

rms_y_all[..., 1] = rms_y_array.min(axis = 1)
rms_y_all[..., 2] = rms_y_array.mean(axis = 1) - rms_y_array.std(axis = 1)
rms_y_all[..., 3] = rms_y_array.mean(axis = 1)
rms_y_all[..., 4] = rms_y_array.mean(axis = 1) + rms_y_array.std(axis = 1)
rms_y_all[..., 5] = rms_y_array.max(axis = 1)

rms_z_all[..., 1] = rms_z_array.min(axis = 1)
rms_z_all[..., 2] = rms_z_array.mean(axis = 1) - rms_z_array.std(axis = 1)
rms_z_all[..., 3] = rms_z_array.mean(axis = 1)
rms_z_all[..., 4] = rms_z_array.mean(axis = 1) + rms_z_array.std(axis = 1)
rms_z_all[..., 5] = rms_z_array.max(axis = 1)

np.savetxt("14208_betacampus_pos1_rms_x_all.txt", rms_x_all)
np.savetxt("14208_betacampus_pos1_rms_y_all.txt", rms_y_all)
np.savetxt("14208_betacampus_pos1_rms_z_all.txt", rms_z_all)

plt.subplot(3,1,1)
plt.plot(f_band, rms_x_all[..., 1], c = 'b', ls = 'dotted')
plt.plot(f_band, rms_x_all[..., 2], c = 'b', ls = 'dashed')
plt.plot(f_band, rms_x_all[..., 3], c = 'b', ls = 'solid')
plt.plot(f_band, rms_x_all[..., 4], c = 'b', ls = 'dashed')
plt.plot(f_band, rms_x_all[..., 5], c = 'b', ls = 'dotted')
plt.xscale('log')
plt.xlim([0.1, 100])
plt.yscale('log')
plt.grid(which = 'both')
plt.xlabel('1/3 octave band frequency [Hz]')
plt.ylabel('RMS of x-signal [mm/s]')
plt.subplot(3,1,2)
plt.plot(f_band, rms_y_all[..., 1], c = 'b', ls = 'dotted')
plt.plot(f_band, rms_y_all[..., 2], c = 'b', ls = 'dashed')
plt.plot(f_band, rms_y_all[..., 3], c = 'b', ls = 'solid')
plt.plot(f_band, rms_y_all[..., 4], c = 'b', ls = 'dashed')
plt.plot(f_band, rms_y_all[..., 5], c = 'b', ls = 'dotted')
plt.xscale('log')
plt.xlim([0.1, 100])
plt.yscale('log')
plt.grid(which = 'both')
plt.xlabel('1/3 octave band frequency [Hz]')
plt.ylabel('RMS of y-signal [mm/s]')
plt.subplot(3,1,3)
plt.plot(f_band, rms_z_all[..., 1], c = 'b', ls = 'dotted')
plt.plot(f_band, rms_z_all[..., 2], c = 'b', ls = 'dashed')
plt.plot(f_band, rms_z_all[..., 3], c = 'b', ls = 'solid')
plt.plot(f_band, rms_z_all[..., 4], c = 'b', ls = 'dashed')
plt.plot(f_band, rms_z_all[..., 5], c = 'b', ls = 'dotted')
plt.xscale('log')
plt.xlim([0.1, 100])
plt.yscale('log')
plt.grid(which = 'both')
plt.xlabel('1/3 octave band frequency [Hz]')
plt.ylabel('RMS of z-signal [mm/s]')
plt.plot()
plt.show()
