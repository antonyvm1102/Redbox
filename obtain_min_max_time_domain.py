# import signal_processing as sp
from Redbox_v2 import file_manager as fm
import time
import datetime as dt
import numpy as np
from matplotlib.dates import drange, date2num
import sys

"""
Obtain min/max values per 5 minutes of signal in time domain.
"""

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * float(count) / float(total), 2)
    bar = '+' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s ...%s' % (bar, percents, '%', status))
    sys.stdout.flush()

stime = time.time()






# data_max = np.zeros((7, len(dates)))
# data_max[0, ...] = dates
#
# data_max = np.loadtxt("14208_Huygensgebouw_min_max_900.txt")
# i_restart = 901
# i_restart_array = np.arange(start = i_restart, stop = len(file_list), step = 1, dtype = "int")
#
# # index_data_max = np.argsort(data_max, axis=1)
# # print(index_data_max)
#
# count = data_max[1, ...].nonzero()[-1][-1] + 1
#
# for i in i_restart_array:       #range(len(file_list):
#     # print("i = %s" %i)
#     # print(file_list[i])
#     filename = dir_path + file_list[i]
#     data = np.loadtxt(filename, dtype = "float", comments = "#", unpack = True)
#     steps = np.arange(0, data.shape[1], sampling_rate * step_size)
#     # print(steps[-1])
#     # print(data.shape[1])
#     if data.shape[1] - steps[-1] > sampling_rate:
#         steps = np.append(steps, data.shape[1])
#     # print("steps = %s" %len(steps))
#     for j in range(len(steps)-1):
#         # print("count = %s" %count)
#         # print(data[1:, steps[j]:steps[j + 1]].max(axis=1).shape)
#         # print(data[1:, steps[j]:steps[j + 1]].max(axis=1))
#         # print(data_max[1:, count].shape)
#         # print(data_max[1:, count])
#         data_max[1:4, count] = data[1:, steps[j]:steps[j + 1]].max(axis=1)
#         data_max[4:, count] = data[1:, steps[j]:steps[j + 1]].min(axis=1)
#         count += 1
#     progress(i, len(file_list), "processing %s of %s" % (i, len(file_list)))
#     if i%100 == 0:
#         np.savetxt("14208_Huygensgebouw_min_max_%s.txt" % i, data_max)
#
# # print(data_max)
#
# # np.savetxt("14208_betacampus_pos1_min_max.txt", data_max)
# np.savetxt("14208_Huygensgebouw_min_max.txt", data_max)
#
# etime = time.time()
#
# dtime = etime - stime
# print("elapsed time = %s" %dtime)