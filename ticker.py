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
### Get stock ticker from yahoo,  plot chart, correlate stock 
# references
#   https://towardsdatascience.com/in-12-minutes-stocks-analysis-with-pandas-and-scikit-learn-a8d8a7b50ee7
#   https://towardsdatascience.com/a-beginners-guide-to-linear-regression-in-python-with-scikit-learn-83a8f7ae2b4f

import pandas as pd
import datetime
import pandas_datareader.data as web
from pandas import Series, DataFrame

# +
### Single stock operations

# Fill pandas data frame with Intel stock data for 1 jear 
start = datetime.datetime(2019, 2, 7)
end = datetime.datetime(2020, 2, 6)
ticker = 'INTC'
df = web.DataReader(ticker, 'yahoo', start, end)
df.tail()

# +
# Compute moving average and dividend ajustment
# adjustment reduces close_px by the divdend
# see: https://www.investopedia.com/terms/a/adjusted_closing_price.asp

adj = (df['Close'] - df['Adj Close'])
close_px = df['Adj Close']
avg = close_px.rolling(window=10).mean()

# +
# The data source does not include dividend info
# But it can be computed
# Note: only works if no stock splits or other company actions occurred

div_year=round(adj.sum()/100, 2)
close_at_div = round(df.Close[pd.DatetimeIndex(['2019-02-07'])].item(),2)
div_pct = round(100 * div_year / close_at_div, 2)
print('${}: dividend=${}, in pct={}'.format(close_at_div, div_year, div_pct))

# +
# Plot line chart with closing price, moving average and dividend adjustment
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib as mpl

mpl.rc('figure', figsize=(8, 7))
style.use('ggplot')

close_px.plot(label='Adj close')
(adj*10).plot(label='Adj*10')
avg.plot(label='Mavg')
plt.title('INTC')
plt.legend();

# +
### Multi stock operations

# Fill pandas data frame with 4 companies stock data for 1 jear 
dfcomp = web.DataReader(['AMD', 'INTC', 'AVGO', 'QCOM'],'yahoo',start=start,end=end)['Adj Close']
# -

# Show returns in percent of these companies stock
retscomp = dfcomp.pct_change()
retscomp[-3:].style.format({
    'AMD':  '{:,.2%}'.format,
    'INTC': '{:,.2%}'.format,
    'AVGO': '{:,.2%}'.format,
    'QCOM': '{:,.2%}'.format,
})

# Correlate these returns and plot them in a heat map
corr = retscomp.corr()
plt.imshow(corr, cmap='hot', interpolation='none')
plt.colorbar()
plt.xticks(range(len(corr)), corr.columns)
plt.yticks(range(len(corr)), corr.columns);

# Do a scatter plot for the "hottest" heat map entry
plt.scatter(retscomp.AMD, retscomp.AVGO)
plt.xlabel('Returns INTC')
plt.ylabel('Returns AVGO');

# Show Risk in a Scatter Plot
plt.scatter(retscomp.mean(), retscomp.std())
plt.xlabel('Expected returns')
plt.ylabel('Risk')
for label, x, y in zip(retscomp.columns, retscomp.mean(), retscomp.std()):
    plt.annotate(
        label, 
        xy = (x, y), xytext = (20, -20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
