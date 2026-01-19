import pandas as pd

print("=" * 60)
print("DATA STRUCTURE VERIFICATION")
print("=" * 60)

# Load market data
print("\nLoading market data...")
market_data = pd.read_csv('data/raw/market_data.csv', index_col=0)

print(f"\n1. Data Shape: {market_data.shape}")
print(f"   Rows (dates): {market_data.shape[0]}")
print(f"   Columns: {market_data.shape[1]}")

print("\n2. Column Structure:")
print(f"   Column names type: {type(market_data.columns)}")
print(f"   First 5 columns: {market_data.columns[:5].tolist()}")

print("\n3. First few rows:")
print(market_data.head())

print("\n4. Column levels:")
if isinstance(market_data.columns, pd.MultiIndex):
    print("   MultiIndex columns detected")
    print(f"   Level 0 (tickers): {market_data.columns.get_level_values(0).unique().tolist()}")
    print(f"   Level 1 (prices): {market_data.columns.get_level_values(1).unique().tolist()}")
else:
    print("   Single level columns")
    print(f"   All columns: {market_data.columns.tolist()}")

print("\n5. Index (dates):")
print(f"   First date: {market_data.index[0]}")
print(f"   Last date: {market_data.index[-1]}")
print(f"   Total dates: {len(market_data.index)}")

print("\n" + "=" * 60)