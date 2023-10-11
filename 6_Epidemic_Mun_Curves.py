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

id_municip = 160030

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

# How many cases notified here?
n_notified = sum(data_total['ID_MUNICIP'] == id_municip)

# How many of these cases reside here actually?
data_notified = data_total[data_total['ID_MUNICIP'] == id_municip]
n_notified_res = sum(data_notified['ID_MN_RESI'] == id_municip)

# How many cases residing here?
n_resident = sum(data_total['ID_MN_RESI'] == id_municip)
data_resident = data_total[data_total['ID_MN_RESI'] == id_municip]
data_resident = data_resident.groupby(['ID_MUNICIP'])['CASO'].sum()
data_resident = data_resident.reset_index()

# How many cases reside in another country?
data_res_ab = data_total[data_total['ID_MUNICIP'] == id_municip]
data_res_ab = data_res_ab[data_res_ab['ID_PAIS'] != 1]
n_res_ab = data_res_ab.shape[0]


# How many cases were infected in another country?
data_inf_ab = data_total[data_total['ID_MUNICIP'] == id_municip]
data_inf_ab = data_inf_ab[data_inf_ab['COPAISINF'] != 1]
n_inf_ab = data_inf_ab.shape[0]


# Doing basic epidemiological curves


# Separating year and epidemiological week
data_total['SEM_EPI'] = data_total['SEM_PRI'].astype(str).str[4:]
data_total['ANO_EPI'] =  data_total['SEM_PRI'].astype(str).str[:4]

# Uniting them with a -
data_total['DATA_EPI'] =  data_total['ANO_EPI'] + '-' + data_total['SEM_EPI']


# Resident cases
data_res = data_total[data_total['ID_MN_RESI'] == id_municip]
res_curve = data_res.groupby(['DATA_EPI'])['CASO'].sum()
res_curve = res_curve.reset_index()
res_curve.to_csv('./Data/analyzed/res_epi_curve_'+str(id_municip)+'.csv')


# Notified cases
data_not = data_total[data_total['ID_MUNICIP'] == id_municip]
not_curve = data_not.groupby(['DATA_EPI'])['CASO'].sum()
not_curve = not_curve.reset_index()
not_curve.to_csv('./Data/analyzed/not_epi_curve_'+str(id_municip)+'.csv')



















