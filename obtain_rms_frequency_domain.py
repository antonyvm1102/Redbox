import signal_processing as sp
import numpy as np
import sys
import time

"""
Get RMS in frequency domain per 1/3 octave band for all signals and translate to min/mean/max per band.
TODO: add option to exclude zeros from the minimum as in 'capture_min_max_mean_stdev.py'.
"""

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

# dir_path = "C:\\Users\\mel\\Documents\\Python\\Betacampus_pos1\\"
# dir_path = "C:\\Users\\mel\\Documents\\Python\\Betacampus_pos2\\"
dir_path = "C:\\Users\\mel\\Documents\\Python\\Huygensgebouw\\"

file_list = sp.obtain_files(dir_path)

f_band = sp.OneThird_octave(0.625 / 2**(1/3), 80 * 2**(1/3))

rms_x_array = np.zeros((len(f_band), len(file_list)+1))
rms_y_array = np.zeros((len(f_band), len(file_list)+1))
rms_z_array = np.zeros((len(f_band), len(file_list)+1))

rms_x_array[... , 0] = f_band
rms_y_array[... , 0] = f_band
rms_z_array[... , 0] = f_band

for i in range(len(file_list)):
    filename = dir_path + file_list[i]
    t,x,y,z = np.loadtxt(filename, dtype="float", comments="#", unpack=True)
    n = largest_power_of_base(len(t))
    xf, f = sp.FFT(x[:n], dT=t[1] - t[0])
    yf = sp.FFT_amplitude(y[:n])
    zf = sp.FFT_amplitude(z[:n])
    rms_x_array[..., i + 1] = sp.FFT_to_OneThird_Octave2(xf, f[1] - f[0], f_band)
    rms_y_array[..., i + 1] = sp.FFT_to_OneThird_Octave2(yf, f[1] - f[0], f_band)
    rms_z_array[..., i + 1] = sp.FFT_to_OneThird_Octave2(zf, f[1] - f[0], f_band)
    progress(i, len(file_list), "processing %s of %s" % (i, len(file_list)))
    if i%100 == 0:
        # np.savetxt("14208_betacampus_pos1_rms_x_%s.txt" % i, rms_x_array)
        # np.savetxt("14208_betacampus_pos1_rms_y_%s.txt" % i, rms_y_array)
        # np.savetxt("14208_betacampus_pos1_rms_z_%s.txt" % i, rms_z_array)
        # np.savetxt("14208_betacampus_pos2_rms_x_%s.txt" % i, rms_x_array)
        # np.savetxt("14208_betacampus_pos2_rms_y_%s.txt" % i, rms_y_array)
        # np.savetxt("14208_betacampus_pos2_rms_z_%s.txt" % i, rms_z_array)
        np.savetxt("14208_Huygensgebouw_rms_x_%s.txt" % i, rms_x_array)
        np.savetxt("14208_Huygensgebouw_rms_y_%s.txt" % i, rms_y_array)
        np.savetxt("14208_Huygensgebouw_rms_z_%s.txt" % i, rms_z_array)

# np.savetxt("14208_betacampus_pos1_rms_x.txt", rms_x_array)
# np.savetxt("14208_betacampus_pos1_rms_y.txt", rms_y_array)
# np.savetxt("14208_betacampus_pos1_rms_z.txt", rms_z_array)
# np.savetxt("14208_betacampus_pos2_rms_x.txt", rms_x_array)
# np.savetxt("14208_betacampus_pos2_rms_y.txt", rms_y_array)
# np.savetxt("14208_betacampus_pos2_rms_z.txt", rms_z_array)
np.savetxt("14208_Huygensgebouw_rms_x.txt", rms_x_array)
np.savetxt("14208_Huygensgebouw_rms_y.txt", rms_y_array)
np.savetxt("14208_Huygensgebouw_rms_z.txt", rms_z_array)

rms_x_all = np.zeros((len(f_band), 6))
rms_y_all = np.zeros((len(f_band), 6))
rms_z_all = np.zeros((len(f_band), 6))

rms_x_all[..., 0] = f_band
rms_x_all[..., 1] = rms_x_array[..., 1:].min(axis = 1)
rms_x_all[..., 2] = rms_x_array[..., 1:].mean(axis = 1) - rms_x_array[..., 1:].std(axis = 1)
rms_x_all[..., 3] = rms_x_array[..., 1:].mean(axis = 1)
rms_x_all[..., 4] = rms_x_array[..., 1:].mean(axis = 1) + rms_x_array[..., 1:].std(axis = 1)
rms_x_all[..., 5] = rms_x_array[..., 1:].max(axis = 1)

rms_y_all[..., 0] = f_band
rms_y_all[..., 1] = rms_y_array[..., 1:].min(axis = 1)
rms_y_all[..., 2] = rms_y_array[..., 1:].mean(axis = 1) - rms_y_array[..., 1:].std(axis = 1)
rms_y_all[..., 3] = rms_y_array[..., 1:].mean(axis = 1)
rms_y_all[..., 4] = rms_y_array[..., 1:].mean(axis = 1) + rms_y_array[..., 1:].std(axis = 1)
rms_y_all[..., 5] = rms_y_array[..., 1:].max(axis = 1)

rms_z_all[..., 0] = f_band
rms_z_all[..., 1] = rms_z_array[..., 1:].min(axis = 1)
rms_z_all[..., 2] = rms_z_array[..., 1:].mean(axis = 1) - rms_z_array[..., 1:].std(axis = 1)
rms_z_all[..., 3] = rms_z_array[..., 1:].mean(axis = 1)
rms_z_all[..., 4] = rms_z_array[..., 1:].mean(axis = 1) + rms_z_array[..., 1:].std(axis = 1)
rms_z_all[..., 5] = rms_z_array[..., 1:].max(axis = 1)

# np.savetxt("14208_betacampus_pos1_rms_x_all.txt", rms_x_all)
# np.savetxt("14208_betacampus_pos1_rms_y_all.txt", rms_y_all)
# np.savetxt("14208_betacampus_pos1_rms_z_all.txt", rms_z_all)
# np.savetxt("14208_betacampus_pos2_rms_x_all.txt", rms_x_all)
# np.savetxt("14208_betacampus_pos2_rms_y_all.txt", rms_y_all)
# np.savetxt("14208_betacampus_pos2_rms_z_all.txt", rms_z_all)
np.savetxt("14208_Huygensgebouw_rms_x_all.txt", rms_x_all)
np.savetxt("14208_Huygensgebouw_rms_y_all.txt", rms_y_all)
np.savetxt("14208_Huygensgebouw_rms_z_all.txt", rms_z_all)

etime = time.time()

dtime = etime - stime
print("elapsed time = %s" %dtime)


