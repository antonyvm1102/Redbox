import signal_processing as sp
from datetime import datetime, timedelta
import numpy as np
from matplotlib.dates import drange

file_list = sp.obtain_files(r"P:\142\14208\Onderzoeksgegevens\Trillingen\Metingen VC vergelijking 1\Betacampus_pos1")

start_times = []

for i in range(len(file_list)):
    year = int(file_list[i][0:4])
    month = int(file_list[i][4:6])
    day = int(file_list[i][6:8])
    hour = int(file_list[i][8:10])
    minute = int(file_list[i][10:12])
    sec = int(file_list[i][12:14])
    start_times.append(datetime(year, month, day, hour, minute, sec))

t = np.zeros(1)
for i in range(len(start_times)):
    t= np.append(t, drange(start_times[i],start_times[i]+timedelta(minutes=30),timedelta(seconds = 150)))

print(t)

# for i in range(len(file_list)):
#     file_list[i] = file_list[i].replace(".txt","")
#     file_list[i] = int(file_list[i])


