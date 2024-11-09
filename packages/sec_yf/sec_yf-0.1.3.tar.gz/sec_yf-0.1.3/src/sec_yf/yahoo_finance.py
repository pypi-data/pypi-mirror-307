#%%
import yfinance as yf
import pandas as pd
import logging
from sec_cik_mapper import StockMapper
import os 
logging.basicConfig(level=logging.INFO)

def get_cik_to_tickers():
    return StockMapper().cik_to_tickers

#%%
# download from yfinance data from a list of tickers 
def get_stock_data(ticker, start_date, end_date):
    """get_stock_data retrieves historical data on prices for a given stock

    Args:
        ticker (str): The stock ticker
        start_date (str): Start date in the format 'YYYY-MM-DD'
        end_date (str): End date in the format 'YYYY-MM-DD'

    Returns:
        pd.DataFrame: A pandas dataframe with the historical data

    Example:
        df = get_stock_data('AAPL', '2000-01-01', '2020-12-31')
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date, auto_adjust=False, actions=False,
                         interval='1d')
    # as dataframe 
    df = pd.DataFrame(data)
    df['ticker'] = ticker
    df.reset_index(inplace=True)
    return df

def get_stocks_data(tickers, start_date, end_date):
    """get_stocks_data retrieves historical data on prices for a list of stocks

    Args:
        tickers (list): List of stock tickers
        start_date (str): Start date in the format 'YYYY-MM-DD'
        end_date (str): End date in the format 'YYYY-MM-DD'

    Returns:
        pd.DataFrame: A pandas dataframe with the historical data

    Example:
        df = get_stocks_data(['AAPL', 'MSFT'], '2000-01-01', '2020-12-31')
    """
    # get the data for each stock
    # try/except to avoid errors when a stock is not found
    dfs = []
    for ticker in tickers:
        try:
            df = get_stock_data(ticker, start_date, end_date)
            # append if not empty
            if not df.empty:
                dfs.append(df)
        except:
            logging.warning(f"Stock {ticker} not found")
    # concatenate all dataframes
    data = pd.concat(dfs)
    return data

# get all data for all tickers 
def get_all_data(start_date='2009-01-01'):
    tickers = get_cik_to_tickers().values()
    # linearize tickers
    ticks = []
    for tick in tickers:
        # convert the set to a list 
        ticks += list(tick)
    end_date = pd.Timestamp.today().strftime('%Y-%m-%d')
    df =  get_stocks_data(ticks, start_date, end_date)
    # create a folder to save the data called yahoo_finance_data
    if not os.path.exists('yahoo_finance_data'):
        os.makedirs('yahoo_finance_data')
    
    # parquet format is faster to read and write
    df.to_parquet('yahoo_finance_data/yahoo_finance_data.parquet')

    # save also the linking table 
    to_append = get_cik_to_tickers()
    # we could have more than one ticker per cik, so append them
    ciks=[]
    tickers = []
    for key, value in to_append.items():
        # check the size of the set
        tick_ = list(value)
        ciks += [key]*len(tick_)
        tickers += tick_
    df_link = pd.DataFrame({'cik': ciks, 'ticker': tickers})
    df_link.to_parquet('yahoo_finance_data/cik_ticker.parquet')
