"""This module contains some auxiliary functions shared across the figures.
First, read in the dataset and incorporate total net family income in past calendar year."""
# %%
import subprocess
import os

import pandas as pd
import numpy as np

# %%
os.getcwd()
os.chdir(r'c:/Users/bec10/OneDrive/Desktop/files/repos/gorman-earlyjobskills-analysis')


# %%
# Read in the dataset
fname = 'data/full-list-variables.pkl'
# Read in data for total net family income 
fname2 = 'data/input/TNFI_TRUNC_79.csv'
if not os.path.exists(fname):
    cwd = os.getcwd()
    os.chdir('data/')
 
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

    return OBS_DATASET