import numpy as np
import pandas as pd
import statsmodels
from model import finding_qualifying_equities
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller as adf

data = pd.read_csv("historical-data.csv")
volume_data = pd.read_csv("historical-volume-data.csv")

class Simulation(object):
    def __init__(self, days, money, reversion_time=5):
        self.days = int(days)
        self.money = money
        self.holding = False
        self.reversion_time = reversion_time
        self.current_day = 30
        self.info = None
        while self.current_day < self.days:
            if not self.holding:
                self.holding = finding_qualifying_equities(data[self.current_day-30:self.current_day], volume_data[self.current_day-30:self.current_day])
                self.info = self.buy(self.holding, self.money)
            else:
                if self.exit_position(self.MACD_signal_line(data, self.holding)):
                    self.money = self.sell(self.info)
                    print("Currently holding " + str(round(self.money, 2)) + ". Originally at " + str(round(money, 2)) + ".")
                    self.holding = False
            self.current_day += 1
        
        self.money = self.sell(self.info)
        print("Finished with " + str(round(self.money, 2)) + ". Originally at " + str(round(money, 2)) + ".")


    def buy(self, ticker, money):
        cost = data[ticker].iloc[self.current_day]
        bought_amount = money / cost
        print("Day " + str(self.current_day))
        print("Bought " + ticker + " at " + str(round(cost, 2)))
        return [ticker, cost, bought_amount]
    def sell(self, info):
        ticker = info[0]
        bought_cost = info[1]
        bought_amount = info[2]
        sold_cost = data[ticker].iloc[self.current_day]
        print("Day " + str(self.current_day))
        print("Sold " + ticker + " at " + str(round(sold_cost, 2)) + ". Earned/Lost " + str(round(sold_cost - bought_cost, 2) * bought_amount))
        return (sold_cost) * bought_amount
    def exit_position(self, lst):
        signal_line = lst[2]
        macd = lst[1]
        should_exit = False
        if signal_line.iloc[self.current_day] > macd.iloc[self.current_day]:
            should_exit = True
        return should_exit

    def MACD_signal_line(self, data, ticker):
        ticker_col = data[ticker]
        exp1 = ticker_col.ewm(span=12, adjust=False).mean()
        exp2 = ticker_col.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=9, adjust=False).mean()
        return [ticker, macd, signal_line]






            
        

Simulation(1215, 10000)




