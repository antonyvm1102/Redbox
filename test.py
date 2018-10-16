import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange,
                              DayLocator, num2date,date2num)
import numpy as np
import datetime

# Fixing random state for reproducibility
np.random.seed(19680801)


# tick every 5th easter
# rule = rrulewrapper(YEARLY, byeaster=1, interval=5)
loc = DayLocator(interval=28)
formatter = DateFormatter('%m/%d/%y')
date1 = datetime.datetime(2003, 1, 1,4)
date2 = datetime.datetime(2004, 4, 12,8)
delta = datetime.timedelta(hours=4)


dates = drange(date1, date2, delta)
s = np.random.rand(len(dates))  # make up some random y values

date = datetime.datetime(2018, 4, 11, 17,35,51)
date = datetime.datetime.strptime("11-4-2018 17:35:01",'%d-%m-%Y %H:%M:%S')
print("11-4-2018 17:35:01")
print(date)

#
# fig, ax = plt.subplots()
# plt.plot_date(dates, s)
# ax.xaxis.set_major_locator(loc)
# ax.xaxis.set_major_formatter(formatter)
# ax.xaxis.set_tick_params(rotation=30, labelsize=10)
#
# plt.show()