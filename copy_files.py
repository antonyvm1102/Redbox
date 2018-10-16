import shutil
import os
import sys


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * float(count) / float(total), 1)
    bar = '+' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s ...%s' % (bar, percents, '%', status))
    sys.stdout.flush()

def find_folders(main_folder):
    b = []
    for i in os.walk(main_folder):
        b.append(i)
    return b[0][1]

def copyFile(src, dest):
    try:
        shutil.copy(src, dest)
    # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e.strerror)


def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

def copy_files(src_year,copyto):
    folders_year = src_year
    folders_months = find_folders(folders_year)
    for month in folders_months:
        month_ = folders_year + "\%s" % month
        folders_days = find_folders(month_)
        for day in folders_days:
            day_ = month_ + "\%s" % day
            items = os.listdir(day_)
            for index, item in enumerate(items):
                progress(index+1, len(items),'')
                item_ = day_ + "\%s" % item
                if not os.path.exists(copyto+"\%s" %item):
                    copyFile(item_, copyto)
            print("day %s - %s is finished" % (day, month))

copy_to = r"P:\142\14208\Onderzoeksgegevens\Trillingen\Metingen VC vergelijking 1\Betacampus_pos2"
folders_year = r"P:\142\14208\Onderzoeksgegevens\Trillingen\Metingen VC vergelijking 1\Betacampus 21-maart vlu\mr3000\events\2018"

copy_files(folders_year, copy_to)