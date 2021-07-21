"""This script creates some informative graphs on subgroups of income quartile, gender, and race."""
# %%
import os
import matplotlib.pyplot as plt
import seaborn as sns

from setup_fin_dataset import get_dataset

# %%
os.chdir('C:/Users/bec10/OneDrive/Desktop/files/repos/gorman-earlyjobskills-analysis/out/heatmaps')

# %%
# Examine scores by income quartile
df = get_dataset()

ax = plt.figure().add_subplot(111)
for group in ['first quartile', 'second quartile', 'third quartile', 'fourth quartile']:
    cond = df['FAMILY_INCOME_QUARTILE'] == group
    dat = df.loc[df['SURVEY_YEAR'] == 1978, ['AFQT_RAW']].loc[cond].dropna()
    sns.distplot(dat, label=group.capitalize())

csfont = {'fontname':'Times New Roman'}
ax.yaxis.get_major_ticks()[0].set_visible(False)
ax.set_xlabel('AFQT Scores', **csfont)
ax.set_xlim([0, 120])
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('fig--income-quartile-afqt.png')


for score in ['ROTTER', 'ROSENBERG']:

    ax = plt.figure().add_subplot(111)
    for group in ['first quartile', 'second quartile', 'third quartile', 'fourth quartile']:
        label = score + '_SCORE'
        cond = df['FAMILY_INCOME_QUARTILE'] == group
        dat = df[cond].loc[df['SURVEY_YEAR'] == 1978, [label]].dropna()
        sns.distplot(dat, label=group)

    ax.set_xlabel(score.lower().capitalize() + ' Scores', **csfont)
    if score == 'ROTTER':
        plt.gca().invert_xaxis()
    ax.yaxis.get_major_ticks()[0].set_visible(False)
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.savefig('fig--income-quartile-' + score.lower() + '.png')

# %%
# Examine scores by gender
df = get_dataset()

ax = plt.figure().add_subplot(111)
for group in [1, 2]:
    cond = df['GENDER'] == group
    dat = df.loc[df['SURVEY_YEAR'] == 1978, ['AFQT_RAW']].loc[cond].dropna()
    sns.distplot(dat, label=group)

csfont = {'fontname':'Times New Roman'}

ax.yaxis.get_major_ticks()[0].set_visible(False)
ax.set_xlabel('AFQT Scores', **csfont)
ax.set_xlim([0, 120])
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('fig-aptitude-gender.png')

for score in ['ROTTER', 'ROSENBERG']:

    ax = plt.figure().add_subplot(111)
    for group in [1, 2]:
        label = score + '_SCORE'
        cond = df['GENDER'] == group
        dat = df[cond].loc[df['SURVEY_YEAR'] == 1978, [label]].dropna()
        sns.distplot(dat, label=group)

    ax.set_xlabel(score.lower().capitalize() + ' Scores', **csfont)
    if score == 'ROTTER':
        plt.gca().invert_xaxis()
    ax.yaxis.get_major_ticks()[0].set_visible(False)
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.savefig('fig-attitude-gender-' + score.lower() + '.png')


# %%
# Examine scores by race
df = get_dataset()

ax = plt.figure().add_subplot(111)
for group in [1, 2, 3]:
    cond = df['RACE'] == group
    dat = df.loc[df['SURVEY_YEAR'] == 1978, ['AFQT_RAW']].loc[cond].dropna()
    sns.distplot(dat, label=group)

csfont = {'fontname':'Times New Roman'}

ax.yaxis.get_major_ticks()[0].set_visible(False)
ax.set_xlabel('AFQT Scores', **csfont)
ax.set_xlim([0, 120])
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('fig-aptitude-race.png')

for score in ['ROTTER', 'ROSENBERG']:

    ax = plt.figure().add_subplot(111)
    for group in [1, 2]:
        label = score + '_SCORE'
        cond = df['GENDER'] == group
        dat = df[cond].loc[df['SURVEY_YEAR'] == 1978, [label]].dropna()
        sns.distplot(dat, label=group)

    ax.set_xlabel(score.lower().capitalize() + ' Scores', **csfont)
    if score == 'ROTTER':
        plt.gca().invert_xaxis()
    ax.yaxis.get_major_ticks()[0].set_visible(False)
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.savefig('fig-attitude-race-' + score.lower() + '.png')