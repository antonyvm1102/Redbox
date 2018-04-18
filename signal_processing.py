import numpy as np
from scipy.fftpack import rfft, rfftfreq
import matplotlib.pyplot as plt
import os
import math

def obtain_files(folder_path):
    """"
    returns all items in a certain folder
    :param folder_path: [path]
    """
    return os.listdir(folder_path)

def obtain_data(filename):
    """
    extract relevant data from txt file produced by the logger
    :param filename : (raw string)
    :return (tpl) (velocity x-direction, velocity y-direction, velocity z-direction)
    """
    with open(filename, encoding='latin-1') as f:
        lines = f.readlines()
        skip = 0
        i = 0
        while lines[i].startswith('#'):
            skip += 1
            i +=1
        t, x, y, z = np.loadtxt(filename, skiprows=skip ,unpack=True)
    return t,x,y,z

def rms_time_dom(signal):
    N = len(signal)
    return math.sqrt(np.sum(np.power(signal,2))/N)

def rms_freq_dom(amplitude):
    return math.sqrt(2*np.sum(np.power(amplitude, 2)))/2

def n_minutes_max(signal, dt, n=5):
    """"
    :param signal (np.array or list)
    :param n: n-minutes range to obtain maximum (int)
    :param dt: sample space or time between samples

    return: numpy array with
    """

    maximums = np.zeros(1)
    samples = int((n*60)/dt)
    start = 0
    end = samples
    while start < len(signal):
        selection = signal[start:end]
        maximums = np.append(maximums, [np.amax(selection),np.amin(selection)])
        start = end
        end = min(len(signal), start + samples)
    maximums = np.delete(maximums,0)
    return maximums

def FFT(signal,dT):
    """
    :param signal: [array]
    :param dT: sample space [float]
    """
    ampl = np.abs(rfft(signal)) * 2.0 / len(signal)
    freq = rfftfreq(len(ampl),d=dT)
    return ampl, freq

def OneThird_octave(low, high):
    """"
    :param low: lowest required frequency band
    :param high: highest required frequency band

    this function starts at the highest band and
    """
    one_third_octave = 2**(1/3)
    last_band = high
    first_band = last_band
    N = 0

    while first_band > low:
        first_band = first_band/one_third_octave
        N += 1
    first_band = first_band * one_third_octave
    return first_band * np.logspace(0, N, endpoint=False, num=N, base=one_third_octave)

def FFT_to_OneThird_Octave(amplitude, df, low, high):
    """
    :param amplitude: amplitudes of the FFT [array]
    :param frequency: frequencies of the FFT [array]

    """

    one_third_octave = 2 ** (1 / 3)
    spectrum = OneThird_octave(low, high)
    rms_amplitude = np.empty(len(spectrum))

    #check if the maximum available frequency exceeds the upper bound
    if (df*len(amplitude))*one_third_octave**0.5 > high:
        lower_bound = spectrum[0] / one_third_octave ** 0.5
        upper_bound = spectrum[0] * one_third_octave ** 0.5
        for n in range(rms_amplitude.size):
            rms_amplitude[n] = rms_freq_dom(amplitude[int(lower_bound // df):int(upper_bound // df)])
            lower_bound = lower_bound * one_third_octave
            upper_bound = upper_bound * one_third_octave
        return rms_amplitude, spectrum
    else:
        print("ERROR frequency range is not large enough")
        return

def integ_to_disp(vel,dt):
    """
    :param vel: velocity obtained from data (np.array)
    :return: (np.array) (displacement)
    """
    disp = np.zeros(len(vel))
    disp = disp[:-1]

    for i in range(1, len(disp)):
        disp[i] = disp[i - 1] + (vel[i + 1] - vel[i]) * dt
    return disp

def diff_to_acc(vel,dt):
    """
    :param vel: velocity obtained from data(lst)
    :return: (tpl) (acceleration)
    """

    acc = np.zeros(len(vel))
    acc = acc[:-1]

    for i in range(0, len(acc)):
        acc[i] = (vel[i + 1] - vel[i]) / dt

    return acc

def select_part(start, stop, to_select):
    """
        :param start: start of selection(flt/int)
        :param stop: end time of selection (flt/int)
        :return: (tpl) (displacement u, velocity v)
    """
    i = int(start / dt)
    j = int(stop / dt)
    lst = []
    for k in rang(i,j):
        lst.append(to_select[k])
    lst_t = linspace(start, dt, stop)

    return lst_t, lst


