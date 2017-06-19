""" compute portfolio statistics"""

import pandas as pd
import matplotlib.pyplot as plt

from util import get_data, plot_data, normalize_data

def compute_daily_port_returns(df):
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    daily_returns.ix[0] = 0
    return daily_returns

def compute_port_cumulative_returns(df):
    cum_returns = (df[-1] / df[0]) - 1
    return cum_returns


def compute_sharpe_ratio(dr_port_val):
    annual_risk_free_rate = .011
    daily_risk_free_rate = (1.0 + annual_risk_free_rate) ** (1.0 / 252) - 1
    mean = (dr_port_val - daily_risk_free_rate).mean()
    std = (dr_port_val - daily_risk_free_rate).std()
    sr = mean/std
    samples_per_year = 252
    k = samples_per_year ** (1.0 / 2)
    sr_corrected = k * sr
    return sr_corrected


def test_run():

    start_val = 1000
    port = {'SPY':.4,
            'XOM':.4,
            'GOOG':.1,
            'GLD':.1}
    # sanity check
    if not sum(port.values()) == 1:
        print 'your allocation must be 100%'
        exit(1)

    dates = pd.date_range('2009-01-01', '2011-12-31')
    symbols = port.keys()
    allocs = port.values()
    #   get all the stock data
    df = get_data(symbols, dates)
    # normed = normalize_data(df)
    # alloc_df = normed * allocs
    # pos_vals = alloc_df * start_val
    # port_val = pos_vals.sum(axis=1)
    #   figure out porfolio value considering funds allocation and start dollar amount
    port_val = ((normalize_data(df) * allocs) * start_val).sum(axis=1)

    #   calculate portfolio statistics

    #   daily returns
    dr_port_val = compute_daily_port_returns(port_val)

    cum_returns = compute_port_cumulative_returns(port_val)
    avg_daily_return = dr_port_val.mean()
    std_daily_return = dr_port_val.std()
    sharpe_ratio = compute_sharpe_ratio(dr_port_val)

    print 'end breakpoint'

if __name__ == "__main__":
    test_run()