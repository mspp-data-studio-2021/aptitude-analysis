"""This file creates figures that illustrate some basic relationships between hourly wages
 and aptitude / attitude by gender."""
# %%
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from setup_fin_dataset import get_dataset

# %%
# change working directory to a separate folder for plots
os.chdir('out/heatmaps')

# %%
# Pull in the data
df = get_dataset()

'''First examine the basic relationship between aptitude / attitude scores
and hourly wages in later life for males
'''
# %%
# Filter by gender, males first 
df2 = df[df['GENDER'] == 1]
df2 

# %%
# Examine the basic relationship between aptitude / attitude scores and hourly wages at 47
cond = df2['AGE'].isin([47])
df2 = df2[cond]

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
    
    plt.savefig('fig-apt-att-male-47' + parent.lower() + '.png')


'''Next examine these relationships for females
'''
# %%
df = get_dataset()

# %%
# Filter for females
df2 = df[df['GENDER'] == 2]
df2 

# %%
cond = df2['AGE'].isin([47])
df2 = df2[cond]

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
    
    plt.savefig('fig-apt-att-female-47' + parent.lower() + '.png')
    
