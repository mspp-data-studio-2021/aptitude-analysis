"""Exploratory Data Analysis 
"""
# %%
# Import necessary packages 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


from setup_fin_dataset import SURVEY_YEARS
from setup_fin_dataset import get_dataset

df = pd.read_pickle('../data/output/original.pkl')
SURVEY_YEAR = df['SURVEY_YEAR'].unique()
df.head(10)
