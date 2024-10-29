# fintual-stock-portfolio

# Portfolio Analysis Project Documentation

## Problem Statement

The project aims to create a portfolio management system that calculates profits and returns between specified 
dates. The core requirement was to implement a Portfolio class containing multiple stocks, with each stock 
having a Price method to retrieve its value at any given date. The system also needed to calculate annualized 
returns and visualize the portfolio's performance over time. The implementation leverages Yahoo Finance for 
real-time stock data and includes data visualization capabilities.

## Project Structure

The project is organized into several Python files, each handling specific functionality:

- `stock.py` serves as the foundation, implementing a Stock class that inherits from pandas DataFrame. 
It manages the connection with Yahoo Finance (yfinance) to download historical stock data. The 
class includes methods for downloading stock data and retrieving prices for specific dates, with built-in handling 
for missing dates by finding the nearest available price.
- `portfolio.py` contains the core Portfolio class implementation, managing a collection of stocks and their 
respective shares. It provides methods for adding stocks, loading historical data, calculating profits, and computing 
annualized returns. The class also includes visualization functionality using matplotlib to plot portfolio value over 
time.
- `main.py` demonstrates the basic usage of the portfolio system through a command-line interface. It creates a sample 
portfolio with stocks (AAPL, MSFT, GOOGL), loads their historical data, and displays both regular and annualized returns 
along with a performance plot.
- `app.py` extends the functionality into a REST API using Flask. It exposes endpoints for adding stocks, calculating 
profits, and generating portfolio visualizations. 
- `notebook_showcase.ipynb` mirrors the functionality of main.py but in a Jupyter notebook format, providing an 
interactive environment for analysis and visualization.
- `shell.nix` defines the development environment using the Nix package manager, ensuring consistent dependencies 
across different systems. It includes Python 3.11 and all required packages .

## Implementation Details

The Stock class uses pandas DataFrame as its base, providing efficient data handling and date-based operations. 
Stock prices are retrieved using the adjusted close price, accounting for splits and dividends. The Portfolio 
class maintains a dictionary of stocks and their quantities, enabling accurate profit calculations across multiple 
positions.

The profit calculation supports both simple returns and annualized returns, using the standard formula for 
annualization: `((end_value / start_value) ^ (365.25 / days_between)) - 1`. 

The plotting functionality visualizes the total portfolio value over time, helping to understand performance trends.

The Flask API adds a service layer, making the portfolio analysis tools accessible via HTTP endpoints. 

## API Tests
To upload stocks to the portfolio
```
curl -X POST http://localhost:5000/add_stock \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "shares": 10}'

curl -X POST http://localhost:5000/add_stock \
  -H "Content-Type: application/json" \
  -d '{"ticker": "MSFT", "shares": 5}'

curl -X POST http://localhost:5000/add_stock \
  -H "Content-Type: application/json" \
  -d '{"ticker": "GOOGL", "shares": 8}'
```

Calculate profits:
```
# Regular profit
curl -X POST http://localhost:5000/calculate_profit \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2021-01-01",
    "end_date": "2024-01-01",
    "annualized": false
  }'

# Annualized return
curl -X POST http://localhost:5000/calculate_profit \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2021-01-01",
    "end_date": "2024-01-01",
    "annualized": true
  }'
```

# Get portfolio Plot in base64
```
curl -X POST http://localhost:5000/portfolio_plot \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2021-01-01",
    "end_date": "2024-01-01"
  }' > portfolio_plot.json
```
