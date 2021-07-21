'''This module includes initial exploratory data analysis.
'''
# %%
# Import necessary packages 
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from setup_fin_dataset import SURVEY_YEARS
from setup_fin_dataset import get_dataset

# %%
# Raed in the data
df = get_dataset()

# %%
# Examine the shape of the dataframe
df.shape

# %%
# List the column names 
df.columns

#%%
# Check the datatypes for specific columns that will be used 
df[['IDENTIFIER', 'SURVEY_YEAR', 'RACE', 'AGE', 'GENDER', 'ROTTER_SCORE', 
'ROSENBERG_SCORE', 'AFQT_1', 'CPSOCC70', 'INCOME_WAGES_SALARY', 
'TYPE_WORK_LMT', 'HEALTH_INS', 'REGION', 'FAMILY_INCOME_QUARTILE']].dtypes

# %%
# Change the datatype of family income quartile to a string with max bytes 
df['FAMILY_INCOME_QUARTILE'] = df['FAMILY_INCOME_QUARTILE'].astype('|S')

# %%
# Change some columns to categorical 
df[['RACE', 'GENDER', 'TYPE_WORK_LMT', 'HEALTH_INS', 'REGION']] = (df[['RACE', 
'GENDER', 'TYPE_WORK_LMT', 'HEALTH_INS', 'REGION']].apply(pd.Categorical))

# %%
# Examine some summary statistics for the dataset for when participants are at early age
df2 = df[df['AGE'] == 23]
df2.head()

# %%
df2.shape

# %%
df2.describe()

# %%
# Examine summary statistics for 
df[['ROTTER_SCORE', 'ROSENBERG_SCORE', 'AFQT_1', 'INCOME_WAGES_SALARY', 'AGE']].describe()

# %%
# Examine 
df['RACE'].value_counts()

# %%
df['RACE'].value_counts(normalize=True)