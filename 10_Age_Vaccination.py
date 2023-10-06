# Extracting information on age and vaccination status
# Code by Denise Cammarota

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

# Filtrating the data we need

# National
data_aux = data_total.copy()
data_aux  = data_aux[['NU_IDADE_N','CS_VACINA']]
data_aux.to_csv('./Data/analyzed/age_vaccine_national.csv')

# Selected municipalities
select_muni = [130260,130250,140045,351630]

for muni in select_muni:
    data_aux = data_total.copy()
    data_aux = data_aux[data_aux['ID_MN_RESI'] == muni]
    data_aux  = data_aux[['NU_IDADE_N','CS_VACINA']]
    data_aux.to_csv('./Data/analyzed/age_vaccine_'+str(muni)+'.csv')

# All states, modifing for states 
data_states = data_total.copy()
data_states = data_states[['SG_UF','NU_IDADE_N','CS_VACINA']]
data_states.to_csv('./Data/analyzed/age_vaccine_states.csv')


# All municipalities
data_aux = data_total.copy()
data_aux  = data_aux[['ID_MN_RESI','NU_IDADE_N','CS_VACINA']]
data_aux.to_csv('./Data/analyzed/age_vaccine_municipalities.csv')
