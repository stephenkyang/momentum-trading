import numpy as np
import pandas as pd
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller as adf
import matplotlib.pyplot as plt
import statsmodels.tsa.vector_ar.vecm
from numpy import polyfit, sqrt, std, subtract, log
import numpy as np
from urllib.request import urlopen

num_data = pd.read_csv("historical-data.csv")

#data cleaning as the cointegration test can't have any NaN values
data = pd.read_csv("normalized-historical-data.csv")
data.iloc[0] = data.iloc[1]
data = data.fillna(method='ffill')


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
tradable_stocks = []
print(data["AAPL"].iloc[0:14].mean())
#print(data["AAPL"][50])
#the Richard Dreihaus strategy
def finding_qualifying_equities(data):
    # Divide the numerator (month end price of a stock - 50-day moving average price) by the 50-day moving average of the month end price.
    # A second filter was applied where the positive relative strength which is nothing but stocks having a 50% or more positive relative strength were chosen.
    data.reset_index(drop=True, inplace=True)
    for ticker in data:
        if ticker == "Date":
            continue
        if data[ticker][1] > data[ticker].iloc[2:50].mean():
            tradable_stocks.append(ticker) 
    return
finding_qualifying_equities(data) 
print(tradable_stocks)   
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
    exp3 = macd.ewm(span=9, adjust=False).mean()
    return ticker, macd, exp3

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



def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
        up = (up*(n-1)+upval)/n
        down = (down*(n-1)+downval)/n
        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)
    return rsi

#TODO
#Use forloop to parse through RSI, MACD, etc
