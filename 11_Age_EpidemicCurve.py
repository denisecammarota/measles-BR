# Doing basic data exploration and analysis with age 
# years 2018 to 2021
# discriminated by different places of notification and residence
# Code developed by Denise Cammarota

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob

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

# And now we filter municipality
data_total = data_total[data_total['ID_MN_RESI'] == 355030]

# Separating year and epidemiological week
data_total['SEM_EPI'] = data_total['SEM_PRI'].astype(str).str[4:]
data_total['ANO_EPI'] =  data_total['SEM_PRI'].astype(str).str[:4]
data_total['DATA_EPI'] = data_total['ANO_EPI'] + '-' + data_total['SEM_EPI']

# Defining the SUS age groups
age_groups = np.array([0,4,9,14,19,29,39,49,59,69,79,120]) # age groups of tabnet datasus

# Adding this range for each case
data_total['GRUPO_IDADE'] = data_total['NU_IDADE_N'].transform(lambda x: pd.cut(x, bins = age_groups).astype(str))

# Now we are going to get the data for generating spatio-temporal maps

# Separating based on residence municipality
data_res = data_total.copy()
data_res = data_res.groupby(['DATA_EPI','GRUPO_IDADE'])['CASO'].sum()
data_res = data_res.reset_index()

# And now we will convert age groups to columns 
data_res = data_res.pivot_table(values='CASO', index = 'DATA_EPI',columns='GRUPO_IDADE', aggfunc='first')
data_res = data_res.reset_index()
data_res = data_res.fillna(0)
data_res = data_res.drop(columns = data_res.keys()[-1])

# We add all cases as well
data_res['TOTAL'] = data_res.iloc[:,1:].sum(axis = 1)

# reorder columns

