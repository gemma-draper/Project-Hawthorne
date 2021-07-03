#%%
import nltk
import numpy as np
import pandas as pd
import psycopg2
import re
from sqlalchemy import create_engine
#%%
# get everything in the sql database as df
credentials = []
with open('credentials.txt','r') as f:
    credentials = eval(f.read())

for k,v in credentials.items(): 
    vars()[k] = v 

#%%
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
# %%
df = pd.read_sql_query("SELECT * FROM all_recipes", engine)

# %%
