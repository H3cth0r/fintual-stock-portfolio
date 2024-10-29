from stock import Stock
import pandas as pd
import matplotlib.pyplot as plt

class Portfolio:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, ticker, shares):
        if ticker not in self.stocks: self.stocks[ticker] = {'stock': None, 'shares': shares}
        else: self.stocks[ticker]["shares"] += shares
    def load_data(self, start, end):
        for stock_ticker, stock_info in zip(self.stocks.keys(), self.stocks.values()):
            stock_info['stock'] = Stock(ticker=stock_ticker, start=start, end=end)
    def profit(self, start_date, end_date, annualized=False):
        start_price = 0.0
        end_price = 0.0

        for stock_info in self.stocks.values():
            stock = stock_info['stock']
            shares = stock_info['shares']
            start_price += stock.price(start_date) * shares
            end_price += stock.price(end_date) * shares

        # calculate total return
        profit = end_price - start_price
        if not annualized:
            return profit

        # calculate annualized return
        days_diff = (end_date - start_date).days
        annualized_return = ((end_price / start_price) ** (365.25 / days_diff)) - 1
        return annualized_return

    def plot_portfolio(self, start_date, end_date):
        date_range = pd.date_range(start=start_date, end=end_date)
        portfolio_values = []

        for date in date_range:
            total_value = sum(
                stock_info['stock'].price(date) * stock_info['shares']
                for stock_info in self.stocks.values()
            )
            portfolio_values.append(total_value)

        plt.figure(figsize=(12, 6))
        plt.plot(date_range, portfolio_values, label='Portfolio Value')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value (USD)')
        plt.title('Portfolio Value Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()
