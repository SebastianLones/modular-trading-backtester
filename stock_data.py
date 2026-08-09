import yfinance as yf
import pandas as pd

def stock_data(ticker, period):
    stock = yf.Ticker(ticker)
    historical = stock.history(period)
    df = historical[["Close"]].reset_index()
    df.columns = ["Date", "Close"]
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df

