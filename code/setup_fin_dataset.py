"""This file adds Total Net Family Income (TNFI) in 1979 to create income quartiles 
used in plots and analysis."""

# %%
# Import necessary packages
import os

import pandas as pd
import numpy as np

# %%
# Read in the dataset
fname = 'data/all-vars.pkl'
# Read in data for total net family income 
fname2 = 'data/TNFI_TRUNC_79.csv'
if not os.path.exists(fname):
     cwd = os.getcwd()
     os.chdir('C:/Users/bec10/OneDrive/Desktop/files/repos/aptitude-analysis/')
 
     os.chdir(cwd)

# %%
OBS_DATASET = pd.read_pickle(fname)
SURVEY_YEARS = OBS_DATASET['SURVEY_YEAR'].unique()
TNFI_79 = pd.read_csv(fname2)
TNFI_79['SURVEY_YEAR'] = 1978
OBS_DATASET = pd.merge(OBS_DATASET, TNFI_79, how='left', left_on=['IDENTIFIER', 'SURVEY_YEAR'],
                       right_on=['IDENTIFIER', 'SURVEY_YEAR'])

# %%
def get_dataset():
    """This function returns the observed dataset."""
    # Add a crude measure for a respondent's age, crude because month of the
    # interview may not directly align with month of birth.
    OBS_DATASET['AGE'] = OBS_DATASET['SURVEY_YEAR'] - OBS_DATASET['YEAR_OF_BIRTH']
    
    # Construct family income quartile variable
    trunc_data = OBS_DATASET.loc[OBS_DATASET['SURVEY_YEAR'] == 1978, ['TNFI_TRUNC']].dropna()

    trunc_data.replace(-3, np.nan)
    trunc_data.replace(-2, np.nan)
    trunc_data.replace(-1, np.nan)
    
    first_q = np.percentile(trunc_data, 25)
    second_q = np.percentile(trunc_data, 50)
    third_q = np.percentile(trunc_data, 75)

    OBS_DATASET['FAMILY_INCOME_QUARTILE'] = np.nan

    def func(x):
        if 'NaN' != x < first_q:
            return 'first quartile'
        elif first_q <= x < second_q:
            return 'second quartile'
        elif second_q <= x < third_q:
            return 'third quartile'
        elif third_q <= x != 'NaN':
            return 'fourth quartile'

    OBS_DATASET['FAMILY_INCOME_QUARTILE'] = OBS_DATASET['TNFI_TRUNC'].apply(func)

    # Construct categorical education variable
    def func(y):
        if y < 1:
            return 'less than hs'
        elif y == 1:
            return 'hs'
        elif y == 2:
            return 'assoc'
        elif 3 <= y <= 4:
            return 'college'
        elif 5 <= y <= 7:
            return 'beyond'

    OBS_DATASET['EDU_CATEGORY'] = OBS_DATASET['HIGHEST_DEGREE_RECEIVED'].apply(func)

    # Construct categorical parental education variables 
    def func(z):
        if z <= 11:
            return 'Less than HS'
        elif z >= 12:
            return 'HS or more'
    
    OBS_DATASET['MOTHER_EDU'] = OBS_DATASET['HIGHEST_GRADE_COMPLETED_MOTHER'].apply(func)
    OBS_DATASET['FATHER_EDU'] = OBS_DATASET['HIGHEST_GRADE_COMPLETED_FATHER'].apply(func)

    return OBS_DATASET

