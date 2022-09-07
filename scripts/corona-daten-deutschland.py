# Python 3.10


#%%
from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff


#%% 
url_base = 'https://www.corona-daten-deutschland.de'
api_impfdaten = '/api/3/action/datastore_search?resource_id=6f8976ee-7916-4e7e-9a43-23b45b5dcb00'
api_infektionszahlen = '/api/3/action/datastore_search?resource_id=877cc347-8652-4c8d-ac2f-e427335f74c6'
api_intensiv = '/api/3/action/datastore_search?resource_id=da2e682f-6154-434f-bd79-01e816c38ad6'
api_todesfaelle = '/api/3/action/datastore_search?resource_id=e99c8fb7-b8f9-4cc6-801c-debf2b1301a6'
api_hospitalisierungen = '/api/3/action/datastore_search?resource_id=18d6cda5-c0e1-4b12-be46-5f564ac1e3ae'
api_genesene = '/api/3/action/datastore_search?resource_id=4d142c90-98a6-4df0-bb84-5e03c3d94ef9'
api_massnahmen = '/api/3/action/datastore_search?resource_id=b4e715d0-e116-430f-bfe7-c009b0aa0a7b'
cols_massnahmen = {
    'm_code_m01a': 'Kontakt-/Versammlungsbeschr. Privatpers. im priv. Raum',
    'm_code_m01b': 'Kontakt-/Versammlungsbeschr. Privatpers. im öff. Raum',
    'm_code_m02a': 'weiterführende Schulen',
    'm_code_m02b': 'Grundschulen',
    'm_code_m03': 'Kitas',
    'm_code_m04': 'öff. Events&Veranst. Indoor',
    'm_code_m05': 'öff. Events&Veranst. Outdoor',
    'm_code_m06': 'Kultur- & Bildungseinr.',
    'm_code_m07': 'Groß- & Einzelhandel',
    'm_code_m08': 'Gastronomie',
    'm_code_m09': 'Dienstl.&Handwerk',
    'm_code_m10': 'Einrichtungen des Nachtlebens',
    'm_code_m11': 'Beherbergung',
    'm_code_m12': 'Sport Indoor',
    'm_code_m13': 'Sport Outdoor',
    'm_code_m14': 'Reisebeschr. Inland',
    'm_code_m15': 'Reisebeschr. Ausland',
    'm_code_m16': 'Maskenpflicht',
    'm_code_m17': 'Arbeitsplatzbeschränkung',
    'm_code_m18': 'Ausgangsbeschränkung',
    'm_code_m19': 'Kapazitätsbeschr. im öff. Verkehr',
    'm_code_m20': 'Abstandsregelung',
    'm_code_m21': 'Test-Maßnahmen'
}
cols_infektionszahlen = {
    'bl_inz': '7-Tage-Fallzahl',
    'bl_inz_fix': '7-Tage-Fallzahl fixiert',
    'bl_inz_rate': '7-Tage-Inzidenz',
    'bl_inz_rate_fix': '7-Tage-Inzidenz fixiert'
}
cols_hospitalisierungen = {
    'bl_hosp': '7-Tage-Fallzahl Hospitalisierungen',
    'bl_hosp_a0004': '7-Tage-Fallzahl Hospitalisierungen - bis 4 Jahre',
    'bl_hosp_a0514': '7-Tage-Fallzahl Hospitalisierungen - 5 bis 14 Jahre',
    'bl_hosp_a1534': '7-Tage-Fallzahl Hospitalisierungen - 15 bis 34 Jahre',
    'bl_hosp_a3559': '7-Tage-Fallzahl Hospitalisierungen - 35 bis 59 Jahre',
    'bl_hosp_a6079': '7-Tage-Fallzahl Hospitalisierungen - 60 bis 79 Jahre',
    'bl_hosp_a80': '7-Tage-Fallzahl Hospitalisierungen - 80 Jahre oder älter',
    'bl_hosp_inz': '7-Tage-Inzidenz Hospitalisierungen',
    'bl_hosp_inz_a0004': '7-Tage-Inzidenz Hospitalisierungen - bis 4 Jahre',
    'bl_hosp_inz_a0514': '7-Tage-Inzidenz Hospitalisierungen - 5 bis 14 Jahre',
    'bl_hosp_inz_a1534': '7-Tage-Inzidenz Hospitalisierungen - 15 bis 34 Jahre',
    'bl_hosp_inz_a3559': '7-Tage-Inzidenz Hospitalisierungen - 35 bis 59 Jahre',
    'bl_hosp_inz_a6079': '7-Tage-Inzidenz Hospitalisierungen - 60 bis 79 Jahre',
    'bl_hosp_inz_a80': '7-Tage-Inzidenz Hospitalisierungen - 80 Jahre oder älter'
}
cols_intensiv = {
    'kr_its_bett': 'ITS-Betten',
    'kr_its_bett_b': 'Belegte ITS-Betten',
    'kr_its_bett_b_18': 'Belegte ITS-Betten nur Erwachsene',
    'kr_its_bett_ew': 'ITS-Betten pro 100.000 Einwohner',
    'kr_its_bett_f': 'Freie ITS-Betten',
    'kr_its_bett_f_18': 'Freie ITS-Betten nur Erwachsene',
    'kr_its_inf': 'COVID-19-Patienten auf ITS',
    'kr_its_inf_b': 'Anzahl COVID-19-Patienten in Beatmung',
    'kr_its_inf_b_ant': 'Anteil COVID-19-Patienten in Beatmung',
    'kr_its_kh': 'Krankenhäuser mit ITS-Kapazitäten',
    'kr_its_meldeb': 'Meldebereiche mit ITS-Kapazitäten'
}


#%%
url = url_base + api_massnahmen
df = pd.DataFrame()

# request data via api
while True:
    with urlopen(url) as response:
        body = response.read()
        result = json.loads(body)
        assert result['success'] is True
        if len(result['result']['records']) < 1:
            break
        df = pd.concat([df, pd.json_normalize(result['result']  ['records'])])
        url = url_base + result['result']['_links']['next']

## prepare dataframe
#df.drop(['_id', 'ags2', 'rank'], axis=1, inplace=True)
df.drop(['_id', 'ags2'], axis=1, inplace=True)
df.rename(columns = cols_massnahmen, inplace=True)
df.rename(columns = {'datum': 'Datum'}, inplace=True)
df.set_index('Datum', inplace=True)

# transform dataframe to timeline
entries = {val: 0 for val in cols_massnahmen.values()}
tasks = {val: dict() for val in cols_massnahmen.values()}
ts = []
for row in df.iterrows():
    for col in cols_massnahmen.values():
        if row[1][col] == 1:
            if entries[col] == 0:
                tasks[col] = dict(Task=col, Start=row[0], End='',   Massnahme=col)
                entries[col] = 1
        else:
            if entries[col] == 1:
                tasks[col]['Finish'] = row[0]
                ts.append(tasks[col])
                entries[col] = 0

fig = px.timeline(ts, x_start="Start", x_end="Finish",  y="Massnahme", color="Massnahme")
fig.show()


#%%
url = url_base + api_infektionszahlen
df = pd.DataFrame()

# request data via api
while True:
    with urlopen(url) as response:
        body = response.read()
        result = json.loads(body)
        assert result['success'] is True
        if len(result['result']['records']) < 1:
            break
        df = pd.concat([df, pd.json_normalize(result['result']  ['records'])])
        url = url_base + result['result']['_links']['next']

## prepare dataframe
df.drop(['_id', 'ags2', 'rank'], axis=1, inplace=True)
df.rename(columns = cols_infektionszahlen, inplace=True)
df.rename(columns = {'datum': 'Datum'}, inplace=True)
df.set_index('Datum', inplace=True)

# drop illegal values
df.replace(-99, np.nan, inplace=True)

# separate fallzahlen and inzidenz
df_fallzahlen = df.drop(['7-Tage-Inzidenz', '7-Tage-Inzidenz fixiert'], axis=1);
df_inzidenz = df.drop(['7-Tage-Fallzahl', '7-Tage-Fallzahl fixiert'], axis=1)

fig, axes = plt.subplots(nrows=2, ncols=1)
df_fallzahlen.plot(ax=axes[0])
df_inzidenz.plot(ax=axes[1])
df_fallzahlen.plot()
df_inzidenz.plot()
plt.show()


#%%
url = url_base + api_hospitalisierungen
df = pd.DataFrame()

# request data via api
while True:
    with urlopen(url) as response:
        body = response.read()
        result = json.loads(body)
        assert result['success'] is True
        if len(result['result']['records']) < 1:
            break
        df = pd.concat([df, pd.json_normalize(result['result']  ['records'])])
        url = url_base + result['result']['_links']['next']

## prepare dataframe
df.drop(['_id', 'ags2', 'rank'], axis=1, inplace=True)
df.drop(['bl_hosp_fix', 'bl_hosp_adj', 'bl_hosp_inz_fix', 'bl_hosp_inz_adj', 'bl_hosp_adj_c95_ug', 'bl_hosp_adj_c95_og', 'bl_hosp_inz_adj_c95_ug', 'bl_hosp_inz_adj_c95_og'], axis=1,inplace=True)
df.rename(columns = cols_hospitalisierungen, inplace=True)
df.rename(columns = {'datum': 'Datum'}, inplace=True)
df.set_index('Datum', inplace=True)

# drop illegal values
df.replace(-99, np.nan, inplace=True)

#drop age data
df_hospitalisierungen_gesamt = df.drop(list(df.filter(regex=r'.*-(Inzidenz|Fallzahl) Hospitalisierungen - .*')), axis=1)

# separate fallzahlen and inzidenz
df_hospitalisierungen_gesamt_fallzahlen = df_hospitalisierungen_gesamt.drop(list(df_hospitalisierungen_gesamt.filter(regex=r'Inzidenz')), axis=1);
df_hospitalisierungen_gesamt_inzidenz = df_hospitalisierungen_gesamt.drop(list(df_hospitalisierungen_gesamt.filter(regex=r'Fallzahl')), axis=1);

fig, axes = plt.subplots(nrows=2, ncols=1)
df_hospitalisierungen_gesamt_fallzahlen.plot(ax=axes[0])
df_hospitalisierungen_gesamt_inzidenz.plot(ax=axes[1])
plt.show()


#%%
url = url_base + api_intensiv
df = pd.DataFrame()

# request data via api
while True:
    with urlopen(url) as response:
        body = response.read()
        result = json.loads(body)
        assert result['success'] is True
        if len(result['result']['records']) < 1:
            break
        df = pd.concat([df, pd.json_normalize(result['result']  ['records'])])
        url = url_base + result['result']['_links']['next']

## prepare dataframe
df.drop(['_id', 'ags2', 'rank'], axis=1, inplace=True)
#df.drop(['bl_hosp_fix', 'bl_hosp_adj', 'bl_hosp_inz_fix', 'bl_hosp_inz_adj', 'bl_hosp_adj_c95_ug', 'bl_hosp_adj_c95_og', 'bl_hosp_inz_adj_c95_ug', 'bl_hosp_inz_adj_c95_og'], axis=1,inplace=True)
df.rename(columns = cols_intensiv, inplace=True)
df.rename(columns = {'datum': 'Datum'}, inplace=True)
df.set_index('Datum', inplace=True)

# drop illegal values
df.replace(-99, np.nan, inplace=True)

# drop regional data
df.drop(['ags5', 'kreis'], axis=1, inplace=True)
print(df)
df.plot()
plt.show()

#drop age data
df_hospitalisierungen_gesamt = df.drop(list(df.filter(regex=r'.*-(Inzidenz|Fallzahl) Hospitalisierungen - .*')), axis=1)

# separate fallzahlen and inzidenz
df_hospitalisierungen_gesamt_fallzahlen = df_hospitalisierungen_gesamt.drop(list(df_hospitalisierungen_gesamt.filter(regex=r'Inzidenz')), axis=1);
df_hospitalisierungen_gesamt_inzidenz = df_hospitalisierungen_gesamt.drop(list(df_hospitalisierungen_gesamt.filter(regex=r'Fallzahl')), axis=1);

fig, axes = plt.subplots(nrows=2, ncols=1)
df_hospitalisierungen_gesamt_fallzahlen.plot(ax=axes[0])
df_hospitalisierungen_gesamt_inzidenz.plot(ax=axes[1])
plt.show()