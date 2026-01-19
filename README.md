# Investment Portfolio Analytics Dashboard

## Project Overview

An end-to-end investment portfolio analytics solution that automates data collection, processing, and visualization. This project replicates institutional fund administration workflows, transforming manual Excel-based reporting into an automated, interactive Power BI dashboard.

---

## Business Problem

Fund administrators spend 10+ hours weekly on manual tasks:
- Reconciling portfolio positions against market prices
- Calculating Net Asset Value (NAV) and unrealized gains/losses
- Generating performance reports and risk metrics
- Updating stakeholders with static Excel files

**This project solves these pain points through automation and interactive analytics.**

---

## Solution

A Python-powered data pipeline feeding a dynamic Power BI dashboard that provides:
- **Real-time portfolio valuation** across 14 positions worth $526K
- **Automated performance tracking** with 64.5% annualized returns
- **Risk analytics** including Sharpe Ratio (2.12), VaR, and maximum drawdown
- **Interactive drill-down** capability for individual position analysis

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Data collection, processing, and calculations |
| **Pandas & NumPy** | Data manipulation and numerical analysis |
| **yfinance API** | Real-time market data retrieval |
| **Power BI** | Interactive dashboard and visualizations |
| **DAX** | Custom measures and calculated columns |
| **Star Schema** | Optimized data modeling for analytics |

---

## Key Features

### 1. Automated Data Pipeline
- Fetches daily market data for 14 securities via yfinance API
- Processes 3,514 historical price records
- Calculates portfolio metrics automatically
- Generates Power BI-ready tables following star schema principles

### 2. Comprehensive Dashboard (4 Pages)

#### **Portfolio Overview**
- Total value, unrealized gains, and return percentage
- Asset allocation breakdown (64% Equity, 36% ETF)
- Top 10 holdings by weight
- Performance table with conditional formatting

#### **Performance Analysis**
- Cumulative returns over time
- Best and worst performing positions
- Returns by asset class
- Daily returns distribution

#### **Individual Stock Focus**
- Interactive stock selector
- Price history charts
- Position-specific KPIs
- Return tracking over time

#### **Risk Analysis**
- Portfolio drawdown visualization
- Risk metrics dashboard (Sharpe, VaR, Volatility)
- Position concentration analysis
- Days in drawdown tracking

### 3. Advanced Financial Metrics
- **Sharpe Ratio**: 2.12 (excellent risk-adjusted returns)
- **Maximum Drawdown**: -17.17%
- **Annualized Volatility**: 28.52%
- **Value at Risk (95%)**: -1.30%
- **Win Rate**: 85.7% (12 of 14 positions profitable)

---

## Project Structure

```
Investment-Portfolio-Analytics/
│
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── .gitignore                         # Git ignore rules
├── portfolio_holdings.csv             # Sample portfolio data
├── Investment Portfolio Analytics.pbix # Power BI dashboard
├── Investment Portfolio Dashboard.pdf  # Dashboard export
│
├── src/                               # Python scripts
│   ├── 01_data_collection.py         # Fetch market data
│   ├── 02_verify_data_structure.py   # Data quality checks
│   ├── 03_clean_market_data.py       # Data cleaning
│   ├── 04_portfolio_performance.py   # Performance calculations
│   ├── 05_risk_metrics.py            # Risk analysis
│   ├── 06_prepare_for_powerbi.py     # Power BI table generation
│   └── 07_fix_data_dictionary.py     # Documentation
│
├── data/                              # Data storage
│   ├── raw/                          # Raw market data (not in repo)
│   ├── processed/                    # Cleaned datasets
│   ├── powerbi/                      # Power BI ready tables
│
├── screenshots/                       # Dashboard images
│   ├── 01_Portfolio_Overview.png
│   ├── 02_Performance_Analysis.png
│   ├── 03_Individual_Stock_Focus.png
│   └── 04_Risk_Analysis.png
│
└── docs/                             # Additional documentation
    └── DATA_DICTIONARY.txt
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- Power BI Desktop
- Internet connection (for market data API)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Investment-Portfolio-Analytics.git
cd Investment-Portfolio-Analytics
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the data pipeline**
```bash
# Step 1: Collect market data
python src/01_data_collection.py

# Step 2: Verify data quality
python src/02_verify_data_structure.py

# Step 3: Clean and process data
python src/03_clean_market_data.py

# Step 4: Calculate portfolio performance
python src/04_portfolio_performance.py

# Step 5: Generate risk metrics
python src/05_risk_metrics.py

# Step 6: Prepare Power BI tables
python src/06_prepare_for_powerbi.py

# Step 7 (Optional): Data Dictionary fix
python src/07_fix_data_dictionary.py
```

4. **Open the Power BI dashboard**
- Open `Investment Portfolio Analytics.pbix` in Power BI Desktop
- Click **Refresh** to load the latest data
- Explore the 4 dashboard pages

---

## Sample Results

### Portfolio Performance
- **Initial Investment**: $433,328
- **Current Value**: $526,179
- **Total Return**: +21.43%
- **Annualized Return**: 64.50%

### Top Performers
1. **GOOGL**: +133.86% ($15,238 gain)
2. **JPM**: +83.54% ($28,152 gain)
3. **QQQ**: +57.09% ($18,078 gain)

### Risk Metrics
- **Max Drawdown**: -17.17%
- **Volatility**: 28.52%
- **Days in Drawdown**: 200 days

---

## Business Impact

### Time Savings
- **Before**: 10+ hours/week manual Excel work
- **After**: 5 minutes to refresh dashboard
- **Annual savings**: 500+ hours

### Improved Decision Making
- Real-time visibility into portfolio performance
- Proactive risk monitoring with automated alerts
- Data-driven rebalancing decisions

### Scalability
- Easily expandable to multiple portfolios
- Supports unlimited securities
- Automated daily updates

---

## Skills Demonstrated

- **Python Programming**: Data collection, cleaning, transformation
- **Financial Analysis**: Portfolio valuation, performance metrics, risk analysis
- **Data Modeling**: Star schema design, fact/dimension tables
- **Power BI**: Dashboard design, DAX measures, interactive features
- **Business Intelligence**: Translating business requirements into analytics

---

## Author

- Robert Collins

Currently: Investment Management Administrator at Deloitte

This project demonstrates my ability to bridge finance domain expertise with technical data analytics skills, automating complex workflows and delivering actionable insights through interactive visualizations.

### Connect With Me
- **LinkedIn**: https://www.linkedin.com/in/robanthonycollins/
- **Email**: RobCollins2002@gmail.com
- **Location**: Cork, Ireland

---

## Acknowledgments

- Market data provided by Yahoo Finance API
- Dashboard inspiration from institutional investment management platforms
- Built as part of my transition from finance operations to data analytics

---

## Related Projects

- [Customer Churn Analysis] - Predictive analytics for customer retention
- [Sales Forecasting Dashboard] - Time series forecasting with Python
- [SQL Case Study - Food Delivery Optimization] - Database design and query optimization

---

Last Updated: January 2026