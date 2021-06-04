import numpy as np
import pandas as pd
import yfinance as yf

if __name__ == "__main__":

    data = pd.read_csv("/Users/stephen/Desktop/Momentum Trading Project/ticker-names-on-NASDAQ-NYSE.csv")
    data = data[data["Volume"] > 1000000][data["IPO Year"] < 2010][data["Symbol"] != "AMHC"]["Symbol"]

    period = "1215"
    df = None
    for name in data:
        col = yf.Ticker(name).history(period=period+"d").loc[: , ["Close"]]
        col = col.rename(columns={"Date": "Date", "Close": name})
        if df is None:
            df = col
        else:
            df = df.join(col)

    #for storing testing data
    df.to_csv("/Users/stephen/Desktop/Momentum Trading Project/historical-data.csv")

"""
    #normalizing data
    for ticker in df:
        normalized_ticker_data = (df[ticker]-df[ticker].mean())/(df[ticker].std())
        df[ticker] = normalized_ticker_data

    df.to_csv("/Users/stephen/Desktop/Momentum Trading Project/normalized-historical-data.csv")
"""
