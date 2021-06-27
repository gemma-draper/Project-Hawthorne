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
df.head()

# %%
