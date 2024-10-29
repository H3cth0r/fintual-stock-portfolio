import yfinance as yf
import pandas as pd
from datetime import datetime

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

if __name__ == "__main__":
    start_date  = datetime(2020, 1, 1)
    end_date    = datetime(2023, 1, 1)
    stock_df    = Stock(ticker="NVDA", start=start_date, end=end_date)
    print(stock_df)
