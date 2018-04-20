import numpy as np
import signal_processing as sp
import numpy.ma as ma

"""
mel 2018-04-20
Translates RMS results for all files to minimum / mean / maximum and filters out zeros in the minimum.
"""

rms_x_array = np.loadtxt("14208_Huygensgebouw_rms_x.txt")
rms_y_array = np.loadtxt("14208_Huygensgebouw_rms_y.txt")
rms_z_array = np.loadtxt("14208_Huygensgebouw_rms_z.txt")

f_band = sp.OneThird_octave(0.625 / 2**(1/3), 80 * 2**(1/3))

rms_x_all = np.zeros((len(f_band), 6))
rms_y_all = np.zeros((len(f_band), 6))
rms_z_all = np.zeros((len(f_band), 6))

rms_x_array_masked = ma.masked_less(rms_x_array, 1e-9)
rms_y_array_masked = ma.masked_less(rms_y_array, 1e-9)
rms_z_array_masked = ma.masked_less(rms_z_array, 1e-9)

rms_x_all[..., 0] = f_band
rms_x_all[..., 1] = rms_x_array_masked[..., 1:].min(axis = 1)
rms_x_all[..., 2] = rms_x_array[..., 1:].mean(axis = 1) - rms_x_array[..., 1:].std(axis = 1)
rms_x_all[..., 3] = rms_x_array[..., 1:].mean(axis = 1)
rms_x_all[..., 4] = rms_x_array[..., 1:].mean(axis = 1) + rms_x_array[..., 1:].std(axis = 1)
rms_x_all[..., 5] = rms_x_array[..., 1:].max(axis = 1)

rms_y_all[..., 0] = f_band
rms_y_all[..., 1] = rms_y_array_masked[..., 1:].min(axis = 1)
rms_y_all[..., 2] = rms_y_array[..., 1:].mean(axis = 1) - rms_y_array[..., 1:].std(axis = 1)
rms_y_all[..., 3] = rms_y_array[..., 1:].mean(axis = 1)
rms_y_all[..., 4] = rms_y_array[..., 1:].mean(axis = 1) + rms_y_array[..., 1:].std(axis = 1)
rms_y_all[..., 5] = rms_y_array[..., 1:].max(axis = 1)

rms_z_all[..., 0] = f_band
rms_z_all[..., 1] = rms_z_array_masked[..., 1:].min(axis = 1)
rms_z_all[..., 2] = rms_z_array[..., 1:].mean(axis = 1) - rms_z_array[..., 1:].std(axis = 1)
rms_z_all[..., 3] = rms_z_array[..., 1:].mean(axis = 1)
rms_z_all[..., 4] = rms_z_array[..., 1:].mean(axis = 1) + rms_z_array[..., 1:].std(axis = 1)
rms_z_all[..., 5] = rms_z_array[..., 1:].max(axis = 1)

np.savetxt("14208_Huygensgebouw_rms_x_all.txt", rms_x_all)
np.savetxt("14208_Huygensgebouw_rms_y_all.txt", rms_y_all)
np.savetxt("14208_Huygensgebouw_rms_z_all.txt", rms_z_all)