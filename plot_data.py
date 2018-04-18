import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, date2num
# from datetime import datetime, timedelta
import signal_processing as sp
import datetime as dt

speed_file = r"P:\142\14208\Onderzoeksgegevens\Trillingen\Metingen VC vergelijking 1\betacampus_pos1_speed.txt"
# time_file = r"P:\142\14208\Onderzoeksgegevens\Trillingen\Metingen VC vergelijking 1\betacampus_pos1_time.txt"

x,y,z = np.loadtxt(speed_file)

# file_list = sp.obtain_files(r"P:\142\14208\Onderzoeksgegevens\Trillingen\Metingen VC vergelijking 1\Betacampus_pos1")

# start_times = []
#
# for i in range(len(file_list)):
#     year = int(file_list[i][0:4])
#     month = int(file_list[i][4:6])
#     day = int(file_list[i][6:8])
#     hour = int(file_list[i][8:10])
#     minute = int(file_list[i][10:12])
#     sec = int(file_list[i][12:14])
#     start_times.append(datetime(year, month, day, hour, minute, sec))

dir_path = "P:\\142\\14208\\Onderzoeksgegevens\\Trillingen\\Metingen VC vergelijking 1\\Betacampus_pos1\\"

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

dates = date2num(total_time_start[0])
for i in range(len(file_list)):
    dates = np.append(dates, drange(total_time_start[i], total_time_end[i], dt.timedelta(seconds=150)))
    np.delete(dates,0)

print(dates[0:99])
print(dates[100:199])
print(dates[200:299])
print(dates[300:399])
print(dates[400:])

fig = plt.figure()
ax1= fig.add_subplot(3,1,1)
ax1.plot_date(dates,x[8:], 'r-')
ax1.xaxis.set_major_locator(DayLocator())
ax1.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax1.set_title('velocity x_axis')
ax1.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')

ax2= fig.add_subplot(3,1,2)
ax2.plot_date(dates,y[8:], 'b-')
ax2.xaxis.set_major_locator(DayLocator())
ax2.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
ax2.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax2.set_title('velocity y_axis')
ax2.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')

ax3= fig.add_subplot(3,1,3)
ax3.plot_date(dates,z[8:], 'g-')
ax3.xaxis.set_major_locator(DayLocator())
ax3.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
ax3.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax3.set_title('velocity z_axis')
ax3.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')

fig.autofmt_xdate()

plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.9)
plt.show()


