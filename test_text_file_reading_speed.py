import signal_processing as sp
import time
import datetime as dt
import numpy as np
from matplotlib.dates import drange, date2num
import sys

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * float(count) / float(total), 2)
    bar = '+' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s ...%s' % (bar, percents, '%', status))
    sys.stdout.flush()

stime = time.time()

sampling_rate = 400     #sampling rate in number of samples per second
step_size = 300         #step size in seconds for which maximum value is determined

# dir_path = "P:\\142\\14208\\Onderzoeksgegevens\\Trillingen\\Metingen VC vergelijking 1\\Betacampus_pos1\\"
# dir_path = "C:\\Users\\mel\\Documents\\Python\\Betacampus_pos1\\"
# dir_path = "C:\\Users\\mel\\Documents\\Python\\Betacampus_pos2\\"
dir_path = "C:\\Users\\mel\\Documents\\Python\\Huygensgebouw\\"

file_list = sp.obtain_files(dir_path)
start_date = []
start_time = []
time_length = []
total_time_start = []
total_time_end = []
total = None
date = None
time_of_day = None

for i in range(len(file_list)):
    file_path = dir_path + file_list[i]
    # print(file_list[i])
    with open(file_path, encoding='latin-1') as f:
       for cnt, line in enumerate(f):
           if line.startswith('# StartDate'):
               year = int(line[12:16])
               month = int(line[17:19])
               day = int(line[20:22])
               date = dt.date(year = year, month = month, day = day)
               total = dt.datetime(year = year, month = month, day = day)
               start_date.append(date)
           elif line.startswith('# StartTime'):
               hour = int(line[12:14])
               minutes = int(line[15:17])
               seconds = int(line[18:20])
               time_of_day = dt.time(hour = hour, minute = minutes, second = seconds)
               total = total+ dt.timedelta(hours = hour, minutes = minutes, seconds = seconds)
               start_time.append(time_of_day)
           elif line.startswith('# Length'):
               hour = int(line[9:11])
               minutes = int(line[12:14])
               seconds = int(line[15:17])
               dtime = dt.time(hour = hour, minute= minutes, second = seconds)
               time_length.append(dtime)
               total_time_start.append(total)
               total = total + dt.timedelta(hours = hour, minutes = minutes, seconds = seconds)
               total_time_end.append(total)
               break
    # print(str(time_length[i]))

dates = date2num(total_time_start[0])
for i in range(len(file_list)):
    dates = np.append(dates, drange(total_time_start[i], total_time_end[i], dt.timedelta(seconds=step_size)))
dates = np.delete(dates, [0])

# print(dates.shape)
# print(dates)

# data_max = np.zeros((7, len(dates)))
# data_max[0, ...] = dates
data_max = np.loadtxt("14208_Huygensgebouw_min_max_900.txt")
i_restart = 901
i_restart_array = np.arange(start = i_restart, stop = len(file_list), step = 1, dtype = "int")

# index_data_max = np.argsort(data_max, axis=1)
# print(index_data_max)

count = data_max[1, ...].nonzero()[-1][-1] + 1

for i in i_restart_array:       #range(len(file_list):
    # print("i = %s" %i)
    # print(file_list[i])
    filename = dir_path + file_list[i]
    data = np.loadtxt(filename, dtype = "float", comments = "#", unpack = True)
    steps = np.arange(0, data.shape[1], sampling_rate * step_size)
    # print(steps[-1])
    # print(data.shape[1])
    if data.shape[1] - steps[-1] > sampling_rate:
        steps = np.append(steps, data.shape[1])
    # print("steps = %s" %len(steps))
    for j in range(len(steps)-1):
        # print("count = %s" %count)
        # print(data[1:, steps[j]:steps[j + 1]].max(axis=1).shape)
        # print(data[1:, steps[j]:steps[j + 1]].max(axis=1))
        # print(data_max[1:, count].shape)
        # print(data_max[1:, count])
        data_max[1:4, count] = data[1:, steps[j]:steps[j + 1]].max(axis=1)
        data_max[4:, count] = data[1:, steps[j]:steps[j + 1]].min(axis=1)
        count += 1
    progress(i, len(file_list), "processing %s of %s" % (i, len(file_list)))
    if i%100 == 0:
        np.savetxt("14208_Huygensgebouw_min_max_%s.txt" % i, data_max)

# print(data_max)

# np.savetxt("14208_betacampus_pos1_min_max.txt", data_max)
np.savetxt("14208_Huygensgebouw_min_max.txt", data_max)

etime = time.time()

dtime = etime - stime
print("elapsed time = %s" %dtime)