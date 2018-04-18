from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, date2num
import matplotlib.pyplot as plt
import numpy as np

# data = np.loadtxt("14208_betacampus_pos2_min_max.txt")
data = np.loadtxt("14208_Huygensgebouw_min_max_900.txt")

dates = data[0, ...]
x_max = data[1, ...]
y_max = data[2, ...]
z_max = data[3, ...]
x_min = data[4, ...]
y_min = data[5, ...]
z_min = data[6, ...]

fig = plt.figure()
ax1= fig.add_subplot(3,1,1)
ax1.plot_date(dates,x_max, 'ro', markersize = 2)
ax1.plot_date(dates,x_min, 'ro', markersize = 2)
ax1.xaxis.set_major_locator(DayLocator())
ax1.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax1.set_title('velocity x_axis')
ax1.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')

ax2= fig.add_subplot(3,1,2)
ax2.plot_date(dates,y_max, 'bo', markersize = 2)
ax2.plot_date(dates,y_min, 'bo', markersize = 2)
ax2.xaxis.set_major_locator(DayLocator())
ax2.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
ax2.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax2.set_title('velocity y_axis')
ax2.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')

ax3= fig.add_subplot(3,1,3)
ax3.plot_date(dates,z_max, 'go', markersize = 2)
ax3.plot_date(dates,z_min, 'go', markersize = 2)
ax3.xaxis.set_major_locator(DayLocator())
ax3.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
ax3.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax3.set_title('velocity z_axis')
ax3.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')

fig.autofmt_xdate()

plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.9)
plt.show()