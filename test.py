import signal_processing as sp
import numpy as np

# dir_path = "C:\\Users\\mel\\Documents\\Python\\Betacampus_pos2\\"
# dir_path = "C:\\Users\\mel\\Documents\\Python\\Huygensgebouw\\"


# file_list = sp.obtain_files(dir_path)

# filename = dir_path + file_list[1357]

# print(filename)

# i_restart = 901
#
# print(len(file_list[i_restart:]))
#
# i_restart_array = np.arange(start = i_restart, stop = len(file_list), step = 1, dtype = "int")
# print(i_restart_array)

# data = np.loadtxt(filename, dtype = "float", comments = "#", unpack = True)

# data_max = np.loadtxt("14208_Huygensgebouw_min_max_900.txt")
#
# x_max = data_max[1, ...]
#
# print(x_max.shape)
#
# indices_nonzero = x_max.nonzero()
#
# print(data_max[1, ...].nonzero()[-1][-1])

freqband = sp.OneThird_octave(0.625 / 2**(1/3), 80 * 2**(1/3))
print(freqband)
print(freqband[-1])