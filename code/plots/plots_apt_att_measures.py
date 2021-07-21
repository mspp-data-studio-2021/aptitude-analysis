
"""This module creates figures that illustrate some basic relationships between labor market
outcomes (hourly wages) and aptitude / attitude."""
# %%
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from setup_fin_dataset import get_dataset

# %%
# Confirm the working directory
os.getcwd()

# %%
# change working directory to a separate folder for plots
os.chdir('C:/Users/bec10/OneDrive/Desktop/files/repos/gorman-earlyjobskills-analysis/out/heatmaps')

# %%
# Pull in the data
df = get_dataset()
df.columns 

# %%
# Check the values of the variable age 
# The oldest age that all respondents have data for in the dataset is 47
# The youngest age that all respondents have data for in the dataset is 22
df['AGE'].value_counts().sort_values(ascending=True)

# %%
# Examine the basic relationship between aptitude / attitude scores and hourly wages at 23
cond = df['AGE'].isin([23])
df = df[cond]

# Plot the relationships in heatmaps 
for parent in ['AFQT', 'ROSENBERG', 'ROTTER']:
    ax = plt.figure().add_subplot(111)

    if parent in ['AFQT']:
        label = 'AFQT_1'
        ylabel = 'AFQT'
    else:
        label = parent + '_SCORE'
        ylabel = parent.lower().capitalize()

    x = pd.qcut(df[label], 4, labels=False, duplicates="drop")
    y = pd.qcut(df['WAGE_HOURLY_JOB_1'], 4, labels=False, duplicates="drop")

    tab = pd.crosstab(y, x, normalize=True)
    tab = round(tab,2)
    hm = sns.heatmap(tab, cmap="Blues", vmin=0, vmax=0.15, annot=True)
    hm.invert_yaxis()

    csfont = {'fontname':'Times New Roman'}
    ax.set_yticks(np.linspace(0.5, 3.5, 4))
    ax.set_yticklabels(range(1, 5))
    ax.set_ylabel('Hourly Wages (quartiles)')



    ax.set_xticks(np.linspace(0.5, 3.5, 4))
    ax.set_xticklabels(range(1, 5))
    ax.set_xlabel(ylabel + ' Scores (quartiles)', **csfont)
    
    plt.savefig('fig-apt-att-23' + parent.lower() + '.png')

# %%
# Re-examine the relationship at a later age
df = get_dataset()

cond = df['AGE'].isin([47])
df = df[cond]

# Plot the relationships in heatmaps 
for parent in ['AFQT', 'ROSENBERG', 'ROTTER']:
    ax = plt.figure().add_subplot(111)

    if parent in ['AFQT']:
        label = 'AFQT_1'
        ylabel = 'AFQT'
    else:
        label = parent + '_SCORE'
        ylabel = parent.lower().capitalize()

    x = pd.qcut(df[label], 4, labels=False, duplicates="drop")
    y = pd.qcut(df['WAGE_HOURLY_JOB_1'], 4, labels=False, duplicates="drop")

    tab = pd.crosstab(y, x, normalize=True)
    tab = round(tab,2)
    hm = sns.heatmap(tab, cmap="Blues", vmin=0, vmax=0.15, annot=True)
    hm.invert_yaxis()

    csfont = {'fontname':'Times New Roman'}
    ax.set_yticks(np.linspace(0.5, 3.5, 4))
    ax.set_yticklabels(range(1, 5))
    ax.set_ylabel('Hourly Wages (quartiles)')


    ax.set_xticks(np.linspace(0.5, 3.5, 4))
    ax.set_xticklabels(range(1, 5))
    ax.set_xlabel(ylabel + ' Scores (quartiles)', **csfont)
    
    plt.savefig('fig-apt-att-47' + parent.lower() + '.png')

