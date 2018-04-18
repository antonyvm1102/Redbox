import signal_processing as sp
import time
import datetime as dt

stime = time.time()

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

etime = time.time()
dtime = etime - stime
print("elapsed time = %s" %dtime)
print(str(start_date))
print(str(start_time))
print(str(time_length))
print(str(total_time_start))
print(str(total_time_end))