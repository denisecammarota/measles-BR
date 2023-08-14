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

# Separating year and epidemiological week
data_total['SEM_EPI'] = data_total['SEM_PRI'].astype(str).str[4:]
data_total['ANO_EPI'] =  data_total['SEM_PRI'].astype(str).str[:4]

# Defining the SUS age groups
age_groups = np.array([0,4,9,14,19,29,39,49,59,69,79,120]) # age groups of tabnet datasus

# Adding this range for each case
data_total['GRUPO_IDADE'] = data_total['NU_IDADE_N'].transform(lambda x: pd.cut(x, bins = age_groups).astype(str))

# Now we are going to get the data for generating spatio-temporal maps

# Separating based on notification municipality
data_not = data_total.copy()
data_not = data_not.groupby(['ID_MUNICIP','GRUPO_IDADE'])['CASO'].sum()
data_not = data_not.reset_index()

# And now we will convert age groups to columns 
data_not = data_not.pivot_table(values='CASO', index=['ID_MUNICIP'], columns='GRUPO_IDADE', aggfunc='first')
data_not = data_not.reset_index()
data_not = data_not.fillna(0)
data_not = data_not.drop(columns = data_not.keys()[-1])

# We add all cases as well
data_not['TOTAL'] = data_not.iloc[:,1:].sum(axis = 1)

# Saving dataframe
data_not.to_csv('./Data/analyzed/not_year_evo.csv') 


# Separating based on residence municipality
data_res = data_total.copy()
data_res = data_res.groupby(['ID_MN_RESI','GRUPO_IDADE'])['CASO'].sum()
data_res = data_res.reset_index()

# And now we will convert age groups to columns 
data_res = data_res.pivot_table(values='CASO', index=['ID_MN_RESI'], columns='GRUPO_IDADE', aggfunc='first')
data_res = data_res.reset_index()
data_res = data_res.fillna(0)
data_res = data_res.drop(columns = data_res.keys()[-1])

# We add all cases as well
data_res['TOTAL'] = data_res.iloc[:,1:].sum(axis = 1)

# Saving dataframe
data_res.to_csv('./Data/analyzed/res_year_evo.csv') 