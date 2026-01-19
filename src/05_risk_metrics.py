import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print(" " * 20 + "PORTFOLIO RISK ANALYSIS")
print("=" * 70)

portfolio = pd.read_csv('portfolio_holdings.csv')
market_data = pd.read_csv('data/processed/market_data_clean.csv')
performance = pd.read_csv('data/processed/portfolio_performance.csv')

market_data['Date'] = pd.to_datetime(market_data['Date'])
market_data = market_data.sort_values('Date')

print(f"\nAnalyzing data from {market_data['Date'].min().date()} to {market_data['Date'].max().date()}")

print("\nCalculating historical portfolio values...")

dates = sorted(market_data['Date'].unique())

portfolio_values = []

for date in dates:
    daily_data = market_data[market_data['Date'] == date]
    
    total_value = 0
    for idx, holding in portfolio.iterrows():
        ticker = holding['Ticker']
        shares = holding['Shares']
        purchase_date = pd.to_datetime(holding['Purchase_Date'])
        
        if date >= purchase_date:
            ticker_price = daily_data[daily_data['Ticker'] == ticker]['Close'].values
            if len(ticker_price) > 0:
                total_value += shares * ticker_price[0]
    
    portfolio_values.append({
        'Date': date,
        'Portfolio_Value': total_value
    })

portfolio_ts = pd.DataFrame(portfolio_values)
portfolio_ts = portfolio_ts[portfolio_ts['Portfolio_Value'] > 0]

print(f"✓ Calculated {len(portfolio_ts)} daily portfolio values")

portfolio_ts['Daily_Return'] = portfolio_ts['Portfolio_Value'].pct_change()
portfolio_ts['Cumulative_Return'] = ((portfolio_ts['Portfolio_Value'] / portfolio_ts['Portfolio_Value'].iloc[0]) - 1) * 100

returns = portfolio_ts['Daily_Return'].dropna()

print("\n" + "=" * 70)
print("RISK METRICS")
print("=" * 70)

total_return = (portfolio_ts['Portfolio_Value'].iloc[-1] / portfolio_ts['Portfolio_Value'].iloc[0] - 1) * 100
days = (portfolio_ts['Date'].iloc[-1] - portfolio_ts['Date'].iloc[0]).days
annualized_return = ((1 + total_return/100) ** (365/days) - 1) * 100

volatility = returns.std() * np.sqrt(252) * 100

risk_free_rate = 0.04
sharpe_ratio = (annualized_return/100 - risk_free_rate) / (volatility/100)

portfolio_ts['Peak'] = portfolio_ts['Portfolio_Value'].expanding(min_periods=1).max()
portfolio_ts['Drawdown'] = (portfolio_ts['Portfolio_Value'] / portfolio_ts['Peak'] - 1) * 100
max_drawdown = portfolio_ts['Drawdown'].min()

var_95 = np.percentile(returns.dropna(), 5) * 100

print(f"\n{'Metric':<35} {'Value':>15}")
print("-" * 52)
print(f"{'Total Return:':<35} {total_return:>14.2f}%")
print(f"{'Annualized Return:':<35} {annualized_return:>14.2f}%")
print(f"{'Annualized Volatility:':<35} {volatility:>14.2f}%")
print(f"{'Sharpe Ratio:':<35} {sharpe_ratio:>14.2f}")
print(f"{'Maximum Drawdown:':<35} {max_drawdown:>14.2f}%")
print(f"{'Value at Risk (95%):':<35} {var_95:>14.2f}%")
print(f"{'Best Daily Return:':<35} {returns.max()*100:>14.2f}%")
print(f"{'Worst Daily Return:':<35} {returns.min()*100:>14.2f}%")

print("\n" + "=" * 70)
print("INDIVIDUAL POSITION RISK")
print("=" * 70)
print(f"\n{'Ticker':<8} {'Asset Name':<30} {'Volatility':>12} {'Max Drawdown':>15}")
print("-" * 70)

position_risk = []

for ticker in portfolio['Ticker']:
    ticker_data = market_data[market_data['Ticker'] == ticker].sort_values('Date')
    ticker_returns = ticker_data['Close'].pct_change().dropna()
    
    ticker_vol = ticker_returns.std() * np.sqrt(252) * 100
    
    ticker_data['Peak'] = ticker_data['Close'].expanding(min_periods=1).max()
    ticker_data['DD'] = (ticker_data['Close'] / ticker_data['Peak'] - 1) * 100
    ticker_max_dd = ticker_data['DD'].min()
    
    asset_name = portfolio[portfolio['Ticker'] == ticker]['Asset_Name'].values[0]
    
    position_risk.append({
        'Ticker': ticker,
        'Volatility': ticker_vol,
        'Max_Drawdown': ticker_max_dd
    })
    
    print(f"{ticker:<8} {asset_name:<30} {ticker_vol:>11.2f}% {ticker_max_dd:>14.2f}%")

portfolio_ts.to_csv('data/processed/portfolio_timeseries.csv', index=False)
print(f"\n{'='*70}")
print(f"✓ Time series data saved to: data/processed/portfolio_timeseries.csv")

risk_summary = pd.DataFrame([{
    'Total_Return_Pct': total_return,
    'Annualized_Return_Pct': annualized_return,
    'Volatility_Pct': volatility,
    'Sharpe_Ratio': sharpe_ratio,
    'Max_Drawdown_Pct': max_drawdown,
    'VaR_95_Pct': var_95,
    'Best_Daily_Return_Pct': returns.max()*100,
    'Worst_Daily_Return_Pct': returns.min()*100
}])

risk_summary.to_csv('data/processed/risk_metrics.csv', index=False)
print(f"✓ Risk metrics saved to: data/processed/risk_metrics.csv")
print(f"{'='*70}\n")