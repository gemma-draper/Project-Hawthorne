#%%
from nltk import ngrams
import numpy as np
import pandas as pd
import psycopg2
import re
from sqlalchemy import create_engine

"""
Get all from all_recipes table.
Returns a pandas DataFrame.
Requires credentials.txt file in the same dir with database credentials.

"""
credentials = []
with open('credentials.txt','r') as f:
    credentials = eval(f.read())

# unpack credentials dict into variables
for k,v in credentials.items(): 
    vars()[k] = v 

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
df = pd.read_sql_query("SELECT * FROM all_recipes", engine)


df.set_index('id', inplace=True)

# filter df ingredient cols
ingredient_df = df.filter(like="ingredient", axis=1)


# add all the ingredients to a list
ingredients_list = []
for col in ingredient_df.columns:
    ingredients_list += ingredient_df[col].to_list()

# remove nulls
ingredients_list = [ele for ele in ingredients_list if ele]

#%%

tokens = []
for element in ingredients_list:
    gram = ngrams(element.split(), n=1)  
    tokens.extend(element.split())

# remove non alpha-numeric characters, like trade marks and hyphens
tokens = [re.sub("[^a-zA-Z0-9]","",token) for token in tokens]
# remove rows which contain numbers
def has_numbers(input):
    return any(char.isdigit() for char in input)
tokens = [token for token in tokens if not has_numbers(token)]

word_freq = {}
for token in tokens:
    if token not in word_freq.keys():
        word_freq[token] = 1
    else:
        word_freq[token] += 1

# %%
# things to do
# remove special characters and punctuation from strings
# make a bigram
# remove strings containing numbers
# make everything lower case 
