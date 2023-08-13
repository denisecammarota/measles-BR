# Doing basic data exploration and analysis with municipality of probable 
# infection, years 2007 to 2021
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
                            parse_dates = ['DT_SIN_PRI','SEM_PRI','DT_NOTIFIC','SEM_NOT'], encoding='cp1252')
    # get the year we are working with in question
    # first column is read differently
    data_test = data_test.drop(columns = ['Unnamed: 0'])
    data_total = data_total.append(data_test)

# Doing this for basic data analysis    
data_total['CASO'] = 1

# Seeing how many of records of probable infection are correctly filled

# We start with country of residence
country_res = data_total.groupby(['ID_PAIS'])['CASO'].sum()
country_res = country_res.reset_index()
country_res['PROP'] = country_res['CASO']*100/data_total.shape[0]

# Now country of probable infection
country_inf = data_total.groupby(['COPAISINF'])['CASO'].sum()
country_inf = country_inf.reset_index()
country_inf['PROP'] = country_inf['CASO']*100/data_total.shape[0]

# Let's check what the 0 cases are with respect to residence
data_copaisinf_0 = data_total[data_total['COPAISINF'] == 0]
data_copaisinf_0 = data_copaisinf_0.groupby(['ID_PAIS'])['CASO'].sum()
data_copaisinf_0 = data_copaisinf_0.reset_index()
data_copaisinf_0['PROP'] = data_copaisinf_0['CASO']*100/data_total.shape[0]

# Combining both residence and probable infection
country_resinf = data_total.groupby(['ID_PAIS','COPAISINF'])['CASO'].sum()
country_resinf = country_resinf.reset_index()
country_resinf['PROP'] = country_resinf['CASO']*100/data_total.shape[0]


# Notification place of cases resident in 138
data_res_138 = data_total[data_total['ID_PAIS'] == 138]
data_res_138 = data_res_138.groupby(['ID_MUNICIP'])['CASO'].sum()
data_res_138 = data_res_138.reset_index()

# Notification place of cases infected in 138
data_inf_138 = data_total[data_total['COPAISINF'] == 138]
data_inf_138 = data_inf_138.groupby(['ID_MUNICIP'])['CASO'].sum()
data_inf_138 = data_inf_138.reset_index()

# Cases resident abroad notified in X municipality
data_res_abroad = data_total[data_total['ID_PAIS'] != 1]
data_res_abroad = data_res_abroad[data_res_abroad['ID_PAIS'] != 0]
data_res_abroad = data_res_abroad.groupby(['ID_MUNICIP'])['CASO'].sum()
data_res_abroad = data_res_abroad.reset_index()
data_res_abroad.to_csv('./Data/analyzed/res_abroad.csv')


# Cases infected abroad notified in X municipality
data_inf_abroad = data_total[data_total['ID_PAIS'] != 1]
data_inf_abroad = data_inf_abroad[data_inf_abroad['ID_PAIS'] != 0]
data_inf_abroad = data_inf_abroad.groupby(['ID_MUNICIP'])['CASO'].sum()
data_inf_abroad = data_inf_abroad.reset_index()
data_inf_abroad.to_csv('./Data/analyzed/inf_abroad.csv')