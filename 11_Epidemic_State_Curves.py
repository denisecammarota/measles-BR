# Doing epidemic curve of all, local and non-local cases infection, 
# years 2007 to 2021, for requested state of residence 
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

id_uf = 13

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


# Doing basic epidemiological curves

# Separating year and epidemiological week
data_total['SEM_EPI'] = data_total['SEM_PRI'].astype(str).str[4:]
data_total['ANO_EPI'] =  data_total['SEM_PRI'].astype(str).str[:4]

# Uniting them with a -
data_total['DATA_EPI'] =  data_total['ANO_EPI'] + '-' + data_total['SEM_EPI']


# Resident cases
data_res = data_total[data_total['SG_UF'] == id_uf]
res_curve = data_res.groupby(['DATA_EPI'])['CASO'].sum()
res_curve = res_curve.reset_index()
res_curve.to_csv('./Data/analyzed/res_epi_curve_'+str(id_uf)+'.csv')


# Notified cases
data_not = data_total[data_total['SG_UF'] == id_uf]
not_curve = data_not.groupby(['DATA_EPI'])['CASO'].sum()
not_curve = not_curve.reset_index()
not_curve.to_csv('./Data/analyzed/not_epi_curve_'+str(id_uf)+'.csv')

