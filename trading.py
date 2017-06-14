import os
import pandas as pd
import datetime
import urllib
import StringIO

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


def test_run():
    # define a date range
    dates = pd.date_range('2010-01-01', '2010-12-31')

    # choose stock symbols to read
    symbols = ['GOOG', 'IBM', 'GLD']  # SPY will be added in get_data()

    df = get_data(symbols, dates)
    #   slice by row range(dates)
    # print df.ix['2010-01-01':'2010-01-31'] # the month of january

    #   slice by column(symbols)
    # print df['GOOG'] # a single label prints a single column
    # print df[['IBM','GLD']] # a list of labelels selects multiple columns

    #   slice by row and column
    # print df.ix['2010-03-10':'2010-03-15',['SPY','IBM']]

    print df


if __name__ == '__main__':
    test_run()
    print 'exit'
