import os
import numpy as np
import datetime as dt
import sys
import pandas as pd

# progress bar


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * float(count) / float(total), 2)
    bar = '+' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s ...%s' % (bar, percents, '%', status))
    sys.stdout.flush()

# obtain files and data


def obtain_files(folder_path):
    """"
    returns all items in a certain folder
    :param folder_path: [path]
    """
    return os.listdir(folder_path)


def file_time(item):
    """
    :param item = filename
    find starting point of measurement
    """
    year = int(item[0:4])
    month = int(item[4:6])
    day = int(item[6:8])
    hour = int(item[8:10])
    minute = int(item[10:12])
    second = int(item[12:14])
    microseconds = int(item[14:20])
    filetime = dt.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second,
                           microsecond=microseconds)
    return filetime

# old
# def load_data_with_datetime(filename):
#     """
#     extract relevant data from txt file produced by the logger
#     :param filename : (raw string)
#     :return (tpl) (velocity x-direction, velocity y-direction, velocity z-direction)
#     """
#     with open(filename, encoding='latin-1') as f:
#         skip = 0
#         total = None
#         start = None
#         for cnt, line in enumerate(f):
#             if line.startswith('# StartDate'):
#                 year = int(line[12:16])
#                 month = int(line[17:19])
#                 day = int(line[20:22])
#                 # date = dt.date(year=year, month=month, day=day)
#                 total = dt.datetime(year=year, month=month, day=day)
#                 skip += 1
#             elif line.startswith('# StartTime'):
#                 hour = int(line[12:14])
#                 minutes = int(line[15:17])
#                 seconds = int(line[18:20])
#                 start = total + dt.timedelta(hours=hour, minutes=minutes, seconds=seconds)
#                 skip += 1
#             elif line.startswith('#'):
#                 skip += 1
#
#         t, x, y, z = np.loadtxt(filename, skiprows=skip, unpack=True)
#         t = t * dt.timedelta(seconds=1) + start
#     return t, x, y, z


def load_data_as_ndarray(filename):
    return np.loadtxt(filename, delimiter=' ', dtype="float", comments="#")

def load_data_as_dataframe(filename, header=('t','x','y','z')):

    return pd.read_csv(filename,sep=' ',comment= '#', header = None,names=header)

def obtain_SBR_data(filename):
    """
    extract relevant data from txt file produced by the logger
    :param filename : (raw string)
    :return (tpl) (velocity x-direction, velocity y-direction, velocity z-direction)
    """
    with open(filename, encoding='latin-1') as f:
        skip = 0
        total = None
        start = None
        for cnt, line in enumerate(f):
            if line.startswith('# StartDate'):
                year = int(line[12:16])
                month = int(line[17:19])
                day = int(line[20:22])
                # date = dt.date(year=year, month=month, day=day)
                total = dt.datetime(year=year, month=month, day=day)
                skip += 1
            elif line.startswith('# StartTime'):
                hour = int(line[12:14])
                minutes = int(line[15:17])
                seconds = int(line[18:20])
                start = total + dt.timedelta(hours=hour, minutes=minutes, seconds=seconds)
                skip += 1
            elif line.startswith('#'):
                skip += 1
        t, peak_x, peak_y, peak_z, f_x, f_y, f_z = np.loadtxt(filename, skiprows=skip ,unpack=True)
        t = t * dt.timedelta(seconds=1) + start
    return [t, peak_x, peak_y, peak_z, f_x, f_y, f_z]


# renaming files


def create_filename(file_path):
    """
    extract relevant data from txt file produced by the logger
    :param file_path : (str) enter full path of filename like: r"path"
    :return: (str) filename consisting start date and start time
    """

    startdate = None
    starttime = None

    with open(file_path, encoding='latin-1') as f:
        lines = f.readlines()
        for i in lines:
            if i.startswith('# StartDate'):
                startdate = i
            elif i.startswith('# StartTime'):
                starttime = i
    filename = ""

    startdate = str(startdate)
    starttime = str(starttime)

    for i in startdate:
        try:
            int(i)
            filename += str(i)
        except:
            pass
    for i in starttime:
        try:
            int(i)
            filename += str(i)
        except:
            pass
    return filename


def rename(folder):
    """
    Rename all files in given folder. Filename based on
    param:
    """
    items = os.listdir(folder)
    for n,i in enumerate(items):
        fpath = folder + "\%s" %i
        new_filename = folder + "\%s.txt" %create_filename(fpath)
        if not os.path.exists(new_filename):
            os.rename(fpath,new_filename)
            progress(n + 1, len(items), "processing %s of %s" % (n + 1, len(items)))
    return

def rename_and_move(orgin_folder, dest_folder):
    """
    Move all files in given folder to another.
    Filename based on date and time
    param:
    """
    items = os.listdir(orgin_folder)
    for n,i in enumerate(items):
        fpath = orgin_folder + "\%s" %i
        new_filename = dest_folder + "\%s.txt" %create_filename(fpath)
        if not os.path.exists(new_filename):
            os.rename(fpath, new_filename)
            progress(n + 1, len(items), "processing %s of %s" % (n + 1, len(items)))
    return
#moving all files to one folder
''' not copy! '''

def move_files(orgin, dest):
    """
    improve with checking if items are folders or files.
    """
    items = os.listdir(orgin)

    for n,i in enumerate(items):
        foo = os.path.join(orgin, i)
        rename_and_move(foo, dest)


