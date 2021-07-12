"""This module creates some basic figures describing the dataset."""
# %%
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

from setup_plots import SURVEY_YEARS
from setup_plots import get_dataset

# %%
def set_formatter(ax):
    """This function sets formatting for the plots"""
    formatter = matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))
    ax.get_yaxis().set_major_formatter(formatter)

# %%
df = get_dataset()

# Plot the number of observations over time.
num_obs = []
for year in SURVEY_YEARS:
    cond = df.loc[df['SURVEY_YEAR'] == year, 'IS_INTERVIEWED'].isin([True])
    num_obs += [df.loc[df['SURVEY_YEAR'] == year, 'IDENTIFIER'][cond].count()]

ax = plt.figure().add_subplot(111)
set_formatter(ax)

ax.bar(df['SURVEY_YEAR'].unique(), num_obs)

ax.set_ylabel('Observations')
ax.set_xlabel('Year')

plt.savefig('fig-dataset-basic-observations.png')

# %%
# Plot gender of respondents
dat = df.loc[df['SURVEY_YEAR'] == 1978, 'GENDER'].astype('category')
dat = dat.cat.rename_categories({1: 'Male', 2: 'Female'})

ax = plt.figure().add_subplot(111)
ax.pie(dat.value_counts(normalize=True), labels=['Male', 'Female'], autopct='%1.1f%%')

plt.savefig('fig-dataset-basic-gender.png')

# %%
# Plot income quartiles of respondents
first_quartile = df.loc[df['FAMILY_INCOME_QUARTILE'] == 'first quartile', 'TNFI_TRUNC'].sum()
second_quartile = df.loc[df['FAMILY_INCOME_QUARTILE'] == 'second quartile', 'TNFI_TRUNC'].sum()
third_quartile = df.loc[df['FAMILY_INCOME_QUARTILE'] == 'third quartile', 'TNFI_TRUNC'].sum()
fourth_quartile = df.loc[df['FAMILY_INCOME_QUARTILE'] == 'fourth quartile', 'TNFI_TRUNC'].sum()
dat = [first_quartile, second_quartile, third_quartile, fourth_quartile]
ax = plt.figure().add_subplot(111)
ax.pie(dat, labels=['First quartile', 'Second quartile', 'Third quartile',
                    'Fourth quartile'], autopct='%1.1f%%')

plt.savefig('fig-dataset-basic-income-quartile.png')

# %%
# Plot respondents' years of birth. For ease of interpretation visually, 
# remove years of birth with only a small number of individuals.
dat = df.loc[df['SURVEY_YEAR'] == 1978, 'YEAR_OF_BIRTH']
dat = dat.value_counts().to_dict()

for year in [1955, 1956, 1965]:
    del dat[year]

ax = plt.figure().add_subplot(111)
set_formatter(ax)

ax.set_ylabel('Observations')
ax.set_xlabel('Year of Birth')

ax.bar(dat.keys(), dat.values())

plt.savefig('fig-dataset-basic-birth.png')

# %%
# Plot the relative shares of the different samples.
df['SAMPLE'] = df.loc[df['SURVEY_YEAR'] == 1978, 'SAMPLE_ID'].copy()
cond = df['SAMPLE_ID'].isin(range(9))
df.loc[cond, 'SAMPLE'] = 'Cross-sectional sample'

cond = df['SAMPLE_ID'].isin(range(9, 15))
df.loc[cond, 'SAMPLE'] = 'Supplementary sample'

cond = df['SAMPLE_ID'].isin(range(15, 21))
df.loc[cond, 'SAMPLE'] = 'Military sample'

ax = plt.figure().add_subplot(111)

dat = df.loc[df['SURVEY_YEAR'] == 1978, 'SAMPLE'].astype('category')

labels = ['Cross-sectional', 'Supplementary', 'Military']
ax.pie(dat.value_counts(normalize=True), labels=labels, autopct='%1.1f%%')
plt.savefig('fig-dataset-basic-samples.png')
