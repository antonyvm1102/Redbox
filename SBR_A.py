import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, date2num, AutoDateLocator,num2date
import signal_processing as sp
import file_manager as fm

# karakteristieke grenswaarden SBR-A curves [mm/s]
f = np.arange(0,101,5)
cat1 = np.array([20,20,20,22.5,25,27.5,30,32.5,35,37.5,40,41,42,43,44,45,46,47,48,49,50])
cat2 = np.array([5,5,5,6.25,7.5,8.75,10,11.25,12.5,13.75,15.,15.5,16,16.5,17.,17.5,18,18.5,19.,19.5,20.])
cat3 = np.array([3.,3.,3.,3.63,4.25,4.88,5.5,6.13,6.75,7.38,8,8.2,8.4,8.6,8.8,9,9.2,9.4,9.6,9.8,10.])
fund = 1000/(2*np.pi*f)
welded_pipe = np.full((21,), 100)
concrete_pipe = np.full((21,), 80)
masonry_pipe = np.full((21,), 50)

# rekenwaarde van grenswaarde

def part_safety_factor(type):
    if type == 'kortdurend':
        return 1.0
    elif type == 'herhaald kortdurend':
        return 1.5
    elif type == 'continu':
        return 2.5
    else:
        print('insert one of following types: kortdurend, herhaald kortdurend, continu')

cat1_r = cat1/part_safety_factor('herhaald kortdurend')
cat2_r = cat2/part_safety_factor('herhaald kortdurend')
cat3_r = cat3/part_safety_factor('herhaald kortdurend')
fund_r = fund/part_safety_factor('herhaald kortdurend')
welded_pipe_r = welded_pipe/part_safety_factor('herhaald kortdurend')
concrete_pipe_r = concrete_pipe/part_safety_factor('herhaald kortdurend')
masonry_pipe_r = masonry_pipe/part_safety_factor('herhaald kortdurend')


# Vtop, Vstat, Vd and dominant frequency

def find_vtop_i(vel, freq):
    ar = np.argsort(vel)
    Vtopi = vel[ar[ar.shape[0]-15:]]
    freqtopi = freq[ar[ar.shape[0]-15:]]
    return Vtopi, freqtopi

def Vstat(Vtopi):
    mean = np.mean(Vtopi)
    std = np.std(Vtopi)
    return mean * np.exp(2.62 * (std/mean))

def Vd(Vstat, type='beperkt'):
    if type == 'indicatief':
        return Vstat * 1.6
    elif type == 'beperkt':
        return Vstat * 1.4
    elif type == 'uitgebreid':
        return Vstat * 1
    else:
        print('insert one of following types: indicatief, beperkt, uitgebreid')
        return

def dominant_freq(Vn, fn, category='cat2'):
    vf = np.amax(Vn)
    ff = fn[np.argmax(Vn)]
    vgf = None
    vgn = np.zeros(fn.shape[0])
    if category == 'cat1':
        vgf = cat1_r[(np.abs(f - ff)).argmin()]
        for cnt, i in enumerate(vgn):
            vgn[cnt] = cat1_r[(np.abs(f - fn[cnt])).argmin()]
    elif category == 'cat2':
        vgf = cat2_r[(np.abs(f - ff)).argmin()]
        for cnt, i in enumerate(vgn):
            vgn[cnt] = cat2_r[(np.abs(f - fn[cnt])).argmin()]
    elif category == 'cat3':
        vgf = cat3_r[(np.abs(f - ff)).argmin()]
        for cnt, i in enumerate(vgn):
            vgn[cnt] = cat3_r[(np.abs(f - fn[cnt])).argmin()]
    return fn[np.multiply((vf / Vn), (vgn / vgf)).argmin()]


# workflow
result_file = "floor_apartment"
filename = r"P:\158\15836\07_Onderzoeksgegevens\trillingsmeting\CR016 185718 Arnhem - Ernst Casimirlaan vloer kelder\CR016 185718 Arnhem - Ernst Casimirlaan.txt"

## obtain data from all files Redbox

folder = r"P:\158\15836\07_Onderzoeksgegevens\trillingsmeting\SYSCOM vloer appartement\download(9)\background\Save\2018-05"
files = fm.obtain_files(folder)

data_tot = None

for cnt, file in enumerate(files):
    data = fm.obtain_SBR_data(folder + '\\' + file)
    # data contains: t, peak_x, peak_ y, peak_z, f_x, f_y, f_z per file
    if data_tot is None:
        data_tot = data
    else:
        for i, var in enumerate(data):
            data_tot[i] = np.concatenate((data_tot[i], data[i]))

"""
## obtain data from CR-file

data_tot =[]
time = []
t, vx, fx, vy, fy, vz, fz = np.genfromtxt(filename, dtype='str', delimiter='\t', skip_header=1, unpack=True)

for element, i in enumerate(t):
    time.append(i)

t = [dt.strptime(x, '%d-%m-%Y %H:%M:%S') for x in time]

data_tot.append(t)

lst = [vx, vy, vz, fx, fy, fz]

for i in lst:
    i = np.char.replace(i, ',', '.')
    data_tot.append(i.astype(np.float))
"""
## total data

t = data_tot[0]
peak_x = data_tot[1]
peak_y = data_tot[2]
peak_z = data_tot[3]
f_x = data_tot[4]
f_y = data_tot[5]
f_z = data_tot[6]

"""
## Statistical evaluation

Vtopix, ftopix = find_vtop_i(peak_x, f_x)
Vtopiy, ftopiy = find_vtop_i(peak_y, f_y)
Vtopiz, ftopiz = find_vtop_i(peak_z, f_z)


Vstatx, Vstaty, Vstatz = Vstat(Vtopix), Vstat(Vtopiy), Vstat(Vtopiz)
Vdx, Vdy, Vdz = Vd(Vstatx), Vd(Vstaty), Vd(Vstatz)

fdomx = dominant_freq(Vtopix, ftopix)
fdomy = dominant_freq(Vtopiy, ftopiy)
fdomz = dominant_freq(Vtopiz, ftopiz)

## saving data

np.savetxt(result_file+'_results.txt', (Vtopix, Vtopiy, Vtopiz, ftopix, ftopiy, ftopiz),
           header='results of %s \n'
                  'Vstatx = %s [mm/s] \n Vstaty = %s [mm/s] \n Vstatz = %s [mm/s] \n '
                  'Vdx = %s [mm/s] \n Vdy = %s [mm/s] \n Vdz = %s [mm/s] \n'
                  ' fdomx = %s [Hz] \n fdomy = %s [Hz] \n fdomz = %s  [Hz] \n'
                  '0= Vtopix \n'
                  '1= Vtopiy \n'
                  '2= Vtopiz \n'
                  '3= ftopix \n'
                  '4= ftopiy \n'
                  '5= ftopiz \n'
                  % (result_file, Vstatx, Vstaty, Vstatz, Vdx, Vdy, Vdz, fdomx, fdomy, fdomz))
"""
## Plotting

#plotting raw data

fig = plt.figure() #A4 size: figsize=(8.27, 11.69/2)

ax1 = fig.add_subplot(1, 1, 1)
ax1.plot_date(t, peak_x, 'g', label="peak_x")
ax1.plot_date(t, peak_y, 'b', label="peak_y")
ax1.plot_date(t, peak_z, 'r', label="peak_z")
ax1.xaxis.set_major_locator(DayLocator())
ax1.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax1.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
ax1.set_ylim(bottom=0.0, top = 10.0)

ax1.set_xlabel('date', fontsize=7)
ax1.set_ylabel('peak velocity [mm/s]', fontsize=7)
ax1.set_title('results raw data floor apartment', fontsize=10)
ax1.legend(bbox_to_anchor=(0.5, 0.75))

fig.autofmt_xdate()

#plt.subplots_adjust(top=0.95, bottom=0.15, left=0.15, right=0.95, hspace=0.2)
plt.savefig(result_file + "_rawdata.png")
plt.show()

""""
# plotting geanalyseerde data

fig = plt.figure(figsize=(8.27, 11.69)) #A4 size

ax1 = fig.add_subplot(3, 1, 1)
ax1.plot(f, cat1_r, 'g', label="cat 1")
ax1.plot(f, cat2_r, 'b', label="cat 2")
ax1.plot(f, cat3_r, 'r', label="cat 3")
# ax1.plot(f, fund, 'grey', label="fund")
ax1.plot(f, welded_pipe_r, 'grey', label="welded pipe_r")
ax1.scatter(f_z,peak_z, s=0.75, c='orange')
ax1.plot(fdomx, Vdx, 'r*',label="Vdx")
ax1.axes.set_xlim([0, 100])
ax1.axes.set_ylim([0, 105/1.5])
ax1.set_xlabel('freq [Hz]', fontsize=7)
ax1.set_ylabel('peak velocity [mm/s]', fontsize=7)
ax1.set_title('Measurement results x-direction', fontsize=10)
ax1.legend(bbox_to_anchor=(-0.09,0.75))

ax2 = fig.add_subplot(3, 1, 2)
ax2.plot(f, cat1_r, 'g', label="cat 1")
ax2.plot(f, cat2_r, 'b', label="cat 2")
ax2.plot(f, cat3_r, 'r', label="cat 3")
# ax2.plot(f, fund, 'grey', label="fund")
ax2.plot(f, welded_pipe_r, 'grey', label="welded pipe_r")
ax2.scatter(f_z, peak_z, s=0.75, c='orange')
ax2.plot(fdomy, Vdy, 'r*', label="Vdy")
ax2.axes.set_xlim([0, 100])
ax2.axes.set_ylim([0, 105/1.5])
ax2.set_xlabel('freq [Hz]', fontsize=7)
ax2.set_ylabel('peak velocity [mm/s]', fontsize=7)
ax2.set_title('Measurement results y-direction', fontsize=10)
ax2.legend(bbox_to_anchor=(-0.09,0.75))

ax3 = fig.add_subplot(3, 1, 3)
ax3.plot(f, cat1_r, 'g', label="cat 1")
ax3.plot(f, cat2_r, 'b', label="cat 2")
ax3.plot(f, cat3_r, 'r', label="cat 3")
# ax3.plot(f, fund, 'grey', label="fund")
ax3.plot(f, welded_pipe_r, 'grey', label="welded pipe_r")
ax3.scatter(f_z, peak_z, s=0.75, c='orange')
ax3.plot(fdomz, Vdz, 'r*', label="Vdz")
ax3.axes.set_xlim([0, 100])
ax3.axes.set_ylim([0, 105/1.5])
ax3.set_xlabel('freq [Hz]', fontsize=7)
ax3.set_ylabel('peak velocity [mm/s]', fontsize=7)
ax3.set_title('Measurement results z-direction',fontsize=10)
ax3.legend(bbox_to_anchor=(-0.09, 0.75))

plt.suptitle('SBR-A measurement at ' + result_file, fontsize=16)
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.3, right=0.9, hspace=0.35)

plt.savefig(result_file + "_graph.png")
plt.show()
"""
