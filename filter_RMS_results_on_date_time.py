import numpy as np
import signal_processing as sp
import numpy.ma as ma
import datetime as dt

"""
mel 2018-04-20
Translates RMS results for all files to minimum / mean / maximum and filters out zeros in the minimum.
Filters out only weekday results between 6:00 and 18:00 hours.
"""

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

f_band = sp.OneThird_octave(0.625 / 2**(1/3), 80 * 2**(1/3))

filter_weekday = np.ndarray((len(f_band), len(file_list)+1), dtype = 'bool')

filter_weekday[..., 0] = True

for i in range(len(file_list)):
    if (start_date[i].weekday() >= 0) and (start_date[i].weekday() <= 4):
        if (start_time[i].hour >= 6) and (start_time[i].hour <= 18):
            filter_weekday[..., i + 1] = False
        else:
            filter_weekday[..., i + 1] = True
    else:
        filter_weekday[..., i + 1] = True

# rms_x_array = np.loadtxt("14208_betacampus_pos1_rms_x_400.txt")
# rms_y_array = np.loadtxt("14208_betacampus_pos1_rms_y_400.txt")
# rms_z_array = np.loadtxt("14208_betacampus_pos1_rms_z_400.txt")

# rms_x_array = np.loadtxt("14208_betacampus_pos2_rms_x.txt")
# rms_y_array = np.loadtxt("14208_betacampus_pos2_rms_y.txt")
# rms_z_array = np.loadtxt("14208_betacampus_pos2_rms_z.txt")

rms_x_array = np.loadtxt("14208_Huygensgebouw_rms_x.txt")
rms_y_array = np.loadtxt("14208_Huygensgebouw_rms_y.txt")
rms_z_array = np.loadtxt("14208_Huygensgebouw_rms_z.txt")

rms_x_array = ma.array(rms_x_array, mask = filter_weekday)
rms_y_array = ma.array(rms_y_array, mask = filter_weekday)
rms_z_array = ma.array(rms_z_array, mask = filter_weekday)

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

# np.savetxt("14208_betacampus_pos1_rms_x_weekday.txt", rms_x_all)
# np.savetxt("14208_betacampus_pos1_rms_y_weekday.txt", rms_y_all)
# np.savetxt("14208_betacampus_pos1_rms_z_weekday.txt", rms_z_all)
# np.savetxt("14208_betacampus_pos2_rms_x_weekday.txt", rms_x_all)
# np.savetxt("14208_betacampus_pos2_rms_y_weekday.txt", rms_y_all)
# np.savetxt("14208_betacampus_pos2_rms_z_weekday.txt", rms_z_all)
np.savetxt("14208_Huygensgebouw_rms_x_weekday.txt", rms_x_all)
np.savetxt("14208_Huygensgebouw_rms_y_weekday.txt", rms_y_all)
np.savetxt("14208_Huygensgebouw_rms_z_weekday.txt", rms_z_all)
