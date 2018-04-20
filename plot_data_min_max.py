from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, date2num
import matplotlib.pyplot as plt
import numpy as np

"""
Plot 5 minutes min/max values for Betacampus pos1/2 vs Huygensgebouw.
"""

data_Huygens = np.loadtxt("14208_Huygensgebouw_min_max.txt")
data_pos1 = np.loadtxt("14208_betacampus_pos1_min_max.txt")
data_pos2 = np.loadtxt("14208_betacampus_pos2_min_max.txt")

dates_Huygens = data_Huygens[0, ...]
x_max_Huygens = data_Huygens[1, ...]
y_max_Huygens = data_Huygens[2, ...]
z_max_Huygens = data_Huygens[3, ...]
x_min_Huygens = data_Huygens[4, ...]
y_min_Huygens = data_Huygens[5, ...]
z_min_Huygens = data_Huygens[6, ...]

dates_pos1 = data_pos1[0, ...]
x_max_pos1 = data_pos1[1, ...]
y_max_pos1 = data_pos1[2, ...]
z_max_pos1 = data_pos1[3, ...]
x_min_pos1 = data_pos1[4, ...]
y_min_pos1 = data_pos1[5, ...]
z_min_pos1 = data_pos1[6, ...]

dates_pos2 = data_pos2[0, ...]
x_max_pos2 = data_pos2[1, ...]
y_max_pos2 = data_pos2[2, ...]
z_max_pos2 = data_pos2[3, ...]
x_min_pos2 = data_pos2[4, ...]
y_min_pos2 = data_pos2[5, ...]
z_min_pos2 = data_pos2[6, ...]

fig = plt.figure()
ax1= fig.add_subplot(3,1,1)
ax1.plot_date(dates_pos1,x_max_pos1, 'bo', markersize = 2, label = "Betacampus positie 1")
ax1.plot_date(dates_pos1,x_min_pos1, 'bo', markersize = 2)
ax1.plot_date(dates_pos2,x_max_pos2, 'go', markersize = 2, label = "Betacampus positie 2")
ax1.plot_date(dates_pos2,x_min_pos2, 'go', markersize = 2)
ax1.plot_date(dates_Huygens,x_max_Huygens, 'ro', markersize = 2, label = "Huygens gebouw")
ax1.plot_date(dates_Huygens,x_min_Huygens, 'ro', markersize = 2)
ax1.xaxis.set_major_locator(DayLocator())
ax1.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax1.set_ylim(bottom = -0.2, top = 0.2)
ax1.set_title('velocity x_axis - min/max per 5 minutes [mm/s]')
ax1.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
ax1.legend(bbox_to_anchor=(-0.05,-0.5))

ax2= fig.add_subplot(3,1,2)
ax2.plot_date(dates_pos1,y_max_pos1, 'bo', markersize = 2)
ax2.plot_date(dates_pos1,y_min_pos1, 'bo', markersize = 2)
ax2.plot_date(dates_pos2,y_max_pos2, 'go', markersize = 2)
ax2.plot_date(dates_pos2,y_min_pos2, 'go', markersize = 2)
ax2.plot_date(dates_Huygens,y_max_Huygens, 'ro', markersize = 2)
ax2.plot_date(dates_Huygens,y_min_Huygens, 'ro', markersize = 2)
ax2.xaxis.set_major_locator(DayLocator())
ax2.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
ax2.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax2.set_ylim(bottom = -0.2, top = 0.2)
ax2.set_title('velocity y_axis - min/max per 5 minutes [mm/s]')
ax2.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')

ax3= fig.add_subplot(3,1,3)
ax3.plot_date(dates_pos1,z_max_pos1, 'bo', markersize = 2)
ax3.plot_date(dates_pos1,z_min_pos1, 'bo', markersize = 2)
ax3.plot_date(dates_pos2,z_max_pos2, 'go', markersize = 2)
ax3.plot_date(dates_pos2,z_min_pos2, 'go', markersize = 2)
ax3.plot_date(dates_Huygens,z_max_Huygens, 'ro', markersize = 2)
ax3.plot_date(dates_Huygens,z_min_Huygens, 'ro', markersize = 2)
ax3.xaxis.set_major_locator(DayLocator())
ax3.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
ax3.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax3.set_ylim(bottom = -0.5, top = 0.5)
ax3.set_title('velocity z_axis - min/max per 5 minutes [mm/s]')
ax3.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')

fig.autofmt_xdate()

plt.subplots_adjust(top=0.95, bottom=0.15, left=0.15, right=0.95, hspace=0.2)
plt.show()