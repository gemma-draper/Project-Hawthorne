#%%
import pandas as pd
import numpy as np
import json
#%%
# load the json.txt file into json_data 
with open('all_recipes_df_data.txt') as f:
    json_data = json.load(f)

# convert to a dataframe
df = pd.read_json(json_data, orient='columns')

# %%
# look at the data types and non-null count.
df.info()
# mostly type object, some float or int.
# no cols are entirely null

# %%
# inspect numeric cols
df.describe()
# inspect n_ratings values, which has a high max
df['n_ratings'].value_counts()
# check the high numbers of ratings are real.
df.loc[df['n_ratings'] > 1000]
# I looked at the webpages: they are real!
# %%
# inspect recipe_yield, also has a high max
df['recipe_yield'].value_counts()
# check the high numbers of ratings are real.
# lots with high numbers. 
# Looked one with 750, actually 750ml not 750 servings.

#%%
# Dropping this col for now.
# Will re-scrape this site to get the full string instead of stripping it.
df.drop('recipe_yield', inplace=True, axis=1)

# %%
# Null values currently set to None. Convert to np.NaN
df.fillna(value=np.nan, inplace=True)
#%%
df.head()
# %%
import psycopg2

conn = psycopg2.connect()

cursor = conn.cursor()
#%%
cursor.execute("CREATE TABLE all_recipes (id VARCHAR(4) PRIMARY KEY)")
conn.commit()

#%%

# create columns of the coresponding type for all columns in the dataframe
for col_name in df.columns:
if col_name == 'star_rating':
cursor.execute(f"ALTER TABLE all_recipes ADD COLUMN {col_name} NUMERIC(2,1)")
conn.commit()
elif col_name == 'n_ratings':
cursor.execute(f"ALTER TABLE all_recipes ADD COLUMN {col_name} NUMERIC(4)")
conn.commit()
else:
cursor.execute(f"ALTER TABLE all_recipes ADD COLUMN {col_name} TEXT")
conn.commit()

# %%
# create sqlalchemy engine to use with df.to_sql
from sqlalchemy import create_engine
engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}')

# add data to the postgres table
df.to_sql('all_recipes', engine, if_exists='append')

# %%

