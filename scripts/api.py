# Python 3.10


#%%
from urllib.request import urlopen
import json
import io
import requests
import pandas as pd
import numpy as np
import scipy as sc
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
from statistics import mean, median, stdev, variance, pvariance
from itertools import combinations, combinations_with_replacement, permutations
from scipy.stats import pearsonr, skew, rankdata
import scipy.stats as stats
from tabulate import tabulate
import math


#%%
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'


#%%
def corr(x_simple, y_simple):
    my_rho = np.corrcoef(x_simple, y_simple)
    print(my_rho)


#%%
def plot(df=[], val=''):
    ax = plt.gca()
    ax.set_title(val)
    df[0].plot(kind='line', x='date', y=val, label='Österreich', color='orange', ax=ax)
    df[1].plot(kind='line', x='date', y=val, label='Deutschland', color='black', ax=ax)
    df[2].plot(kind='line', x='date', y=val, label='Großbritannien', color='red', ax=ax)
    df[3].plot(kind='line', x='date', y=val, label='Schweden', color='blue', ax=ax)
    plt.show()

#%%
# request data via api
content = requests.get(url).content
df = pd.read_csv(io.StringIO(content.decode('utf-8')))

#%%
# prepare dataframe
df.set_index(['date', 'iso_code'], inplace=True)

#%%
# restrict date
df = df[df.date < '2021-08-01']
#df.loc[(df['date'] >= '2020-01-01') & (df['date'] < '2020-10-01')]

#%%
# interpolate missing data
#df['total_vaccinations_per_hundred'].fillna(method ='pad', inplace=True)
#df.interpolate(inplace=True)
country = ['SWE']
df1 = df[df.iso_code.isin(country)]
df['total_vaccinations_per_hundred'] = df1['total_vaccinations_per_hundred'].interpolate()
df = pd.concat([df, df1])

#%%
# restrict region
countries = ['AUT', 'DEU', 'GBR']
df = df[df.iso_code.isin(countries)]
#continent = ['Europe']
#df = df[df.continent.isin(continent)]

#%%
# separate dataframes
df_cases = df[['date', 'iso_code', 'new_cases_smoothed_per_million']]
df_deaths = df[['date', 'iso_code', 'new_deaths_smoothed_per_million']]
df_vacc = df[['date', 'iso_code', 'new_people_vaccinated_smoothed_per_hundred']]
df_total_cases = df[['date', 'iso_code', 'total_cases_per_million']]
df_total_deaths = df[['date', 'iso_code', 'total_deaths_per_million']]
df_total_vacc = df[['date', 'iso_code', 'total_vaccinations_per_hundred']]
df_stringency_index = df[['date', 'iso_code', 'stringency_index']]

#%%
df1 = df_stringency_index
dfAUT = (df_stringency_index[df_stringency_index.iso_code=='AUT'])
dfDEU = (df_stringency_index[df_stringency_index.iso_code=='DEU'])
dfDNK = (df_stringency_index[df_stringency_index.iso_code=='DNK'])
dfSWE = (df_stringency_index[df_stringency_index.iso_code=='SWE'])
dfPRT = (df_stringency_index[df_stringency_index.iso_code=='PRT'])
dfGBR = (df_stringency_index[df_stringency_index.iso_code=='GBR'])
plot([dfAUT, dfDEU, dfGBR, dfSWE], 'stringency_index')

#%%
country = ['AUT']
df = df[df.iso_code.isin(country)]
#df = df.loc[(df['date'] >= '2021-07-01') & (df['date'] < '2022-01-01')]
df = df.loc[df['date'] < '2021-05-01']
#df2 = df[['new_cases_smoothed_per_million', 'new_deaths_smoothed_per_million']]
df2 = df[['new_cases_smoothed_per_million', 'new_deaths_smoothed_per_million', 'new_vaccinations_smoothed_per_million', 'stringency_index']]
#df2 = df[['total_cases_per_million', 'total_deaths_per_million', 'total_vaccinations_per_hundred', 'stringency_index']]
#df2 = df[['total_cases', 'total_deaths', 'total_vaccinations', 'stringency_index']]
corrM = df2.corr(method='pearson')
print(corrM)
print(df[['total_deaths']])

#%%
corr1 = df['new_cases'].corr(df['new_deaths'], method="kendall")
print(corr1)

#%%
ax = plt.gca()
df.plot(kind='line', x='date', y='new_cases_smoothed_per_million', label='Fallzahlen', color='orange', ax=ax)
df.plot(kind='line', x='date', y='new_deaths_smoothed_per_million', label='Todesfälle', color='black', ax=ax)
plt.show()

#%%
df.set_index(['date', 'iso_code'], inplace=True)
df.set_index('date', inplace=True)
corrR = df['new_cases'].rolling(90).corr(df['new_deaths'], method="kendall")
print(corrR)
corrR.plot()
plt.show()

#%%
f = plt.figure()
plt.matshow(df2.corr(), fignum=f.number)
plt.xticks(range(df2.select_dtypes(['number']).shape[1]), df2.select_dtypes(['number']).columns, rotation=90)
plt.yticks(range(df2.select_dtypes(['number']).shape[1]), df2.select_dtypes(['number']).columns)
cb = plt.colorbar()
plt.title('Correlation Matrix')
plt.show()