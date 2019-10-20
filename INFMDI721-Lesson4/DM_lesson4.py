import pandas as pd
import requests
import json
import time

url = "https://raw.githubusercontent.com/fspot/INFMDI-721/master/lesson5/products.csv"
df = pd.read_csv(url, sep=';')

# Cleaning colonne price
df['price_corr'] = df['price'].str.split().str[0]
df['price_corr'] = pd.to_numeric(df.price_corr)
df['currency'] = df['price'].str.split().str[1]
df['currency'] = df['currency'].astype(str)
df['price'] = df['price_corr']
del df['price_corr']

# Taux de conversion avec API fixer.IO
fixerKey = 'e0195d4321648c53d6794f556b4d8f0f'
conv = requests.get("http://data.fixer.io/api/latest? access_key=" + fixerKey)

# Conversion en EURO
df['price_EUR'] = None
for index, row in df.iterrows():
    try:
        if df.loc[index, 'currency'] == 'nan':
            df.loc[index, 'currency'] = requests.get('http://www.geoplugin.net/json.gp?ip=' + row['ip_address'])\
                .json()['geoplugin_currencyCode']
            if df.loc[index, 'currency'] is not None:
                df.loc[index, 'price_EUR'] = round(row['price'] / conv.json()['rates'][df.loc[index, 'currency']], 2)
    except json.decoder.JSONDecodeError:
        df.loc[index, 'price_EUR'] = None
    time.sleep(1)

# Conversion des ingrédients en booléens
# Création des nouvelles colonnes d'ingrédients
ingredient_list = []
ingredient_list.extend(df.infos.str.split())
flat_ingredient_list = [item.strip(',:').lower() for sublist in ingredient_list for item in sublist]
ingredient_set = set(flat_ingredient_list)
ingredient_set -= {'may', 'ingredients', 'and', 'contain', 'contains'}
df = pd.concat([df, pd.DataFrame(columns=ingredient_set)], sort=False)
# Affectation des booléens
for ingredient in ingredient_set:
    df[ingredient] = df.infos.str.contains(ingredient)

del df['infos']
