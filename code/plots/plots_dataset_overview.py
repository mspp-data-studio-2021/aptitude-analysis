"""This file creates some basic figures describing the dataset."""
# %%
import os
from matplotlib import font_manager 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from mpl_toolkits.axisartist.axislines import Subplot

from setup_fin_dataset import SURVEY_YEARS
from setup_fin_dataset import get_dataset


# %%
def set_formatter(ax):
    """This function sets tick formatting for the plots"""
    formatter = matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))
    ax.get_yaxis().set_major_formatter(formatter)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# %%
df = get_dataset()
df

# %%
# Plot respondents' years of birth. For ease of interpretation visually, 
# remove years of birth with only a small number of individuals.
dat = df.loc[df['SURVEY_YEAR'] == 1978, 'YEAR_OF_BIRTH']
dat = dat.value_counts().to_dict()

for year in [1955, 1956, 1965]:
    del dat[year]

ax = plt.figure().add_subplot(111)
set_formatter(ax)

csfont = {'fontname':'Times New Roman'}

ax.set_ylabel('Number of Respondents', **csfont)
ax.set_xlabel('Year of Birth', **csfont)
ax.set_title('Figure 1. Respondents\' year of birth, NLSY79', **csfont)
ax.bar(dat.keys(), dat.values())

plt.savefig('fig1-dataset-basic-birth.png')


# %%
# Plot the number of observations over time.
num_obs = []
for year in SURVEY_YEARS:
    cond = df.loc[df['SURVEY_YEAR'] == year, 'IS_INTERVIEWED'].isin([True])
    num_obs += [df.loc[df['SURVEY_YEAR'] == year, 'IDENTIFIER'][cond].count()]

ax = plt.figure().add_subplot(111)
set_formatter(ax)

ax.bar(df['SURVEY_YEAR'].unique(), num_obs)

csfont = {'fontname':'Times New Roman'}

ax.set_ylabel('Number of Respondents', **csfont)
ax.set_xlabel('Year', **csfont)
ax.set_title('Figure 2. Number of respondents per year, NLSY79', **csfont)

plt.savefig('fig2-dataset-basic-observations.png')


# %%
# Plot the number of observations in each of the different samples 
# in the first year of the survey.
df['SAMPLE'] = df.loc[df['SURVEY_YEAR'] == 1978, 'SAMPLE_ID'].copy()
cond = df['SAMPLE_ID'].isin(range(9))
df.loc[cond, 'SAMPLE'] = 'Cross-sectional \nsample'

cond = df['SAMPLE_ID'].isin(range(9, 15))
df.loc[cond, 'SAMPLE'] = 'Supplemental \nsample'

cond = df['SAMPLE_ID'].isin(range(15, 21))
df.loc[cond, 'SAMPLE'] = 'Military \nsample' 

ax = plt.figure().add_subplot(111)
set_formatter(ax)

csfont = {'fontname':'Times New Roman'}

dat = df.loc[df['SURVEY_YEAR'] == 1978, 'SAMPLE'].astype('category')
dat = dat.value_counts().to_dict()

ax.bar(dat.keys(), dat.values())

ax.set_ylabel('Number of Respondents', **csfont)
ax.set_title('Figure 3. Independent probability samples, NLSY79 (1978)', **csfont)

plt.savefig('fig3-dataset-basic-samples.png')

# %%
# Plot income quartiles 
first_quartile = df.loc[df['FAMILY_INCOME_QUARTILE'] == 'first quartile', 'TNFI_TRUNC'].sum()
second_quartile = df.loc[df['FAMILY_INCOME_QUARTILE'] == 'second quartile', 'TNFI_TRUNC'].sum()
third_quartile = df.loc[df['FAMILY_INCOME_QUARTILE'] == 'third quartile', 'TNFI_TRUNC'].sum()
fourth_quartile = df.loc[df['FAMILY_INCOME_QUARTILE'] == 'fourth quartile', 'TNFI_TRUNC'].sum()

dat = [first_quartile, second_quartile, third_quartile, fourth_quartile]
labels = ['First quartile', 'Second quartile', 'Third quartile', 'Fourth quartile']
ax = plt.figure().add_subplot(111)
ax.bar(labels, dat)

csfont = {'fontname':'Times New Roman'}

ax.set_xlabel('Total unadjusted dollars', **csfont)
ax.set_xticks(labels)
ax.set_xticklabels(dat)
ax.set_title('Figure 4. Income quartiles, NLSY79 (1978)', **csfont)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('fig3-dataset-basic-inc-quartiles.png')


