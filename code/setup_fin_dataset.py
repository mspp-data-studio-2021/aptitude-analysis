"""This module adds Total Net Family Income (TNFI) in 1979 to create income quartiles 
used in plots and analysis."""
# %%
# Import necessary packages
import os

import pandas as pd
import numpy as np
from pathlib import Path

# %%
code_folder = Path(os.path.abspath(''))
print(code_folder)
project_dir = os.path.dirname(code_folder)
os.chdir(project_dir)
print(project_dir)

# %%
# Read in the dataset
fname = 'data/all-vars.pkl'
# Read in data for total net family income 
fname2 = 'data/TNFI_TRUNC_79.csv'
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

    return OBS_DATASET
# %%
