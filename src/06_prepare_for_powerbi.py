import pandas as pd
import numpy as np

print("=" * 70)
print(" " * 15 + "PREPARING DATA FOR POWER BI")
print("=" * 70)

print("\nLoading data files...")
portfolio = pd.read_csv('portfolio_holdings.csv')
performance = pd.read_csv('data/processed/portfolio_performance.csv')
timeseries = pd.read_csv('data/processed/portfolio_timeseries.csv')
market_data = pd.read_csv('data/processed/market_data_clean.csv')
risk_metrics = pd.read_csv('data/processed/risk_metrics.csv')

print("\n1. Creating Date dimension table...")

timeseries['Date'] = pd.to_datetime(timeseries['Date'])
date_dim = pd.DataFrame({
    'Date': pd.date_range(start=timeseries['Date'].min(), 
                          end=timeseries['Date'].max(), 
                          freq='D')
})

date_dim['Year'] = date_dim['Date'].dt.year
date_dim['Month'] = date_dim['Date'].dt.month
date_dim['Month_Name'] = date_dim['Date'].dt.strftime('%B')
date_dim['Quarter'] = date_dim['Date'].dt.quarter
date_dim['Week'] = date_dim['Date'].dt.isocalendar().week
date_dim['Day_of_Week'] = date_dim['Date'].dt.day_name()
date_dim['Is_Weekend'] = date_dim['Date'].dt.dayofweek >= 5

print(f"   ✓ Created {len(date_dim)} date records")

print("\n2. Enhancing performance data...")

performance['Weight_Pct'] = (performance['Current_Value'] / performance['Current_Value'].sum()) * 100
performance['Gain_Loss_Label'] = performance['Unrealized_Gain'].apply(
    lambda x: 'Gain' if x > 0 else 'Loss'
)
performance['Performance_Category'] = pd.cut(
    performance['Unrealized_Gain_Pct'],
    bins=[-100, -10, 0, 10, 25, 50, 200],
    labels=['Large Loss', 'Small Loss', 'Small Gain', 'Moderate Gain', 'Good Gain', 'Excellent Gain']
)

performance['Risk_Category'] = pd.cut(
    performance['Current_Value'],
    bins=[0, 20000, 40000, 60000, 100000],
    labels=['Small', 'Medium', 'Large', 'Very Large']
)

print(f"   ✓ Enhanced {len(performance)} positions")

print("\n3. Creating daily returns table...")

timeseries['Date'] = pd.to_datetime(timeseries['Date'])
timeseries['Daily_Return_Pct'] = timeseries['Daily_Return'] * 100
timeseries['Portfolio_Gain_Loss'] = timeseries['Portfolio_Value'] - timeseries['Portfolio_Value'].iloc[0]
timeseries['Return_Category'] = timeseries['Daily_Return_Pct'].apply(
    lambda x: 'Positive' if x > 0 else 'Negative' if x < 0 else 'Flat'
)

print(f"   ✓ Created {len(timeseries)} daily records")

print("\n4. Creating asset class summary...")

asset_summary = performance.groupby('Asset_Class').agg({
    'Current_Value': 'sum',
    'Cost_Basis': 'sum',
    'Unrealized_Gain': 'sum',
    'Ticker': 'count'
}).reset_index()

asset_summary.columns = ['Asset_Class', 'Current_Value', 'Cost_Basis', 
                         'Unrealized_Gain', 'Number_of_Positions']
asset_summary['Weight_Pct'] = (asset_summary['Current_Value'] / 
                                asset_summary['Current_Value'].sum()) * 100
asset_summary['Return_Pct'] = (asset_summary['Unrealized_Gain'] / 
                                asset_summary['Cost_Basis']) * 100

print(f"   ✓ Created summary for {len(asset_summary)} asset classes")

print("\n5. Creating individual stock history...")

market_data['Date'] = pd.to_datetime(market_data['Date'])

stock_history = market_data.merge(
    portfolio[['Ticker', 'Shares', 'Purchase_Price', 'Purchase_Date', 'Asset_Name', 'Asset_Class']], 
    on='Ticker', 
    how='left'
)

stock_history['Position_Value'] = stock_history['Shares'] * stock_history['Close']
stock_history['Cost_Basis'] = stock_history['Shares'] * stock_history['Purchase_Price']
stock_history['Unrealized_Gain'] = stock_history['Position_Value'] - stock_history['Cost_Basis']
stock_history['Unrealized_Gain_Pct'] = (stock_history['Unrealized_Gain'] / 
                                        stock_history['Cost_Basis']) * 100

stock_history = stock_history.sort_values(['Ticker', 'Date'])
stock_history['Price_Change'] = stock_history.groupby('Ticker')['Close'].diff()
stock_history['Price_Change_Pct'] = stock_history.groupby('Ticker')['Close'].pct_change() * 100

print(f"   ✓ Created {len(stock_history)} stock history records")

print("\n6. Creating KPI summary...")

total_value = performance['Current_Value'].sum()
total_cost = performance['Cost_Basis'].sum()
total_gain = performance['Unrealized_Gain'].sum()
total_return_pct = (total_gain / total_cost) * 100

kpi_summary = pd.DataFrame([{
    'Metric_Name': 'Total Portfolio Value',
    'Metric_Value': total_value,
    'Metric_Format': 'Currency'
}, {
    'Metric_Name': 'Total Cost Basis',
    'Metric_Value': total_cost,
    'Metric_Format': 'Currency'
}, {
    'Metric_Name': 'Total Unrealized Gain',
    'Metric_Value': total_gain,
    'Metric_Format': 'Currency'
}, {
    'Metric_Name': 'Total Return',
    'Metric_Value': total_return_pct,
    'Metric_Format': 'Percentage'
}, {
    'Metric_Name': 'Number of Positions',
    'Metric_Value': len(performance),
    'Metric_Format': 'Number'
}, {
    'Metric_Name': 'Annualized Return',
    'Metric_Value': risk_metrics['Annualized_Return_Pct'].iloc[0],
    'Metric_Format': 'Percentage'
}, {
    'Metric_Name': 'Sharpe Ratio',
    'Metric_Value': risk_metrics['Sharpe_Ratio'].iloc[0],
    'Metric_Format': 'Number'
}, {
    'Metric_Name': 'Maximum Drawdown',
    'Metric_Value': risk_metrics['Max_Drawdown_Pct'].iloc[0],
    'Metric_Format': 'Percentage'
}])

print(f"   ✓ Created {len(kpi_summary)} KPI metrics")

print("\n" + "=" * 70)
print("Saving Power BI tables...")
print("=" * 70)

import os
os.makedirs('data/powerbi', exist_ok=True)

date_dim.to_csv('data/powerbi/dim_date.csv', index=False)
performance.to_csv('data/powerbi/fact_portfolio_performance.csv', index=False)
timeseries.to_csv('data/powerbi/fact_daily_portfolio.csv', index=False)
asset_summary.to_csv('data/powerbi/dim_asset_class.csv', index=False)
stock_history.to_csv('data/powerbi/fact_stock_history.csv', index=False)
kpi_summary.to_csv('data/powerbi/kpi_metrics.csv', index=False)

print("\n✓ Saved tables:")
print("  1. dim_date.csv                    - Date dimension table")
print("  2. fact_portfolio_performance.csv  - Current position performance")
print("  3. fact_daily_portfolio.csv        - Daily portfolio values")
print("  4. dim_asset_class.csv             - Asset class summary")
print("  5. fact_stock_history.csv          - Individual stock history")
print("  6. kpi_metrics.csv                 - Key metrics for KPI cards")

data_dict = """
DATA DICTIONARY FOR POWER BI
=============================

1. dim_date.csv - Date Dimension
   - Date: Date value
   - Year, Month, Quarter, Week: Time hierarchies
   - Month_Name: Full month name
   - Day_of_Week: Day name
   - Is_Weekend: Boolean flag

2. fact_portfolio_performance.csv - Current Holdings
   - Ticker: Stock symbol
   - Asset_Name: Full company/fund name
   - Asset_Class: Equity or ETF
   - Shares: Number of shares owned
   - Purchase_Price: Price per share at purchase
   - Current_Price: Latest market price
   - Cost_Basis: Total amount invested
   - Current_Value: Current market value
   - Unrealized_Gain: Profit/loss in dollars
   - Unrealized_Gain_Pct: Return percentage
   - Weight_Pct: Position weight in portfolio
   - Performance_Category: Performance bucket
   - Risk_Category: Position size category

3. fact_daily_portfolio.csv - Time Series Data
   - Date: Trading date
   - Portfolio_Value: Total portfolio value
   - Daily_Return: Daily return as decimal
   - Daily_Return_Pct: Daily return as percentage
   - Cumulative_Return: Running total return %
   - Drawdown: Current drawdown from peak
   - Peak: Highest portfolio value to date
   - Return_Category: Positive/Negative/Flat

4. dim_asset_class.csv - Asset Class Breakdown
   - Asset_Class: Equity or ETF
   - Current_Value: Total value by asset class
   - Cost_Basis: Total invested by asset class
   - Unrealized_Gain: Total gain by asset class
   - Number_of_Positions: Count of holdings
   - Weight_Pct: % of portfolio
   - Return_Pct: Return % by asset class

5. fact_stock_history.csv - Individual Stock Performance
   - Date: Trading date
   - Ticker: Stock symbol
   - Open, High, Low, Close, Volume: Daily OHLCV data
   - Shares: Number of shares owned
   - Position_Value: Daily position value
   - Unrealized_Gain: Daily profit/loss
   - Unrealized_Gain_Pct: Daily return %
   - Price_Change: Daily price change in $
   - Price_Change_Pct: Daily price change in %

6. kpi_metrics.csv - Dashboard KPIs
   - Metric_Name: KPI description
   - Metric_Value: Numeric value
   - Metric_Format: Display format (Currency/Percentage/Number)

RELATIONSHIPS TO CREATE IN POWER BI:
- fact_daily_portfolio[Date] → dim_date[Date]
- fact_stock_history[Date] → dim_date[Date]
- fact_stock_history[Ticker] → fact_portfolio_performance[Ticker]
"""

with open('data/powerbi/DATA_DICTIONARY.txt', 'w') as f:
    f.write(data_dict)

print("\n✓ Data dictionary saved: data/powerbi/DATA_DICTIONARY.txt")
print("\n" + "=" * 70)
print("✓ ALL DATA READY FOR POWER BI!")
print("=" * 70)
print("\nNext steps:")
print("1. Open Power BI Desktop")
print("2. Import all CSV files from data/powerbi/ folder")
print("3. Create relationships between tables")
print("4. Build your dashboard!")
print("\n")