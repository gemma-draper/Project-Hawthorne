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

df.describe()
# %%
# look at the data types and non-null count.
df.info()
# mostly type object, some float or int.
# no cols are entirely null
# %%
# inspect n_ratings values
df['n_ratings'].value_counts()
# check the high numbers of ratings are real.
df.loc[df['n_ratings'] > 1000]
# I looked at the webpages: they are real!
# %%
