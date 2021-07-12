
"""This module creates figures that illustrate some basic relationships between labor market
outcomes (hourly wages) and measures of human capital."""
# %%
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from setup_plots import get_dataset

# %%
# Confirm the working directory
os.getcwd()

# %%
# Pull in the data
df = get_dataset()

# %%
df.shape
df.head()
df.columns
# %%

cond = df['AGE'].isin([18])
df = df[cond]

# %%
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
    ax.set_yticks(np.linspace(0.5, 3.5, 4))
    ax.set_yticklabels(range(1, 5))
    ax.set_ylabel('Hourly Wages (quartiles)')

    ax.set_xticks(np.linspace(0.5, 3.5, 4))
    ax.set_xticklabels(range(1, 5))
    ax.set_xlabel(ylabel + ' Scores (quartiles)')

    plt.savefig('fig-human-capital-' + parent.lower() + '.png')


# %%
