import os
import sys

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * float(count) / float(total), 2)
    bar = '+' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s ...%s' % (bar, percents, '%', status))
    sys.stdout.flush()

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

folder_1 = r"P:\142\14208\Onderzoeksgegevens\Trillingen\Metingen VC vergelijking 1\Betacampus_pos1"
folder_2 = r"P:\142\14208\Onderzoeksgegevens\Trillingen\Metingen VC vergelijking 1\Betacampus_pos2"
folder_3 = r"P:\142\14208\Onderzoeksgegevens\Trillingen\Metingen VC vergelijking 1\Huygensgebouw"
rename(folder_2)
rename(folder_3)

