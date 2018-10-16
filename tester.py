import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time as time
import os
import csv

file = r"C:\Users\mdk\Desktop\93307\Ruwe trillingsdata\positie_1\20181001112633000195.txt"

# start = time.time()
# data = np.loadtxt(file,delimiter=' ')
# elapsed_time = time.time()-start
# print(data)
# print(elapsed_time)

start = time.time()
data = pd.read_csv(file,sep=' ',comment= '#', header = None,names=('t','x','y','z'))
elapsed_time = time.time()-start
print(data)
print(elapsed_time)
