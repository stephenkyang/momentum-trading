import numpy as np
import pandas as pd
import statsmodels
from model import bollinger_bands, finding_qualifying_equities
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller as adf

data = pd.read_csv("historical-data.csv")
#data = data.iloc[-303:]
volume_data = pd.read_csv("historical-volume-data.csv")
#volume_data = volume_data.iloc[-303:]
class Simulation(object):
    def __init__(self, days, money, reversion_time=5):
        self.days = int(days)
        self.money = money
        self.holding = False
        self.reversion_time = reversion_time
        self.current_day = 50
        self.info = None
        while self.current_day < self.days:
            if not self.holding:
                print("Day " + str(self.current_day))
                self.holding = finding_qualifying_equities(data[self.current_day-50:self.current_day], volume_data[self.current_day-30:self.current_day])
                self.info = self.buy(self.holding, self.money)
            else:
                if self.exit_position(self.MACD_signal_line(data, self.holding)):
                    print("Day " + str(self.current_day))
                    self.money = self.sell(self.info)
                    print("Currently holding " + str(round(self.money, 2)) + ". Originally at " + str(round(money, 2)) + ".")
                    self.holding = finding_qualifying_equities(data[self.current_day-50:self.current_day], volume_data[self.current_day-30:self.current_day])
                    self.info = self.buy(self.holding, self.money)
                else:
                    self.reversion_time -= 1
            self.current_day += 1
            
        
        self.money = self.sell(self.info)
        print("Finished with " + str(round(self.money, 2)) + ". Originally at " + str(round(money, 2)) + ".")


    def buy(self, ticker, money):
        cost = data[ticker].iloc[self.current_day]
        bought_amount = money / cost
        print("Bought " + ticker + " at " + str(round(cost, 2)))
        self.reversion_time = 5
        return [ticker, cost, bought_amount]

    def sell(self, info):
        ticker = info[0]
        bought_cost = info[1]
        bought_amount = info[2]
        sold_cost = data[ticker].iloc[self.current_day]
        print("Sold " + ticker + " at " + str(round(sold_cost, 2)) + ". Earned/Lost " + str(round((sold_cost - bought_cost)* bought_amount, 2))) 
        return (sold_cost) * bought_amount

    def exit_position(self, lst):
        signal_line = lst[2]
        macd = lst[1]
        should_exit = False
        if signal_line.iloc[self.current_day] < macd.iloc[self.current_day]:
            should_exit = True
            print("Crossed the signal line, selling " + self.info[0])
        elif self.info[1] > self.bollinger_bands(self.info[0])[0]:
            should_exit = True
            print("Exceeded 2 standard deviations above the mean, selling " + self.info[0])
        elif self.info[1] < self.bollinger_bands(self.info[0])[1]:
            print("Dipped .05 standard deviations below the mean, selling " + self.info[0])
            should_exit = True
        elif self.reversion_time <= 0:
            print("Reversion time exceeded, selling " + self.info[0])
            should_exit = True
        return should_exit

    def MACD_signal_line(self, data, ticker):
        ticker_col = data[ticker]
        exp1 = ticker_col.ewm(span=12, adjust=False).mean()
        exp2 = ticker_col.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=9, adjust=False).mean()
        return [ticker, macd, signal_line]


    def bollinger_bands(self, ticker):
        upper_bolli_band = data[ticker].iloc[self.current_day-50:self.current_day].mean() + data[ticker].iloc[self.current_day-50:self.current_day].std() * 1.5
        lower_bolli_band = data[ticker].iloc[self.current_day-50:self.current_day].mean() - data[ticker].iloc[self.current_day-50:self.current_day].std() * .05
        return [upper_bolli_band, lower_bolli_band]





            
        

Simulation(1215, 10000)




