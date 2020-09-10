import pandas as pd
import pandas_ta as ta

import matplotlib.pyplot as plt

df = pd.read_csv('AAPL_OHLC.csv', index_col=0)
df_iv = pd.read_csv('AAPL_IV.csv', index_col=0)
df_hv = pd.read_csv('AAPL_HV.csv', index_col=0)

df1 = df.assign(IV=df_iv.close, HV=df_hv.close)
#df1.ta.ema(length=10, append=True)
#df1.ta.ema(length=20, append=True)
#df1.ta.sma(length=200, append=True)

#df1.ta.sma(length=200, append=True)


s=df1.ta.stoch()
ss=s.STOCHFk_14
ss.tail()

ss.ta.ema(length=3, append=True)

s.tail()

help(pd.DataFrame().ta)
pd.DataFrame().ta.indicators()
help(ta.stoch)


df.tail()
# Calculate Returns and append to the df DataFrame
df.ta.log_return(cumulative=True, append=True)
df.ta.percent_return(cumulative=True, append=True)

# New Columns with results
df.columns

# Take a peek
df.tail()
