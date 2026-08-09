import numpy as np
import pandas as pd

def backtest(df_data, initial_balance, fee_rate, strategy_function):
    raw_pct = df_data["Close"].pct_change().fillna(0)
    master_b = initial_balance * (raw_pct + 1).cumprod()
    df = strategy_function(df_data)
    df["PCT_Change"] = df["Close"].pct_change()
    df = df.dropna(subset=["Position"]).reset_index(drop=True)
    df = df.dropna(subset=["PCT_Change"]).reset_index(drop=True)
    pos_y = df["Position"].shift(1)
    pos_y.iloc[0] = 0
    df["Trigger"] = np.select([(df["Position"] == 1) & (pos_y == 0), (df["Position"] == 0) & (pos_y == 1)], ["Buy", "Sell"], default="Hold")
    df["Return"] = (pos_y * (df["PCT_Change"])).fillna(0)
    df["Fees"] = np.where(df["Trigger"].isin(["Buy", "Sell"]), 1 - fee_rate, 1)
    df["Current_Balance"] = initial_balance * ((df["Return"] + 1) * df["Fees"]).cumprod()
    df["Buy and Hold"] = master_b.iloc[-len(df):].reset_index(drop=True)
    return df

def strategy_1(df, SMA=9, LMA=21):
    df = df.copy()
    df["SMA"] = df["Close"].rolling(window=SMA).mean()
    df["LMA"] = df["Close"].rolling(window=LMA).mean()
    df["Position"] = np.where(df["SMA"] > df["LMA"], 1, 0)
    df.loc[df["LMA"].isna(), "Position"] = np.nan
    return df

def strategy_2(df, period=14, os=30, ob=70):
    df = df.copy()
    change = df["Close"].diff()
    df["gain"] = np.where(change > 0, change, 0.0)
    df["loss"] = np.where(change < 0, -change, 0.0)  
    df["avg_gain"] = df["gain"].rolling(window=period).mean()
    df["avg_loss"] = df["loss"].rolling(window=period).mean()
    rs = df["avg_gain"] / (df["avg_loss"] + 1e-10)
    df["RSI"] = 100 - (100 / (1 + rs))
    df["Point"] = np.nan
    df.loc[df["RSI"] < os, "Point"] = 1
    df.loc[df["RSI"] > ob, "Point"] = 0
    df["Position"] = df["Point"].ffill().fillna(0).astype(int)
    df.loc[df["RSI"].isna(), "Position"] = np.nan
    df = df.drop(columns=["gain", "loss", "avg_gain", "avg_loss"])
    return df

def strategy_3(df, window=20, num_std=2):
    df = df.copy()
    df["BB_Mid"] = df["Close"].rolling(window=window).mean()
    df["BB_Std"] = df["Close"].rolling(window=window).std()
    df["BB_Upp"] = df["BB_Mid"] + (num_std * df["BB_Std"])
    df["BB_Low"] = df["BB_Mid"] - (num_std * df["BB_Std"])
    close_y = df["Close"].shift(1)
    df["Point"] = np.nan
    df.loc[close_y < df["BB_Low"].shift(1), "Point"] = 1
    df.loc[close_y > df["BB_Upp"].shift(1), "Point"] = 0
    df["Position"] = df["Point"].ffill().fillna(0).astype(int)
    df.loc[df["BB_Mid"].isna(), "Position"] = np.nan
    return df

def strategy_4(df, buy_window=20, sell_window=10):
    df = df.copy()
    df["High"] = df["Close"].rolling(window=buy_window).max().shift(1)
    df["Low"] = df["Close"].rolling(window=sell_window).min().shift(1)
    close_y = df["Close"].shift(1)
    df["Point"] = np.nan
    df.loc[close_y >= df["High"], "Point"] = 1
    df.loc[close_y <= df["Low"], "Point"] = 0
    df["Position"] = df["Point"].ffill().fillna(0).astype(int)
    df.loc[df["High"].isna(), "Position"] = np.nan
    return df

def strategy_5(df, SEMA=9, LEMA=21):
    df = df.copy()
    df["SEMA"] = df["Close"].ewm(span=SEMA, adjust=False).mean()
    df["LEMA"] = df["Close"].ewm(span=LEMA, adjust=False).mean()
    df["Position"] = np.where(df["SEMA"] > df["LEMA"], 1, 0)
    return df