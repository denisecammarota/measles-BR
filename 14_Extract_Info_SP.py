# Extracting cities from the state of Sao Paulo in order to do analysis 
# with number of cases overall in the period 2018-2020, infected, non-infected
# and also estimate the percentage

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

# filtrating to epidemic period only
data_total['ANO_EPI'] = data_total['ANO_EPI'].astype(int)
data_total = data_total[data_total['ANO_EPI'] >= 2018]
data_total = data_total[data_total['ANO_EPI'] <= 2020]

# Resident cases in the state of SP
data_res = data_total[data_total['SG_UF'] == id_uf]
data_res['CS_VACINA'] = data_res['CS_VACINA'].replace(np.nan,9)
data_n_vac = data_res[data_res['CS_VACINA'] == 2]
data_vac = data_res[data_res['CS_VACINA'] == 1]
data_ign = data_res[data_res['CS_VACINA']  == 9]

# Separate by city, count by city and number 
data_res = data_res.groupby(['ID_MN_RESI'])['CASO'].sum()
data_res = data_res.reset_index('ID_MN_RESI')

# Doing the same for different vaccination status
data_n_vac = data_n_vac.groupby(['ID_MN_RESI'])['CASO'].sum()
data_n_vac = data_n_vac.reset_index('ID_MN_RESI')

data_vac = data_vac.groupby(['ID_MN_RESI'])['CASO'].sum()
data_vac = data_vac.reset_index('ID_MN_RESI')

data_ign = data_ign.groupby(['ID_MN_RESI'])['CASO'].sum()
data_ign = data_ign.reset_index('ID_MN_RESI')

# Now we merge everything 
data_res = data_res.merge(data_vac, how = 'left', on = 'ID_MN_RESI', suffixes=('', '_VAC'))
data_res = data_res.merge(data_n_vac, how = 'left', on = 'ID_MN_RESI', suffixes=('', '_N_VAC'))
data_res = data_res.merge(data_ign, how = 'left', on = 'ID_MN_RESI', suffixes=('', '_IGN'))
data_res = data_res.fillna(0)

# And now we calculate the vaccination coverage overall in the city
eps = 0.93

# considering ignored are vaccinated
N = data_res['CASO_VAC'] + data_res['CASO_IGN'] + data_res['CASO_N_VAC']
p_vacs = (data_res['CASO_VAC'] + data_res['CASO_IGN'])/(N)
e_p_vacs = np.sqrt(p_vacs*(1 - p_vacs)/N)
data_res['COV_1'] = (1 +((1-eps)*((1/(p_vacs)) -1)))**-1
data_res['E_COV_1'] =  np.sqrt((1-eps)/((eps*(p_vacs-1) + 1)**2))*e_p_vacs

# considering ignored/2 are vaccinated
p_vacs = (data_res['CASO_VAC'] + 0.5*data_res['CASO_IGN'])/(N)
e_p_vacs = np.sqrt(p_vacs*(1 - p_vacs)/N)
data_res['COV_2'] = (1 +((1-eps)*((1/(p_vacs)) -1)))**-1
data_res['E_COV_2'] = np.sqrt((1-eps)/((eps*(p_vacs-1) + 1)**2))*e_p_vacs


data_res.to_csv('./Data/analyzed/municipalities_SP.csv')



