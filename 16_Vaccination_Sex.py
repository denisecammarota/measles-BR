# Analysis of the sex and vaccine state of people
# Code developed by Denise Cammarota
# years 2007 to 2021

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# Dividing by age group
age_groups = np.array([0,4,9,14,19,29,39,49,59,69,79,120]) # age groups of tabnet datasus

# Adding this range for each case
data_total['GRUPO_IDADE'] = data_total['NU_IDADE_N'].transform(lambda x: pd.cut(x, bins = age_groups).astype(str))

# Doing some basic filtering

## vaccination status has to be filled
data_total = data_total[-data_total['CS_VACINA'].isna()] 
data_total = data_total[data_total['CS_VACINA'] != 9]

## sex between M and F
data_total = data_total[data_total['CS_SEXO'].isin(['F','M'])]

## age group available
data_total = data_total[data_total['GRUPO_IDADE'] != 'nan']


# And now grouping by sex, age group and vaccination status
df_vac = data_total.groupby(['CS_SEXO','GRUPO_IDADE','CS_VACINA'])['CASO'].sum()
df_vac = df_vac.reset_index(name = 'CASO')

# Now calculating proportions
df_prop = data_total.groupby(['CS_SEXO','GRUPO_IDADE'])['CASO'].sum()
df_prop = df_prop.reset_index(name = 'CASO')

# Uniting both dataframs
df_vac = df_vac.merge(df_prop, how = 'left', on = ['CS_SEXO','GRUPO_IDADE'])

# Calculating proportions over full dataframe
df_vac['PROP'] = 100*df_vac['CASO_x']/df_vac['CASO_y']

# Eliminating the rest of columns
df_vac = df_vac[['CS_SEXO','GRUPO_IDADE','CS_VACINA','CASO_x','PROP']]

# Filtrating the last age group
df_vac = df_vac[df_vac['GRUPO_IDADE'] != '(79, 120]']

# Filtrating the proportion of vaccinated
df_vac = df_vac[df_vac['CS_VACINA'] == 1]

# And now plotting 
df_vac


sns.catplot(x = 'GRUPO_IDADE', y = 'PROP', hue = 'CS_SEXO', data = df_vac, kind = 'bar', order = ['(0, 4]', '(4, 9]', '(9, 14]', '(14, 19]', '(19, 29]', '(29, 39]', '(39, 49]', '(49, 59]', '(59, 69]', '(69, 79]'])
plt.xlabel('Faixa etária')
plt.ylabel('Prop de vacinados')
plt.xticks(rotation = 'vertical')


sns.catplot(x = 'GRUPO_IDADE', y = 'CASO_x', hue = 'CS_SEXO', data = df_vac, kind = 'bar', order = ['(0, 4]', '(4, 9]', '(9, 14]', '(14, 19]', '(19, 29]', '(29, 39]', '(39, 49]', '(49, 59]', '(59, 69]', '(69, 79]'])
plt.xlabel('Faixa etária')
plt.ylabel('Prop de vacinados')
plt.xticks(rotation = 'vertical')
