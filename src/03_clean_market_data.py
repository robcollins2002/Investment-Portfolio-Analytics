import pandas as pd
import numpy as np

print("=" * 60)
print("CLEANING MARKET DATA")
print("=" * 60)

print("\nLoading raw market data...")
market_data = pd.read_csv('data/raw/market_data.csv')

print(f"Original shape: {market_data.shape}")

date_column = market_data.iloc[2:, 0].values 

tickers = []
for col in market_data.columns:
    if col not in ['Ticker', 'Price', 'Date', 'Unnamed: 0']:
        base_ticker = col.split('.')[0]
        if base_ticker not in tickers:
            tickers.append(base_ticker)

print(f"\nFound {len(tickers)} tickers: {tickers}")

cleaned_data = []

print("\nRestructuring data...")

for i, date in enumerate(date_column):
    row_idx = i + 2 
    
    if pd.notna(date):
        for ticker in tickers:

            ticker_cols = [col for col in market_data.columns if col == ticker or col.startswith(ticker + '.')]
            
            if len(ticker_cols) >= 5:
                try:
                    open_val = market_data.iloc[row_idx][ticker_cols[0]]
                    high_val = market_data.iloc[row_idx][ticker_cols[1]]
                    low_val = market_data.iloc[row_idx][ticker_cols[2]]
                    close_val = market_data.iloc[row_idx][ticker_cols[3]]
                    volume_val = market_data.iloc[row_idx][ticker_cols[4]]
                    
                    if pd.notna(close_val):
                        cleaned_data.append({
                            'Date': str(date),
                            'Ticker': ticker,
                            'Open': float(open_val),
                            'High': float(high_val),
                            'Low': float(low_val),
                            'Close': float(close_val),
                            'Volume': float(volume_val)
                        })
                except Exception as e:
                    continue

cleaned_df = pd.DataFrame(cleaned_data)

if len(cleaned_df) > 0:
    print(f"\n✓ Cleaned data shape: {cleaned_df.shape}")
    print(f"✓ Date range: {cleaned_df['Date'].min()} to {cleaned_df['Date'].max()}")
    print(f"✓ Tickers: {sorted(cleaned_df['Ticker'].unique().tolist())}")
    
    print("\nSample of cleaned data:")
    print(cleaned_df.head(15))

    cleaned_df.to_csv('data/processed/market_data_clean.csv', index=False)
    print(f"\n✓ Cleaned data saved to: data/processed/market_data_clean.csv")
    
    print("\n" + "=" * 60)
    print("DATA QUALITY CHECK")
    print("=" * 60)
    
    for ticker in sorted(cleaned_df['Ticker'].unique()):
        ticker_data = cleaned_df[cleaned_df['Ticker'] == ticker]
        latest_row = ticker_data.iloc[-1]
        print(f"{ticker:6} - {len(ticker_data):3} records | Latest: ${latest_row['Close']:8.2f} on {latest_row['Date']}")
    
    print("\n✓ Data cleaning complete!")
else:
    print("\n❌ No data was extracted. Debugging info:")
    print(f"Date column sample: {date_column[:5]}")
    print(f"Number of rows: {len(date_column)}")

    print("\nSample row for AAPL:")
    aapl_cols = [col for col in market_data.columns if col == 'AAPL' or col.startswith('AAPL.')]
    print(market_data.iloc[2][aapl_cols])