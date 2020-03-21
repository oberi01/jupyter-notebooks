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

# +
### Plot stacked bar data read from csv file

# Render plots inline
# %matplotlib inline
from os.path import expandvars
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (15, 5)

# change dir to jupyter project folder
import os
os.chdir(expandvars('$HOME/gitwork/github/jupyter-notebooks'))
# -

df = pd.read_csv('./data/fnbp2.csv', encoding='latin1', sep=';', 
                 parse_dates=['date'], index_col='date' ) # usecols=

# Show the first rows
df[:3]

df.plot.bar(stacked=True, color=['green','blue','red','lightgrey']);
