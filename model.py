import numpy as np
import pandas as pd
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller as adf
import matplotlib.pyplot as plt
import statsmodels.tsa.vector_ar.vecm
from numpy import polyfit, sqrt, std, subtract, log
from scraper import yFinanceScraper

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
