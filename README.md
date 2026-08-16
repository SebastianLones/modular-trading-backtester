# Modular Trading Backtester

A Python framework for backtesting rule-based technical trading strategies against historical stock data, using buy-and-hold as a benchmark.

## Features

- Fetches historical stock price data using `yfinance`
- 5 built-in strategies: SMA Crossover, RSI Mean Reversion, Bollinger Bands, breakouts, EMA Crossover
- Vectorised backtest engine (pandas/numpy) - fee-aware, lookahead-bias-free
- Displays total returns, Sharpe ratio, max drawdown
- `matplotlib` charts: price with buy/sell signals, multi-strategy comparison, equity curve

## Project Structure

```
├── main.py         # config, runs the backtest, plots results
├── stock_data.py   # fetches historical price data
└── strategy.py     # backtest engine + strategy definitions
```

## Installation

```bash
git clone https://github.com/sebastianlones/modular-trading-backtester.git
cd modular-trading-backtester
pip install -r requirements.txt
```

## Usage

All settings are controlled in lines 6-12 of `main.py` - the values can be edited here.

```python
strategy_compare = "n"           # "y" to compare all 5 strategies, "n" for a single strategy
ticker = "msft"                  # any valid Yahoo Finance ticker symbol
stock_period = "1y"              # time period to fetch data for, e.g. "1y" or "1m"
initial_balance = 10000          # starting account balance in $
trade_fee = 0.001                # trading fee per buy/sell, as a decimal

strategy_function = strategy_1   # which strategy to run when strategy_compare == "n"
```

Once configured, run:

```bash
python main.py
```

- **`strategy_compare = "n"`** — runs `strategy_function` only. Prints final balance, % return, Sharpe ratio, and max drawdown vs. buy-and-hold, then displays a price chart with the specific overlay for the strategy selected with buy/sell indicators, and an equity curve.
- **`strategy_compare = "y"`** — runs all 5 strategies on the same data and plots them together on one equity curve chart, ranked by final balance, alongside the buy-and-hold benchmark.

To switch strategies, change `strategy_function` to any of the built-in strategies in `strategy.py` e.g. `strategy_1`.

## Requirements

```
yfinance
pandas
numpy
matplotlib
```
