import numpy as np
from Redbox_v2 import file_manager as fm
import pandas as pd
from scipy.fftpack import rfft, rfftfreq
import matplotlib.pyplot as plt
import os
import math



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

    this functions does not return the real time of the occuring
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


def n_seconds_min_max(data, dt, n):
    """
    :param data = 2D array with t and velocity in one direction
    :param dt = sample space or time between samples
    :param n = in seconds for which interval maximum value is determined

    collect minimum and maximum values of the data over an interval
    """
    samples = int(1/dt * n)
    start = 0
    end = samples

    min_max_array = np.zeros([1, 2])   # col 1 = time [s], col 2 = min and max of direction
    while start < data.shape[0]:
        index_max = start + np.argmax(data[start:end, 1])
        index_min = start + np.argmin(data[start:end, 1])
        x = np.array([[data[index_max,0], data[index_max,1]], [data[index_min,0], data[index_min,1]]])
        min_max_array = np.concatenate((min_max_array, x), axis=0)

        start = end
        end += samples

    min_max_array = np.delete(min_max_array,0,0)
    min_max_array = min_max_array[min_max_array[:,0].argsort()]
    return min_max_array


def FFT(signal,dT):
    """
    :param signal: [array]
    :param dT: sample space [float]
    """
    ampl = np.abs(rfft(signal)) * 2.0 / len(signal)
    freq = rfftfreq(len(ampl),d=dT)
    return ampl, freq


def FFT_amplitude(signal):
    """
    :param signal: [array]
    """
    ampl = np.abs(rfft(signal)) * 2.0 / len(signal)
    return ampl


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
            rms_amplitude[n] = rms_freq_dom(amplitude[int(lower_bound // df)*2:int(upper_bound // df)*2])
            lower_bound = lower_bound * one_third_octave
            upper_bound = upper_bound * one_third_octave
        return rms_amplitude, spectrum
    else:
        print("ERROR frequency range is not large enough")
        return


def FFT_to_OneThird_Octave2(amplitude, df, spectrum):
    """
    :param amplitude: amplitudes of the FFT [array]
    :param frequency: frequencies of the FFT [array]

    """

    one_third_octave = 2 ** (1 / 3)
    spectrum = spectrum
    rms_amplitude = np.empty(len(spectrum))
    high = spectrum[-1]

    #check if the maximum available frequency exceeds the upper bound
    if (df*len(amplitude))*one_third_octave**0.5 > high:
        lower_bound = spectrum[0] / one_third_octave ** 0.5
        upper_bound = spectrum[0] * one_third_octave ** 0.5
        for n in range(rms_amplitude.size):
            rms_amplitude[n] = rms_freq_dom(amplitude[int(lower_bound // df)*2:int(upper_bound // df)*2])
            lower_bound = lower_bound * one_third_octave
            upper_bound = upper_bound * one_third_octave
        return rms_amplitude
    else:
        print("ERROR frequency range is not large enough")
        return
"""
integration and differentiation
"""

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
    TODO nagaan of deze functie werkelijk nuttig is
        :param start: start of selection(flt/int)
        :param stop: end time of selection (flt/int)
        :return: (tpl) (displacement u, velocity v)
    """
    i = int(start / dt)
    j = int(stop / dt)
    lst = []
    for k in range(i,j):
        lst.append(to_select[k])
    lst_t = np.linspace(start, dt, stop)

    return lst_t, lst

""" SBR methods"""

def compute_veff_sbr(v,T,Ts=0.125, a=8):
    """
    :param =df =  vels (mm/s)
    :param = T = sample space (s)
    :param a = each a'th sample is used
    """
    l = int(np.log2(v.size)+1) #nth-power
    N_org = v.size
    N = 2**l
    t = np.linspace(0,N*T,N,endpoint=False)

    v = np.pad(v,(0,N-v.size),'constant')
    vibrations_fft = np.fft.fft(v)

    f = np.linspace(0, 1 / T, N, endpoint=False)

    f_mod=f
    f_mod[f<1.0]=0.1

    weight = 1 / np.sqrt(1 + (5.6 / f_mod) ** 2)
    vibrations_fft_w = weight * vibrations_fft
    vibrations_w = np.fft.ifft(vibrations_fft_w).real

    t_sel = t[:N_org:a]
    vibrations_w = vibrations_w[:N_org:a]
    v_sqrd_w = vibrations_w ** 2

    v_eff = np.zeros(t_sel.size)
    dt = t_sel[1] - t_sel[0]
    print('compute v_eff')
    for i in range(t_sel.size - 1):
        g_xi = np.exp(-t_sel[:i + 1][::-1] / Ts)
        v_eff[i] = np.sqrt(1 / Ts * np.trapz(g_xi * v_sqrd_w[:i + 1], dx=dt))
        fm.progress(i,t_sel.size-1,"processing %s of %s" % (i + 1, t_sel.size))

    idx = np.argmax(v_eff)
    return v_eff[idx], t_sel, vibrations_w, v_eff


def plot_SBR_B(save_to_path,vibrations, vibrations_w,v_eff,t_sel):
    """
    vibrations, vibrations_w,v_eff are optional arguments
    """
    plt.figure(figsize=(10, 6))
    if vibrations:
        plt.plot(t_sel, vibrations, label="signal")
    if vibrations_w:
        plt.plot(t_sel, vibrations_w, label="weighted_signal")
    if v_eff:
        plt.plot(t_sel, v_eff, label="v_eff")
        plt.text(t[idx], v_eff[idx], "max v_eff: {}".format(round(v_eff[idx], 3)), color="r")
    plt.xlabel("t [s]")
    plt.ylabel("v [mm/s]")
    plt.title("velocity")
    plt.legend()
    plt.savefig(save_to_path.format("png"))
    plt.show()

def plot_SBR_B_xyz(save_to_path,vibrations, vibrations_w,v_eff,t_sel):
    """
    TODO check use of pandas plotting wrapper
    vibrations, vibrations_w,v_eff are optional arguments (tpl)
    """

    fig = plt.figure(figsize=(10, 18))
    ax1 = fig.add_subplot(3,1,1)
    ax2 = fig.add_subplot(3,1,2)
    ax3 = fig.add_subplot(3,1,3)
    if vibrations:
        ax1.plot(t_sel, vibrations[0], label="signal")
        ax2.plot(t_sel, vibrations[1], label="signal")
        ax3.plot(t_sel, vibrations[2], label="signal")
    if vibrations_w:
        ax1.plot(t_sel, vibrations_w[0], label="weighted_signal")
        ax2.plot(t_sel, vibrations_w[1], label="weighted_signal")
        ax3.plot(t_sel, vibrations_w[2], label="weighted_signal")
    if v_eff:
        idx = [np.argmax(v_eff[x]) for x in range(len(v_eff))]
        ax1.plot(t_sel, v_eff, label="v_eff")
        ax1.text(t[idx[0]], v_eff[0][idx[0]], "max v_eff: {}".format(round(v_eff[idx], 3)), color="r")
        ax2.plot(t_sel, v_eff, label="v_eff")
        ax2.text(t[idx[1]], v_eff[1][idx[1]], "max v_eff: {}".format(round(v_eff[idx], 3)), color="r")
        ax3.plot(t_sel, v_eff, label="v_eff")
        ax3.text(t[idx[1]], v_eff[2][idx[2]], "max v_eff: {}".format(round(v_eff[idx], 3)), color="r")
    plt.xlabel("t [s]")
    plt.ylabel("v [mm/s]")
    plt.title("velocity")
    plt.legend()
    plt.savefig(save_to_path.format("png"))
    plt.show()