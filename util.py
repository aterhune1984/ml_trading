
import os
import pandas as pd
import datetime
import urllib
import StringIO
import matplotlib.pyplot as plt

def google_history_pull(symbol, start_date, end_date=datetime.date.today().isoformat()):
    """ pull 'date,open,high,low,close,volume' from google 
        date format is 'yyyy-mm-dd' """
    symbol = symbol.upper()
    start = datetime.date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
    end = datetime.date(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
    url_string = "http://www.google.com/finance/historical?q={0}".format(symbol)
    url_string += "&startdate={0}&enddate={1}&output=csv".format(
        start.strftime('%b %d, %Y'), end.strftime('%b %d, %Y'))
    csv = urllib.urlopen(url_string).readlines()
    return csv

def plot_selected(df, columns, start_index, end_index):
    '''plot desired columns over index values in the given range'''
    plot_data(df.ix[start_index:end_index,columns],title="Selected data")


def symbol_to_path(symbol, base_dir="data"):
    """Return csv file path given ticket symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference if absent
        symbols.insert(0, 'SPY')

    # TODO: create a pull method to get trade information from google finance
    for symbol in symbols:
        _temp = google_history_pull(symbol,
                                    dates[0].strftime('%Y-%m-%d'),
                                    dates[-1].strftime('%Y-%m-%d'))
        output = StringIO.StringIO()
        output.writelines(_temp)
        output.seek(0)
        df_temp = pd.read_csv(output,
                              index_col='Date',
                              parse_dates=True,
                              usecols=['Date', 'Close'],
                              na_values=['-'])
        df_temp = df_temp.rename(columns={'Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':
            df = df.dropna(subset=['SPY'])
    return df

def plot_data(df, title='Stock prices', xlabel='Date', ylabel='Price'):
    '''plot stock prices'''
    ax = df.plot(title=title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()


def get_rolling_mean(values, window):
    return pd.rolling_mean(values, window=window)

def get_rolling_std(values,window):
    return pd.rolling_std(values, window=window)

def get_bollinger_bands(rm, rstd):
    ''' return upper and lower bollinger bands'''
    upper_band = rm + rstd * 2
    lower_band = rm - rstd * 2
    return upper_band, lower_band

def normalize_data(df):
    """normalize stock prices uning the first row of the dataframe"""
    return df/ df.ix[0,:]

def compute_daily_returns(df):
    """ compute and return the daily return values"""
    daily_returns = df.copy() # copy given dataframe to match size and column names
    # compute daily returns for row 1 onwards
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    daily_returns.ix[0, :] = 0  # set daily returns for row 0 to 0
    return daily_returns



def test_run():
    # define a date range
    dates = pd.date_range('2010-01-01', '2010-01-31')

    # choose stock symbols to read
    symbols = ['GOOG']  # SPY will be added in get_data()

    df = get_data(symbols, dates)
    # fill any missing data ('NaN values') forward, then backward
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    #   slice by row range(dates)
    # print df.ix['2010-01-01':'2010-01-31'] # the month of january

    #   slice by column(symbols)
    # print df['GOOG'] # a single label prints a single column
    # print df[['IBM','GLD']] # a list of labelels selects multiple columns

    #   slice by row and column
    # print df.ix['2010-03-10':'2010-03-15',['SPY','IBM']]

    #   normalize data so it starts at 1
    # df = normalize_data(df)

    #   plot all data
    # plot_data(df)

    #   plot selected data
    # plot_selected(df, ['SPY', 'IBM'], '2010-03-01', '2010-04-01')

    #   compute global statistics for each stock
    # print df.mean()
    # print df.median()
    # print df.std()

    #===================================================================
    #   calculate and plot rolling mean for SPY
    # ax = df['SPY'].plot(title="SPY rolling mean", label='SPY')
    # rm_SPY = pd.rolling_mean(df['SPY'], window=20)
    # rm_SPY.plot(label='Rolling mean', ax=ax)
    # ax.set_xlabel('Date')
    # ax.set_ylabel('Price')
    # ax.legend(loc='upper left')
    # plt.show()
    #==============================================================
    #   calculate and plot rolling mean plus upper and lower bounds of 2x std deviation (bollinger bands)
    # rm_SPY = get_rolling_mean(df['SPY'], window=20)
    # rstd_SPY = get_rolling_std(df['SPY'], window=20)
    # upper_band, lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)
    # ax = df['SPY'].plot(title='Bollinger Bands', label='SPY')
    # rm_SPY.plot(label="Rolling mean",ax=ax)
    # upper_band.plot(label='upper band', ax=ax)
    # lower_band.plot(label='lower band', ax=ax)
    # ax.set_xlabel('Date')
    # ax.set_ylabel('Price')
    # ax.legend(loc='upper left')
    # plt.show()
    #==============================================================
    #   Daily returns
    daily_returns = compute_daily_returns(df)
    plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")



if __name__ == '__main__':
    test_run()
    print 'exit'
