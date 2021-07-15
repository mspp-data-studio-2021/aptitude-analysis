'''This module includes initial regression analyses.
'''
# %%
# Import necessary packages 
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from setup_plots import SURVEY_YEARS
from setup_plots import get_dataset

# %%
df = get_dataset()

# %%
# Create an instance of the class LinearRegression to represent the regression model.
model = LinearRegression()

# %%
df.columns

# %%
df2 = df[(df['SURVEY_YEAR'] == 1978) & (df['AGE'] == (18))]
df2



# %%
df['YEAR_OF_BIRTH'].unique

# %%
age50 = df.loc[df['SURVEY_YEAR'] == 2013, ['AGE'] == 53:56]
age50

# %%
cond = df['AGE'].isin([52])
print(cond)

# %%
df = df[cond]
print(df)

# %%
# Reshape the data for regression: the array for x is required to be two-dimentional,
# in other words, having one column with many rows. 
rotter_score = df['ROTTER_SCORE']
hourly_wages = df['WAGE_HOURLY_JOB_1'].dropna()

# %%
x = np.array(rotter_score).reshape((-1,1))
y = hourly_wages

# %%
model.fit(x,y)

# %%
np.any(np.isnan(hourly_wages))


# %%
np.all(np.isfinite(hourly_wages))

# %%
np.nan_to_num(hourly_wages)

# %%
model.fit(x,y)

# %%
np.where(np.isnan(hourly_wages))