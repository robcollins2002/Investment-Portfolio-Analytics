import pandas as pd
import numpy as np

print("=" * 70)
print(" " * 20 + "PORTFOLIO PERFORMANCE ANALYSIS")
print("=" * 70)

print("\nLoading data...")
portfolio = pd.read_csv('portfolio_holdings.csv')
market_data = pd.read_csv('data/processed/market_data_clean.csv')

latest_date = market_data['Date'].max()
latest_prices = market_data[market_data['Date'] == latest_date].set_index('Ticker')

print(f"Valuation Date: {latest_date}")
print(f"Portfolio Holdings: {len(portfolio)} positions")

results = []

print("\n" + "=" * 70)
print("INDIVIDUAL POSITION ANALYSIS")
print("=" * 70)

for idx, holding in portfolio.iterrows():
    ticker = holding['Ticker']
    shares = holding['Shares']
    purchase_price = holding['Purchase_Price']
    purchase_date = holding['Purchase_Date']
    asset_name = holding['Asset_Name']
    
    current_price = latest_prices.loc[ticker, 'Close']
    
    cost_basis = shares * purchase_price
    current_value = shares * current_price
    unrealized_gain = current_value - cost_basis
    unrealized_gain_pct = (unrealized_gain / cost_basis) * 100
    
    days_held = (pd.to_datetime(latest_date) - pd.to_datetime(purchase_date)).days
    
    results.append({
        'Ticker': ticker,
        'Asset_Name': asset_name,
        'Asset_Class': holding['Asset_Class'],
        'Shares': shares,
        'Purchase_Date': purchase_date,
        'Purchase_Price': purchase_price,
        'Current_Price': current_price,
        'Cost_Basis': cost_basis,
        'Current_Value': current_value,
        'Unrealized_Gain': unrealized_gain,
        'Unrealized_Gain_Pct': unrealized_gain_pct,
        'Days_Held': days_held
    })
    
    print(f"\n{ticker} - {asset_name}")
    print(f"  {'Shares:':<20} {shares:>12,.0f}")
    print(f"  {'Purchase Price:':<20} ${purchase_price:>11,.2f}")
    print(f"  {'Current Price:':<20} ${current_price:>11,.2f}")
    print(f"  {'Purchase Date:':<20} {purchase_date:>12}")
    print(f"  {'Days Held:':<20} {days_held:>12,}")
    print(f"  {'-'*35}")
    print(f"  {'Cost Basis:':<20} ${cost_basis:>11,.2f}")
    print(f"  {'Current Value:':<20} ${current_value:>11,.2f}")
    print(f"  {'Unrealized Gain:':<20} ${unrealized_gain:>11,.2f}")
    print(f"  {'Return:':<20} {unrealized_gain_pct:>11,.2f}%")

results_df = pd.DataFrame(results)

print("\n" + "=" * 70)
print(" " * 25 + "PORTFOLIO SUMMARY")
print("=" * 70)

total_cost_basis = results_df['Cost_Basis'].sum()
total_current_value = results_df['Current_Value'].sum()
total_unrealized_gain = results_df['Unrealized_Gain'].sum()
total_unrealized_gain_pct = (total_unrealized_gain / total_cost_basis) * 100

print(f"\n{'Total Cost Basis:':<30} ${total_cost_basis:>15,.2f}")
print(f"{'Total Current Value:':<30} ${total_current_value:>15,.2f}")
print(f"{'Total Unrealized Gain:':<30} ${total_unrealized_gain:>15,.2f}")
print(f"{'Total Return:':<30} {total_unrealized_gain_pct:>14,.2f}%")

print("\n" + "=" * 70)
print("ASSET ALLOCATION (by Current Value)")
print("=" * 70)

allocation = results_df.groupby('Asset_Class').agg({
    'Current_Value': 'sum',
    'Unrealized_Gain': 'sum',
    'Cost_Basis': 'sum'
})
allocation['Weight'] = (allocation['Current_Value'] / total_current_value) * 100
allocation['Return_Pct'] = (allocation['Unrealized_Gain'] / allocation['Cost_Basis']) * 100

for asset_class, row in allocation.iterrows():
    print(f"\n{asset_class}:")
    print(f"  Value: ${row['Current_Value']:,.2f} ({row['Weight']:.1f}%)")
    print(f"  Gain: ${row['Unrealized_Gain']:,.2f} ({row['Return_Pct']:.2f}%)")

print("\n" + "=" * 70)
print("TOP 5 PERFORMERS (by % Return)")
print("=" * 70)
print(f"\n{'Ticker':<8} {'Asset Name':<30} {'Return %':>12} {'Gain ($)':>15}")
print("-" * 70)

top_5 = results_df.nlargest(5, 'Unrealized_Gain_Pct')
for idx, row in top_5.iterrows():
    print(f"{row['Ticker']:<8} {row['Asset_Name']:<30} {row['Unrealized_Gain_Pct']:>11,.2f}% ${row['Unrealized_Gain']:>13,.2f}")

print("\n" + "=" * 70)
print("BOTTOM 5 PERFORMERS (by % Return)")
print("=" * 70)
print(f"\n{'Ticker':<8} {'Asset Name':<30} {'Return %':>12} {'Gain ($)':>15}")
print("-" * 70)

bottom_5 = results_df.nsmallest(5, 'Unrealized_Gain_Pct')
for idx, row in bottom_5.iterrows():
    print(f"{row['Ticker']:<8} {row['Asset_Name']:<30} {row['Unrealized_Gain_Pct']:>11,.2f}% ${row['Unrealized_Gain']:>13,.2f}")

print("\n" + "=" * 70)
print("TOP 5 POSITIONS (by Current Value)")
print("=" * 70)
print(f"\n{'Ticker':<8} {'Asset Name':<30} {'Value':>15} {'% of Portfolio':>15}")
print("-" * 70)

top_positions = results_df.nlargest(5, 'Current_Value')
for idx, row in top_positions.iterrows():
    weight = (row['Current_Value'] / total_current_value) * 100
    print(f"{row['Ticker']:<8} {row['Asset_Name']:<30} ${row['Current_Value']:>13,.2f} {weight:>14,.2f}%")

results_df.to_csv('data/processed/portfolio_performance.csv', index=False)
print(f"\n{'='*70}")
print(f"✓ Performance report saved to: data/processed/portfolio_performance.csv")
print(f"{'='*70}\n")