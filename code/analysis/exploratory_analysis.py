"""Exploratory Data Analysis. This module creates the values for Table 1 (summary statistics)."""

# %%
# Import necessary packages 
import os
import numpy as np
from pathlib import Path

# %%
# Set up folder path
code_folder = Path(os.path.abspath(''))
print(code_folder)
project_dir = os.path.dirname(code_folder)
os.chdir(project_dir)
print(project_dir)

# %%
# Import the (mostly) cleaned and formatted data 
from setup_fin_dataset import get_dataset
from setup_fin_dataset import OBS_DATASET

# %%
df = get_dataset()

# %%
# Examine the dataframe shape and columns
print(df.shape)
print(df.columns)

# %%
'''A bit of cleaning
'''
# Remove negative values in Total Net Family Income (TNFI) as they refer to non-responses.
df['TNFI_TRUNC'] = df['TNFI_TRUNC'].replace(-3, np.nan).replace(-2, np.nan).replace(-1, np.nan)

# %%
# Remove rows that don't have aptitude and attitude scores 
df.dropna(axis=0, how='any', subset=['AFQT_1','ROSENBERG_SCORE', 'ROTTER_SCORE'], inplace=True)
df.shape


# %%
# Examine distribution of age in 1978
df2 = df[df['SURVEY_YEAR'] == 1978]
df2.shape

# %%
# Double check to make sure all rows with null values were dropped 
df2[['AFQT_1','ROSENBERG_SCORE', 'ROTTER_SCORE']].isnull().sum()


# %%
# Examine the age distribution
df_age = df2.groupby('AGE')['IDENTIFIER'].nunique().sort_values(ascending=False)
df_age

# %%
'''SUMMARY STATISTICS TABLE
'''
# Summary statistics for age groups 
# Ages 14-17
df_1978_a = df[(df['SURVEY_YEAR']==1978) & (df['AGE']>=13) & (df['AGE']<=17)]
df_1978_a[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()

# %% 
# Ages 18-22
df_1978_b = df[(df['SURVEY_YEAR']==1978) & (df['AGE']>=18) & (df['AGE']<=22)]
df_1978_b[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()




# %%
# Summary statistics by gender 
df_male = df2[df2['GENDER']==1]
df_male[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()

# %%
df_female = df2[df2['GENDER']==2]
df_female[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()



# %%
# Summary stasticis by race 
df_hispanic = df2[df2['RACE']==1]
df_hispanic[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()

# %%
df_black = df2[df2['RACE']==2]
df_black[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()

# %%
df_non_hb = df2[df2['RACE']==3]
df_non_hb[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()




# %%
# Summary statistics by income quartile
df_q1 = df2[df2['FAMILY_INCOME_QUARTILE'].isin(['first quartile'])]
df_q1[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()

# %%
df_q2 = df2[df2['FAMILY_INCOME_QUARTILE'].isin(['second quartile'])]
df_q2[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()

# %%
df_q3 = df2[df2['FAMILY_INCOME_QUARTILE'].isin(['third quartile'])]
df_q3[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()

# %%
df_q4 = df2[df2['FAMILY_INCOME_QUARTILE'].isin(['fourth quartile'])]
df_q4[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()



# %%
# Examine parental education
df_mom_edu = df2.groupby('HIGHEST_GRADE_COMPLETED_MOTHER')['IDENTIFIER'].nunique().sort_values(ascending=False)
df_mom_edu

# %%
df_mom_edu = df2[df2['HIGHEST_GRADE_COMPLETED_MOTHER'] >= 12]
df_mom_edu[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()

# %%
df_mom_nedu = df2[df2['HIGHEST_GRADE_COMPLETED_MOTHER'] <= 11]
df_mom_nedu[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()


# %%
df_dad_edu = df2[df2['HIGHEST_GRADE_COMPLETED_FATHER'] >= 12]
df_dad_edu[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()

# %%
df_dad_nedu = df2[df2['HIGHEST_GRADE_COMPLETED_FATHER'] <= 11]
df_dad_nedu[['AFQT_1', 'ROSENBERG_SCORE', 'ROTTER_SCORE']].describe()


'''Re-construct income quartiles to get the range within each.
'''
# %%
print(OBS_DATASET)

# %%
# Construct family income quartile variable
trunc_data = OBS_DATASET.loc[OBS_DATASET['SURVEY_YEAR'] == 1978, ['TNFI_TRUNC']].dropna()

# %%
trunc_data.replace(-3, np.nan)
trunc_data.replace(-2, np.nan)
trunc_data.replace(-1, np.nan)

# %%
trunc_data.describe()

# %%
