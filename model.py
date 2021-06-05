import numpy as np
import pandas as pd
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller as adf
import matplotlib.pyplot as plt
import statsmodels.tsa.vector_ar.vecm
from numpy import polyfit, sqrt, std, subtract, log
import numpy as np
import yfinance as yf

#data cleaning as the cointegration test can't have any NaN values
data = pd.read_csv("historical-data.csv")
data.iloc[0] = data.iloc[1]
data = data.fillna(method='ffill')
volume = pd.read_csv("historical-volume-data.csv")

# Code should do the following:
#   1. Selection, or what equities you choose
#       Using RSI, moving average, and momentum indicator to find eligible equities (Moving Average Convergence Divergence)
#   2. Calculating risk
#   3. Take a wide spread of positions
#   4. When to exit position

# Selection
# 1. Is the price from today higher than the price from 200 days ago?
# 2. Checking Hurst exponent (if it is > than .5 then it wont mean revert)
# 3. Find the RSI of the stock (higher than 55 lower than 70)

# Calculating Risk
# 1. Look into MACD(and the trigger line), RSI, Percentage Price Oscillator

# Exit Positions when
# Stock goes below 5% of the initial buying price (Loss)
# Stock goes above 1 SD above the bolinger band? (Gain)
# Initial assumptions are wrong (MACD's trigger line is crossed, RSI reverses trend, etc)



def bollinger_bands(pair,days = 200):
    combined_z_scores = (data[pair[0]].iloc[-days:-1] + data[pair[1]].iloc[-days:-1]) / 2
    upper_bolli_band = combined_z_scores + combined_z_scores.std() * 2
    lower_bolli_band = combined_z_scores - combined_z_scores.std() * 2
    return [upper_bolli_band, combined_z_scores, lower_bolli_band]


def MACD_signal_line(data, ticker):
    ticker_col = data[ticker]
    exp1 = ticker_col.ewm(span=12, adjust=False).mean()
    exp2 = ticker_col.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=9, adjust=False).mean()
    return [ticker, macd, signal_line]

def RSI(series, period=14):
    delta = series.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
    u = u.drop(u.index[:(period-1)])
    d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
    d = d.drop(d.index[:(period-1)])
    rs = pd.DataFrame.ewm(u, com=period-1, adjust=False).mean() / \
         pd.DataFrame.ewm(d, com=period-1, adjust=False).mean()
    return 100 - 100 / (1 + rs)


def finding_qualifying_equities(data):
    # if the stock price is higher than its 50-day average
    # RSI of 50 or higher
    #MACD is 4% higher than the 50-day average
    # volume is 4% higher than the previous day
    volume_map = {}
    data.reset_index(drop=True, inplace=True)
    for ticker in data:
        if ticker == "Date":
            continue
        if data[ticker].iloc[-1] > data[ticker].iloc[-49:-2].mean():
            macd = MACD_signal_line(data, ticker)[1]
            if macd.iloc[-1] >= macd.iloc[-49:-2].mean() * 1.04:
                ticker_api = yf.Ticker(ticker)
                ticker_volume = volume
                ticker_volume = ticker_volume.reset_index()
                if not ticker_volume.empty and ticker_volume[ticker].iloc[-1] >= ticker_volume[ticker].iloc[-2] * 1.04:
                    ticker_open = data[ticker].iloc[-20:-1]
                    if RSI(ticker_open).iloc[-1] > 50:
                        volume_map[ticker_volume[ticker].iloc[-1]] = ticker

    return volume_map[max(volume_map.keys())]

print(finding_qualifying_equities(data))



def MACD_plot(ticker, macd, exp3):
    macd.plot(label=ticker + 'MACD', color='g')
    ax = exp3.plot(label='Signal Line', color='r')
    ticker.plot(ax=ax, secondary_y=True, label='AAPL')
    ax.set_ylabel('MACD')
    ax.right_ax.set_ylabel('Price $')
    ax.set_xlabel('Date')
    lines = ax.get_lines() + ax.right_ax.get_lines()
    ax.legend(lines, [l.get_label() for l in lines], loc='upper left')
    plt.show()


#TODO
#Use forloop to parse through RSI, MACD, etc
