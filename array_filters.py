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

# ### Data types
#
# A Pandas DF column is a pd.Series which are internally numpy arrays

import pandas as pd
import numpy as np

pd.Series([1, 2, 3]).values

# ### Binary Array arithmetik
#
# Build an array of `True`s and `False`s, one for each row in our dataframe. When we index our dataframe with this array, we get just the rows where our boolean array evaluated to `True`.  It's important to note that for row filtering by a boolean array the length of our dataframe's index must be the same length as the boolean array used for filtering. Binary-array-selection works with any numpy array.
#
# You can also combine more than one condition with the `&` operator

# +
### one dimension

# prepare array of alternating True and False as selector
l=6
select = np.arange(l) % 2 == 0
select
# -

target = np.linspace(10,l*10,l); target

# now select from target 
target[select]

# +
### two dimensions

# prepare some target with l * x dimensions
x = np.array(['a', 'b', 'c'], dtype=object)
target=np.outer(x, np.arange(l))
target = np.transpose(target)
target
# -

# now select from 2-dimensional target
target[select]
