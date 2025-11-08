# Library importation
import pandas as pd
import numpy as np
import math as mt
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset
df = pd.read_csv("data/games.csv")
print(df.head(10))

# 1. Data Pre-processing
## 1.1 Column names of the dataset
new_col_names = []

for i in df.columns:
    i = i.lower()
    new_col_names.append(i)
    print(new_col_names)

df.columns = new_col_names

# Data info
df.info()

# Data description
df.describe(include = ['object'])

# User Score
df['user_score']

# Rating
df['rating']

## 1.2. Data Types correction
### 1.2.1 'year_of_release'
df['year_of_release'] = pd.to_numeric(df['year_of_release'], errors='coerce').astype('Int64')

### 1.2.2. 'user_score'
df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce').astype('float')

"""
Reasons why we change Data Type for 'user_score' and 'year_of_release' attributes
1. 'year_of_release': at first, the data type was 'float64', but it was changed to 'Int64' because it is a year, and it is not necessary to have decimals in years.
2. 'user_score': at first, the data type was 'object', but it was changed to 'float64' because it is a score, and it is necessary to have decimals in scores.
"""
## 1.3. Missing values
### 1.3.1. 'name'
df['name'].nunique()
'TBD' in df['name'].values
(df['name'].unique() == 'TBD').sum()
df['name'].isnull().sum()
print(df[df['name'].isnull()])

### 1.3.2. 'platform'
'TBD' in df['platform'].values
(df['platform'].unique() == 'TBD').sum()
df['platform'].isnull().sum()

### 1.3.3. 'year_of_release'
'TBD' in df['year_of_release'].values
(df['year_of_release'].unique() == 'TBD').sum()
df['year_of_release'].isnull().sum()
print(df[df['year_of_release'].isnull()])

def assign_year_of_release(row):
    parse_name = row['name'].split()
    for word in parse_name:
        if word.isdigit() and len(word) == 4:
            return int(word)
        elif word.isdigit() and len(word) == 2:
            if int(word) < 20:
                return int('20' + word)
            else:
                return int('19' + word)
        
mask = df['year_of_release'].isna() | (df['year_of_release'] == 0)
df.loc[mask, 'year_of_release'] = df.loc[mask].apply(assign_year_of_release, axis=1)

# Mapear cada juego a su año más común en otras plataformas
year_by_game = df.groupby('name')['year_of_release'].apply(
    lambda x: x.dropna().mode()[0] if not x.dropna().empty else np.nan
).to_dict()

# Rellenar NaN con el año del mismo juego en otra plataforma
mask_nan = df['year_of_release'].isna()
df.loc[mask_nan, 'year_of_release'] = df.loc[mask_nan, 'name'].map(year_by_game)

# Rellenar los NaN restantes con 0
df['year_of_release'] = df['year_of_release'].fillna(0).astype(int)

#df.fillna({'year_of_release': 0}, inplace=True)


### 1.3.4. 'genre'
'TBD' in df['genre'].values
df['genre'].nunique()
(df['genre'].unique() == 'TBD').sum()
df['genre'].isnull().sum()
print(df[df['genre'].isnull()])

#### Se eliminan los dos registros que no tienen 'genre', ya que coinciden que tampoco tienen 'name', 'critic_score', 'user_score', ni 'rating, además no tiene ventas muy altas
df.dropna(subset=['genre'], inplace=True)

### 1.3.5. 'na_sales'
'TBD' in df['na_sales'].values
(df['na_sales'].unique() == 'TBD').sum()

### 1.3.6. 'eu_sales'
'TBD' in df['eu_sales'].values
(df['eu_sales'].unique() == 'TBD').sum()

### 1.3.7. 'jp_sales'
'TBD' in df['jp_sales'].values
(df['jp_sales'].unique() == 'TBD').sum()

### 1.3.8. 'other_sales'
'TBD' in df['other_sales'].values
(df['other_sales'].unique() == 'TBD').sum()

### 1.3.9. 'critic_score'
'TBD' in df['critic_score'].values
(df['critic_score'].unique() == 'TBD').sum()


### 1.3.10. 'user_score'
'TBD' in df['user_score'].values
(df['user_score'].unique() == 'TBD').sum()

## 1.4. Additional columns
### 1.4.1. 'sales'
df['total_sales'] = df['na_sales'] + df['eu_sales'] + df['jp_sales'] + df['other_sales']

df.info()

df.to_csv('data/games_pre_cleaned.csv', index=False)


