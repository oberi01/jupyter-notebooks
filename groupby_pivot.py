# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ## Using Group By and Pivot

# + pycharm={"is_executing": false}
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# -

# ### Group By
# Can be used to create a plot for time series data 

# + pycharm={"is_executing": false}
# create a DataFrame containing monthly Data for three Persons, where data is incomplete for one person 
from pandas import DataFrame

df: DataFrame = pd.DataFrame({'M': ['jan', 'feb', 'mar', 'jan', 'feb', 'mar', 'jan', 'feb', ],
                              'P': ['eva'] * 3 + ['ed'] * 3 + ['mike'] * 2,
                              'C': np.random.randint(0, 101, 8),
                              'D': np.random.randint(0, 101, 8)})
df
# -

# get info about the dataframe
df.info()

# get statistics about number columns
df.describe()

# + pycharm={"is_executing": false}
# create a df indexed by Month - this will be the x-axis in a plot
dfm = df.set_index('M')
dfm[:5]
# -

# show info on index
dfm.index

# + pycharm={"is_executing": false}
### Plot trend for all P with one Metric C

# groupby yields a DataSeries, plotted as f(y=C,x=M) for all P, with plot arguments:
#  xticks provides labels for xaxis, todo: why is the 'mar' tick missing -incomplete data for mike?
gc = dfm.groupby('P', sort=False)['C']
gc.plot(title='Trend for C', legend=True, x='M', xticks=range(len(gc)));  # subplots=False, use_index=True)

# + pycharm={"is_executing": false}
# Grouping info is held in a dict exposed via .groups
gc.groups

# + pycharm={"is_executing": false}
### Plot trend for one P with all Metrics

# The index returned by groupby can be used with the iloc function:
dfm.iloc[gc.indices['ed']].plot(kind='bar', title='ed',xticks=range(len(gc)));
# -

# ### Pivot Table
# Although the former plot can be achieved by groupby there is the more specialized pivot_table which allows for reshaping data and easy plotting 

p1=df.pivot_table(index='M',columns=['P'],values='C')
p1.plot(kind='bar',xticks=range(len(p1)));

# More complex Dataframes can be reshaped and plotted:

# create a Dataframe containing monthly Data for three Persons with metricName N and metricData D
months = ['jan', 'feb', 'mar']
persons = ['eva'] * 3 + ['ed'] * 3 + ['mike'] * 3
df2 = pd.DataFrame({'M': months * 3 * 2,
                    'P': persons * 2,
                    'N': ['lunch'] * 3 * 3 + ['dinner'] * 3 * 3,
                    'D': np.random.randint(1, 11, 9 * 2)})
df2 = df2.set_index('M')
df2[7:12]

# reshape the Dataframe into 2-dim columns (Person, metricName) with values=metricData and Months as index
p2 = df2.pivot_table(index='M', columns=['P', 'N'], values='D')

p2.plot(kind='bar', legend=True, xticks=range(len(p2)));
