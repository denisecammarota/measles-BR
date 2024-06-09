# Extracting cities from the state of Sao Paulo in order to do analysis 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob
import datetime
from epiweeks import Week, Year
from sklearn.utils.extmath import cartesian



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

# Grouping for DT_SIN_PRI and ID_MN_RESI
data_res = data_res.groupby(['ANO_EPI','SEM_EPI','ID_MN_RESI'])['CASO'].sum()
data_res = data_res.reset_index(name = 'CASO')

# Padding for the rest of weeks and dates
mun_list = np.unique(data_res['ID_MN_RESI'])
year_list = np.arange(2007,2023,1)
week_list = np.arange(1,54,1)
        

df = pd.DataFrame(cartesian((year_list, week_list, mun_list)))
df = df.rename(columns={0: "ANO_EPI", 1: "SEM_EPI", 2: "ID_MN_RESI"})
df['CASO'] = 0
df['ID_MN_RESI'] = df['ID_MN_RESI'].astype(int)
df['ANO_EPI'] = df['ANO_EPI'].astype(int)
df['SEM_EPI'] = df['SEM_EPI'].astype(int)
df['CASO'] = df['CASO'].astype(int)

data_res['ID_MN_RESI'] = data_res['ID_MN_RESI'].astype(int)
data_res['ANO_EPI'] = data_res['ANO_EPI'].astype(int)
data_res['SEM_EPI'] = data_res['SEM_EPI'].astype(int)
data_res['CASO'] = data_res['CASO'].astype(int)

df = df.merge(data_res, how = 'left', on = ['ANO_EPI','SEM_EPI','ID_MN_RESI'])
df['CASO'] = df['CASO_y']
df['CASO'] = df['CASO'].fillna(0)
df = df.drop(columns = ['CASO_x','CASO_y'])

df['DATA_EPI'] =  df['ANO_EPI'].astype(str) + '-' + df['SEM_EPI'].astype(str)

for year in year_list:
    n_weeks = Year(year).totalweeks()
    print(year,n_weeks)
    if(n_weeks == 52):
        week_rm = str(year)+'-53'
        df = df[df['DATA_EPI'] != week_rm]

df = df.to_csv('Data/analyzed/epicurves_SP.csv')
