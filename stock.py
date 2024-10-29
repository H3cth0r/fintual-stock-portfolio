import yfinance as yf
import pandas as pd
from datetime import datetime
from pandas.errors import OutOfBoundsDatetime

import io
from contextlib import redirect_stdout

def run_function_silently(func):
    with io.StringIO() as fake_stdout:
        with redirect_stdout(fake_stdout):
            result = func()

        return result, fake_stdout.getvalue()

class Stock(pd.DataFrame):
    """ stock dataframe holding the data from a stock. Uses yfiance"""
    def __init__(self, ticker=None, *args, **kwargs):
        if isinstance(ticker, str):
            downloaded_data = self.download(ticker, **kwargs)
        super(Stock, self).__init__(downloaded_data, *args)

    def download(self, ticker, start=None, end=None, interval="1d", *args, **kwargs):
        param_dict = {
            'tickers': ticker,
            'start': start,
            'end': end,
            'interval': interval
        }
        param_dict.update(kwargs)
        donwloaded, _ = run_function_silently(lambda: yf.download(**param_dict))
        return donwloaded

    def price(self, date):
        """Returns the adjusted close price for a given date or the nearest available date."""
        # Ensure the date is in datetime format
        if not isinstance(date, pd.Timestamp):
            date = pd.to_datetime(date)

        # Try to get the price for the exact date
        if date in self.index:
            return self.loc[date, "Adj Close"]

        # If date is not found, get the closest available date
        nearest_idx = self.index.get_indexer([date], method='nearest')[0]
        if nearest_idx >= 0:  # Ensure that the index is valid
            nearest_date = self.index[nearest_idx]
            return self.loc[nearest_date, "Adj Close"]
        
        # If no valid date is available in the index
        print("not found!")
        return None

if __name__ == "__main__":
    start_date  = datetime(2021, 1, 1)
    end_date    = datetime(2024, 1, 1)
    stock_df    = Stock(ticker="NVDA", start=start_date, end=end_date)
    print(stock_df)
