# Doing epidemic curve of all, local and non-local cases infection, 
# years 2007 to 2021, difference between municipality of residence and of report
# Code developed by Denise Cammarota

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob
import datetime

files = glob.glob('./Data/processed/*.csv')
data_total = pd.DataFrame()


for file in files:
    # reading data 
    data_test = pd.read_csv(file, 
                            delimiter = ',',
                            index_col=False,
                            parse_dates = ['DT_SIN_PRI','DT_NOTIFIC'], encoding='cp1252')
    # get the year we are working with in question
    # first column is read differently
    data_test = data_test.drop(columns = ['Unnamed: 0'])
    data_total = data_total.append(data_test)
    
# Doing this for basic data analysis    
data_total['CASO'] = 1

# Municipality of residence vs of notification - overall
data_diff = data_total[data_total['ID_MUNICIP'] != data_total['ID_MN_RESI']]
n_diff = data_diff.shape[0]


# Identifying residence vs notification combos that are more common
data_diff = data_diff.groupby(['ID_MUNICIP','ID_MN_RESI'])['CASO'].sum()
data_diff = data_diff.reset_index()
