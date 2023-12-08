# Extracting cities from the state of Sao Paulo in order to do analysis 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob
import datetime

files = glob.glob('./Data/processed/*.csv')
data_total = pd.DataFrame()

id_uf = 35

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


# Resident cases in the state of SP
data_res = data_total[data_total['SG_UF'] == id_uf]

# Getting all municipalities
municipalities_sp = data_res['ID_MN_RESI'].unique()
len(municipalities_sp)

# ask for data from or later than 2018 and up to 2021 (excluding 2021)
data_res['ANO_EPI'] = data_res['ANO_EPI'].astype(int)
data_res = data_res[data_res['ANO_EPI'] >= 2018]
data_res = data_res[data_res['ANO_EPI'] < 2021]

for municipality in municipalities_sp:
    data_mun = data_res[data_res['ID_MN_RESI'] == municipality]
    res_curve = data_mun.groupby(['DATA_EPI'])['CASO'].sum()
    res_curve = res_curve.reset_index()
    res_curve.to_csv('./Data/analyzed/municipalities_SP/res_epi_curve_'+str(municipality)+'.csv')

    



