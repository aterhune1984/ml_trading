""" plot a histogram."""

import pandas as pd
import matplotlib.pyplot as plt

from util import get_data, plot_data

def compute_daily_returns(df):
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    daily_returns.ix[0, :] = 0
    return daily_returns

def test_run():
    # read data
    dates = pd.date_range('2009-01-01', '2012-12-31')
    symbols = ['SPY','GOOG']
    df = get_data(symbols, dates)
    #plot_data(df)

    # compute daily returns
    daily_returns = compute_daily_returns(df)
    #plot_data(daily_returns, title='daily returns', ylabel='daily returns')

    # plot a histogram
    daily_returns['GOOG'].hist(bins=20,label='GOOG')
    daily_returns['SPY'].hist(bins=20,label='SPY')
    plt.legend(loc='upper right')
    

    # get mean and standard deviation
    #mean = daily_returns['SPY'].mean()
    #print "mean=", mean
    #std = daily_returns['SPY'].std()
    #print "std=", std

    #plt.axvline(mean, color='w', linestyle='dashed', linewidth=2)
    #plt.axvline(std, color='r', linestyle='dashed', linewidth=2)
    #plt.axvline(-std, color='r', linestyle='dashed', linewidth=2)

    #print daily_returns.kurtosis()
    plt.show()

if __name__ == "__main__":
    test_run()