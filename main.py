from datetime import datetime
from portfolio import Portfolio

if __name__ == "__main__":
    # dates for analysis
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2024, 1, 1)

    portfolio = Portfolio()
    portfolio.add_stock('AAPL', 10)  
    portfolio.add_stock('MSFT', 5)  
    portfolio.add_stock('GOOGL', 8)  

    portfolio.load_data(start=start_date, end=end_date)

    profit = portfolio.profit(start_date, end_date)
    annualized_return = portfolio.profit(start_date, end_date, annualized=True)
    print(f"Profit: ${profit:.2f}")
    print(f"Annualized Return: {annualized_return * 100:.2f}%")

    portfolio.plot_portfolio(start_date, end_date)
