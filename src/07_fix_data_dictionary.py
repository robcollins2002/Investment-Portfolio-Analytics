import os

print("Creating data dictionary...")

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
- fact_daily_portfolio[Date] --> dim_date[Date]
- fact_stock_history[Date] --> dim_date[Date]
- fact_stock_history[Ticker] --> fact_portfolio_performance[Ticker]
"""

with open('data/powerbi/DATA_DICTIONARY.txt', 'w', encoding='utf-8') as f:
    f.write(data_dict)

print("✓ Data dictionary saved successfully!")
print("\n" + "=" * 70)
print("✓ ALL DATA READY FOR POWER BI!")
print("=" * 70)
print("\nYou now have 6 tables ready to import:")
print("  1. dim_date.csv")
print("  2. fact_portfolio_performance.csv")
print("  3. fact_daily_portfolio.csv")
print("  4. dim_asset_class.csv")
print("  5. fact_stock_history.csv")
print("  6. kpi_metrics.csv")
print("\nLocation: data/powerbi/")
print("\n" + "=" * 70)