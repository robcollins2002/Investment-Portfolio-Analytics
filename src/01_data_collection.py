import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os

os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

print("Loading portfolio holdings...")
portfolio = pd.read_csv('portfolio_holdings.csv')
print(f"Portfolio loaded: {len(portfolio)} holdings")
print(portfolio[['Ticker', 'Asset_Name', 'Shares']])

tickers = portfolio['Ticker'].tolist()
print(f"\nTickers to fetch: {tickers}")

print("\nFetching market data from Yahoo Finance...")
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')

print("\nData collection complete!")
print(f"Date range: {start_date.date()} to {end_date.date()}")

print("\nSaving raw data...")
# Fixed: Add filename to the path
data.to_csv('data/raw/market_data.csv')
print("Saved to: data/raw/market_data.csv")

print("\nSample data for AAPL:")
if len(tickers) == 1:
    print(data.tail())
else:
    print(data['AAPL'].tail())

print("\n✓ Data collection successful!")