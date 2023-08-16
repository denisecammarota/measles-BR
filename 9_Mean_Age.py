# Calculating mean age at infection, considering simple naive SIR model
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

# Separating year and epidemiological week
data_total['SEM_EPI'] = data_total['SEM_PRI'].astype(str).str[4:]
data_total['ANO_EPI'] =  data_total['SEM_PRI'].astype(str).str[:4]

# Uniting them with a -
data_total['DATA_EPI'] =  data_total['ANO_EPI'] + '-' + data_total['SEM_EPI']

data_total = data_total.groupby(['ID_MN_RESI'])['NU_IDADE_N'].mean()
data_total = data_total.reset_index()

mu = 1/80
R0 = 15
data_total['p'] = 1 - ((1/data_total['NU_IDADE_N'])*(1/(mu*(R0-1))))
data_total = data_total[data_total['p'] >= 0]

data_total.to_csv('./Data/analyzed/SIR_naive_p.csv')