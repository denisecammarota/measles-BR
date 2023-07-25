# Doing basic data exploration and analysis with age 
# years 2007 to 2021
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

# Replace vaccination status nan for 9
data_total['CS_VACINA'] = data_total['CS_VACINA'].replace(np.nan,9)

# Defining the SUS age groups
age_groups = np.array([0,4,9,14,19,29,39,49,59,69,79,120]) # age groups of tabnet datasus

# Adding this range for each case
data_total['GRUPO_IDADE'] = data_total['NU_IDADE_N'].transform(lambda x: pd.cut(x, bins = age_groups).astype(str))

# And now we create an auxiliary thing
data_aux = data_total.copy()

# Now we have to group
data_total = data_total.groupby(['ID_MUNICIP','GRUPO_IDADE'])['CASO'].sum()
data_total = data_total.reset_index(name = 'CASOS')

# Filtering vaccinated people
vaccinated_municipality = data_aux.copy()
vaccinated_municipality = vaccinated_municipality[vaccinated_municipality['CS_VACINA'] == 1]
vaccinated_municipality = vaccinated_municipality.groupby(['ID_MUNICIP', 'GRUPO_IDADE'])['CASO'].sum()
vaccinated_municipality = vaccinated_municipality.reset_index(name = 'VAC')

# Filtering non-vaccinated people
nonvaccinated_municipality = data_aux.copy()
nonvaccinated_municipality = nonvaccinated_municipality[nonvaccinated_municipality['CS_VACINA'] == 2]
nonvaccinated_municipality = nonvaccinated_municipality.groupby(['ID_MUNICIP', 'GRUPO_IDADE'])['CASO'].sum()
nonvaccinated_municipality  = nonvaccinated_municipality .reset_index(name = 'N_VAC')

# Merging everything together
cases_municipality = data_total.merge(vaccinated_municipality, how = 'left', on = ['ID_MUNICIP','GRUPO_IDADE']).fillna(0)
cases_municipality = cases_municipality.merge(nonvaccinated_municipality, how = 'left', on = ['ID_MUNICIP','GRUPO_IDADE']).fillna(0)
cases_municipality['I_VAC'] = cases_municipality['CASOS'] - cases_municipality['VAC'] - cases_municipality['N_VAC']

# Adding the state id number
cases_municipality['SG_UF_NOT'] = cases_municipality['ID_MUNICIP'].astype(str).str[:2].astype(int)

# Saving the data 
if(not(os.path.exists('./Data/analyzed/'))):
    os.makedirs('./Data/analyzed/')
path_save = './Data/analyzed/'+'basic_age_analysis.csv'
cases_municipality.to_csv(path_save, sep=',')