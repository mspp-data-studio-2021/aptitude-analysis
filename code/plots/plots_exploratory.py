"""This script creates some informative graphs on subgroups of income quartile, gender, and race."""
# %%
import os
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# %%
# Set up folder path
code_folder = Path(os.path.abspath(''))
print(code_folder)
project_dir = os.path.dirname(code_folder)
os.chdir(project_dir)
print(project_dir)


# %%
from setup_fin_dataset import get_dataset


# %%
os.chdir(code_folder)
print(code_folder)



# %%
'''Plot scores by income quartile
'''
df = get_dataset()

#%%
df.dropna(axis=0, how='any', subset=['AFQT_1','ROSENBERG_SCORE', 'ROTTER_SCORE'], inplace=True)


# %%
ax = plt.figure().add_subplot(111)
for group in ['first quartile', 'second quartile', 'third quartile', 'fourth quartile']:
    cond = df['FAMILY_INCOME_QUARTILE'] == group
    dat = df.loc[df['SURVEY_YEAR'] == 1978, ['AFQT_1']].loc[cond].dropna()
    sns.distplot(dat, label=group.capitalize())

csfont = {'fontname':'Times New Roman'}
ax.yaxis.get_major_ticks()[0].set_visible(False)
ax.set_xlabel('AFQT Scores', **csfont)
ax.set_xlim([0, 120])
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('fig-inc-quartile-afqt.png')


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

    plt.savefig('fig-inc-quartile-' + score.lower() + '.png')



# %%
'''Plot scores by gender
'''
df = get_dataset()

#%%
df.dropna(axis=0, how='any', subset=['AFQT_1','ROSENBERG_SCORE', 'ROTTER_SCORE'], inplace=True)


ax = plt.figure().add_subplot(111)
for group in [1, 2]:
    cond = df['GENDER'] == group
    dat = df.loc[df['SURVEY_YEAR'] == 1978, ['AFQT_1']].loc[cond].dropna()
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
'''Plot scores by race
'''
df = get_dataset()

#%%
df.dropna(axis=0, how='any', subset=['AFQT_1','ROSENBERG_SCORE', 'ROTTER_SCORE'], inplace=True)


ax = plt.figure().add_subplot(111)
for group in [1, 2, 3]:
    cond = df['RACE'] == group
    dat = df.loc[df['SURVEY_YEAR'] == 1978, ['AFQT_1']].loc[cond].dropna()
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
    for group in [1, 2, 3]:
        label = score + '_SCORE'
        cond = df['RACE'] == group
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




# %%
'''Plot by parental educational attainment, mother
'''
df = get_dataset()

#%%
df.dropna(axis=0, how='any', subset=['AFQT_1','ROSENBERG_SCORE', 'ROTTER_SCORE'], inplace=True)

# %%
df['MOTHER_EDU'].nunique()

# %%
df['FATHER_EDU'].nunique()


# %%
df_mother = df.groupby('MOTHER_EDU')['IDENTIFIER'].nunique().sort_values(ascending=False)
df_mother

# %%
df_father = df.groupby('FATHER_EDU')['IDENTIFIER'].nunique().sort_values(ascending=False)
df_father



# %%

ax = plt.figure().add_subplot(111)
for group in ['Less than HS', 'HS or more']:
    cond = df['MOTHER_EDU'] == group
    dat = df['AFQT_1'].loc[cond].dropna()
    sns.distplot(dat, label=group)

csfont = {'fontname':'Times New Roman'}
ax.yaxis.get_major_ticks()[0].set_visible(False)
ax.set_xlabel('AFQT Scores', **csfont)
ax.set_xlim([0, 120])
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('fig-aptitude-mother-edu.png')

for score in ['ROTTER', 'ROSENBERG']:

    ax = plt.figure().add_subplot(111)
    for group in ['Less than HS', 'HS or more']:
        label = score + '_SCORE'
        cond = df['MOTHER_EDU'] == group
        dat = df[cond].loc[df['SURVEY_YEAR'] == 1978, [label]].dropna()
        sns.distplot(dat, label=group)

    ax.set_xlabel(score.lower().capitalize() + ' Scores', **csfont)
    if score == 'ROTTER':
        plt.gca().invert_xaxis()
    ax.yaxis.get_major_ticks()[0].set_visible(False)
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.savefig('fig-attitude-mother-edu-' + score.lower() + '.png')


# %%
'''Plot by parental educational attainment, father
'''
# %%
df = get_dataset()

#%%
df.dropna(axis=0, how='any', subset=['AFQT_1','ROSENBERG_SCORE', 'ROTTER_SCORE'], inplace=True)


ax = plt.figure().add_subplot(111)
for group in ['Less than HS', 'HS or more']:
    cond = df['FATHER_EDU'] == group
    dat = df['AFQT_1'].loc[cond].dropna()
    sns.distplot(dat, label=group)

csfont = {'fontname':'Times New Roman'}
ax.yaxis.get_major_ticks()[0].set_visible(False)
ax.set_xlabel('AFQT Scores', **csfont)
ax.set_xlim([0, 120])
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('fig-aptitude-father-edu.png')

for score in ['ROTTER', 'ROSENBERG']:

    ax = plt.figure().add_subplot(111)
    for group in ['Less than HS', 'HS or more']:
        label = score + '_SCORE'
        cond = df['FATHER_EDU'] == group
        dat = df[cond].loc[df['SURVEY_YEAR'] == 1978, [label]].dropna()
        sns.distplot(dat, label=group)

    ax.set_xlabel(score.lower().capitalize() + ' Scores', **csfont)
    if score == 'ROTTER':
        plt.gca().invert_xaxis()
    ax.yaxis.get_major_ticks()[0].set_visible(False)
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.savefig('fig-attitude-father-edu-' + score.lower() + '.png')
# %%
