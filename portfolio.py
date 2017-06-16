""" compute portfolio statistics"""

import pandas as pd
import matplotlib.pyplot as plt

from util import get_data, plot_data, normalize_data

def compute_daily_returns(df):
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    daily_returns.ix[0, :] = 0
    return daily_returns


def test_run():

    start_val = 1000
    dates = pd.date_range('2009-01-01', '2011-12-31')
    symbols = ['SPY','XOM','GOOG','GLD']
    allocs = [.4,.4,.1,.1]
    #   get all the stock data
    df = get_data(symbols, dates)
    # normed = normalize_data(df)
    # alloc_df = normed * allocs
    # pos_vals = alloc_df * start_val
    # port_val = pos_vals.sum(axis=1)
    #   figure out porfolio value considering funds allocation and start dollar amount
    port_val = ((normalize_data(df) * allocs) * start_val).sum(axis=1)
    print 'end breakpoint'

if __name__ == "__main__":
    test_run()