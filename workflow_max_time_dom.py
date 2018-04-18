""""
workflow to  create a file with maximum values per n minutes for a certain signal

"""

import signal_processing as sp
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime
import sys


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * float(count) / float(total), 2)
    bar = '+' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s ...%s' % (bar, percents, '%', status))
    sys.stdout.flush()

start_time = time.time()
folder = r"P:\142\14208\Onderzoeksgegevens\Trillingen\Metingen VC vergelijking 1\Betacampus_pos2"
files = sp.obtain_files(folder)

max_vel_x = np.zeros(1)
max_vel_y = np.zeros(1)
max_vel_z = np.zeros(1)

n_max = 5 #in minutes
for n, f in enumerate(files):
    filename = folder + "\\" + f
    t,x,y,z = sp.obtain_data(filename)
    max_vel_x = np.append(max_vel_x, sp.n_minutes_max(x, n=n_max, dt=1. / 400))
    max_vel_y = np.append(max_vel_y, sp.n_minutes_max(y, n=n_max, dt=1. / 400))
    max_vel_z = np.append(max_vel_z, sp.n_minutes_max(z,n=n_max,dt=1./400))
    progress(n + 1, len(files), "processing %s of %s" % (n + 1, len(files)))

max_vel_x=np.delete(max_vel_x,0)
max_vel_y=np.delete(max_vel_y,0)
max_vel_z=np.delete(max_vel_z,0)

start = np.datetime64('2018-02-16T11:00:00')
end = start + np.timedelta64(n_max * 60//2 * len(max_vel_z),'s')
t = np.arange(start,end, dtype='datetime64[150s]')

np.savetxt(r"P:\142\14208\Onderzoeksgegevens\Trillingen\Metingen VC vergelijking 1\betacampus_pos2_speed.txt",
           (max_vel_x, max_vel_y, max_vel_z),
           delimiter=' ',
           newline='\n',
           header="x,y,z")
np.savetxt(r"P:\142\14208\Onderzoeksgegevens\Trillingen\Metingen VC vergelijking 1\betacampus_pos2_time.txt",
           t,
           fmt='%s',
           delimiter=' ',
           newline='\n',
           header="t")


end_time = time.time()
dtime = end_time-start_time
print("elapsed time = %s" %dtime)
