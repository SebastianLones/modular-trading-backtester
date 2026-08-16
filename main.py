import matplotlib.pyplot as plt
import numpy as np
from stock_data import stock_data
from strategy import backtest, strategy_1, strategy_2, strategy_3, strategy_4, strategy_5

strategy_compare = "n"
ticker = "msft"
stock_period = "1y"
initial_balance = 10000
trade_fee = 0.001

strategy_function = strategy_1

strategy_list = [strategy_1, strategy_2, strategy_3, strategy_4, strategy_5]

df_data = stock_data(ticker, stock_period)
df = backtest(df_data, initial_balance, trade_fee, strategy_function)

if strategy_compare == "y":
    plt.figure(figsize=(12,7))
    final_balances = {}
    pct_returns = {}
    for i in strategy_list:
        df_result = backtest(df_data, initial_balance, trade_fee, i)
        name = i.__name__.upper()
        final_balance = df_result["Current_Balance"].iloc[-1]
        pct_return = ((final_balance - initial_balance) / initial_balance) * 100
        final_balances[name] = final_balance
        pct_returns[name] = pct_return
        plt.plot(df_result["Date"], df_result["Current_Balance"], label=f"{name:<10} (${final_balance:.2f})")
    b_final = df_result["Buy and Hold"].iloc[-1]
    b_return = ((b_final - initial_balance) / initial_balance) * 100
    plt.plot(df_result["Date"], df_result["Buy and Hold"], label=f"Buy and Hold (${b_final:.2f})", color="black", linestyle="--")
    print("\n" + "=" * 50)
    print("              Strategy Comparison")
    print("-" * 50)
    print(f"Buy and Hold Final: ${b_final:.2f} ({b_return:+.2f}%)")
    print("-" * 50)
    for n in final_balances:
        print(f"{n}: ${final_balances[n]:.2f} ({pct_returns[n]:+.2f}%)")
    print("-" * 50)
    winner = max(final_balances, key=final_balances.get)
    print(f"Best Strategy: {winner}")
    print("=" * 50 + "\n")
    plt.xlabel("Date")
    plt.ylabel("Account Balance ($)")
    plt.title(f"{(ticker).upper()} Multi-Strategy Comparison")
    plt.legend()
    plt.grid(True)
    plt.show()

hb = df["Buy and Hold"].iloc[-1]
st = df["Current_Balance"].iloc[-1]

def sharpe_ratio(returns, periods=252):
    if returns.std() == 0:
        return 0
    return (returns.mean() / returns.std()) * np.sqrt(periods)

def max_drawdown(balance):
    running_max = balance.cummax()
    drawdown = (balance - running_max) / running_max
    return drawdown.min()

def results(hb, st, initial_balance, strategy_returns, strategy_balance):
    sharpe = sharpe_ratio(strategy_returns)
    mdd = max_drawdown(strategy_balance)
    print("\n" + "=" * 50)
    print("                    Results")
    print("-" * 50)
    print(f"Buy and Hold Final: ${hb:.2f} ({((hb - initial_balance) / initial_balance) * 100:+.2f}%)")
    print("-" * 50)
    print(f"Strategy Final: ${st:.2f} ({((st - initial_balance) / initial_balance) * 100:+.2f}%)")
    print(f"Strategy Sharpe Ratio: {sharpe:.2f}")
    print(f"Strategy Max Drawdown: {mdd * 100:.2f}%")
    print("-" * 50)  
    if st > hb:
        print("Strategy outperformed Buy and Hold")
    else:
        print("Buy and Hold outperformed Strategy")
    print("=" * 50 + "\n")

buys = df[df["Trigger"] == "Buy"]
sells = df[df["Trigger"] == "Sell"]

if strategy_compare == "n":
    results(hb, st, initial_balance, df["Return"], df["Current_Balance"])
    plt.figure(figsize=(10,6))
    plt.plot(df["Date"], df["Close"], label="Stock Price")
    if strategy_function == strategy_2:
        plt.plot(df["Date"], df["RSI"], label="RSI", color="purple")
        plt.axhline(70, linestyle="--", alpha=0.5, label="Overbought")
        plt.axhline(30, linestyle="--", alpha=0.5, label="Oversold")
    if strategy_function == strategy_1:
        plt.plot(df["Date"], df["SMA"], label="Short-Term Moving Average")
        plt.plot(df["Date"], df["LMA"], label="Long-Term Moving Average")
    if strategy_function == strategy_5:
        plt.plot(df["Date"], df["SEMA"], label="Short-Term Exponential Moving Average")
        plt.plot(df["Date"], df["LEMA"], label="Long-Term Exponential Moving Average")
    if strategy_function == strategy_3:
        plt.plot(df["Date"], df["BB_Upp"], label="Upper Band", linestyle=":")
        plt.plot(df["Date"], df["BB_Low"], label="Lower Band", linestyle=":")
    plt.scatter(buys["Date"], buys["Close"], marker="^", color="green", s=100, label="Buy Signal", zorder=5)
    plt.scatter(sells["Date"], sells["Close"], marker="v", color="red", s=100, label="Sell Signal", zorder=5)
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.title(f"{(ticker).upper()} Stock Price")
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10,6))
    plt.plot(df["Date"], df["Current_Balance"], label="Current Balance")
    plt.plot(df["Date"], df["Buy and Hold"], label="Buy and Hold")
    plt.xlabel("Date")
    plt.ylabel("Account Balance ($)") 
    plt.title(f"{(ticker).upper()} Stock Performance")
    plt.legend()
    plt.grid(True)
    plt.show()
