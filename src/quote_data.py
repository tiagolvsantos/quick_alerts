import yfinance as yf
import pandas as pd
import requests
import time
import yaml
import os
from src import utils as utils



def get_stock_last_price(stock):
    """
    Retrieves the last price of a stock using its symbol.

    Args:
        stock (str): The stock symbol.

    Returns:
        float: The last price of the stock.
    """
    ticker = yf.Ticker(stock)
    try:
        return ticker.fast_info['lastPrice']
    except KeyError:
        return None

def get_all_time_high(stock):
    """
    Returns the all-time high price for a stock.
    """
    data = yf.Ticker(stock)
    history = data.history(period="1y")
    return history['High'].max()

def get_all_time_low(stock):
    """
    Returns the all-time low price for a stock.
    """
    data = yf.Ticker(stock)
    history = data.history(period="1y")
    return history['Low'].min()

def get_tradfi_historical_data(symbol, period="1y", interval="1d"):
    """
    Retrieves historical data for a given symbol from Yahoo Finance.

    Args:
        symbol (str): The symbol of the stock or asset.
        period (str, optional): The time period for which to retrieve the data. Defaults to "1y".
        interval (str, optional): The interval between data points. Defaults to "1d".

    Returns:
        pandas.DataFrame: The historical data as a DataFrame with columns: 'date', 'open', 'high', 'low', 'close', 'adj close', 'volume' (if 7 columns),
        or 'date', 'open', 'high', 'low', 'close', 'volume', 'dividends', 'stock split', 'capital gains' (if 9 columns).
        Returns an empty DataFrame if no data is available.

    Raises:
        NameError: If an error occurs during the retrieval of data.

    """
    try:
        time.sleep(0.3)
        df_data = (yf.download(tickers=symbol, period=period, interval=interval, progress=False).dropna())
        df_data.reset_index(level=0, inplace=True)

        if len(df_data) > 0:
            df_data["Date"] = df_data["Date"].dt.tz_localize(None)

        if len(df_data.columns) == 7:
            df_data.columns = ['date', 'open', 'high', 'low', 'close', 'adj close', 'volume']
        elif len(df_data.columns) == 9:
            df_data.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'dividends', 'stock split', 'capital gains']
        else:
            df_data = pd.DataFrame()

        return df_data

    except Exception as e:
        raise e

def get_crypto_historical_data(symbol: str, interval="1d"):
    """
    Retrieves historical cryptocurrency data from Binance API.

    Args:
        symbol (str): The symbol of the cryptocurrency.
        interval (str, optional): The interval for the data. Defaults to "1d".

    Returns:
        pandas.DataFrame: The historical data as a DataFrame, or an empty DataFrame if an exception occurs or no data is available.
    """
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}"
    try:
        df_quote = pd.DataFrame(requests.get(url).json())
        df_quote.columns = ['open time', 'open', 'high', 'low', 'close', 'volume', 'close time', 'asset volume', 'number of trades', 'taker buy asset volume', 'taker buy quote volume', 'ignore']
        df_quote['open time'] = df_quote['open time'].astype(str)
        df_quote['close time'] = df_quote['close time'].astype(str)
        df_quote['close'] = float(df_quote['close'].iloc[-1])
        for index, row in df_quote.iterrows():
            df_quote.at[index,'open time']= str(utils.epoch_to_datetime(int(row['open time'])))
            df_quote.at[index,'close time']= str(utils.epoch_to_datetime(int(row['close time'])))
        return df_quote if len(df_quote)>0 else pd.DataFrame()
    except Exception as e:
        raise e


def get_crypto_last_price(symbol: str, interval="1d"):
    """
    Retrieves historical cryptocurrency data from Binance API.

    Args:
        symbol (str): The symbol of the cryptocurrency.
        interval (str, optional): The interval for the data. Defaults to "1d".

    Returns:
        pandas.DataFrame: The historical data as a DataFrame, or an empty DataFrame if an exception occurs or no data is available.
    """
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}"
    try:
        df_quote = pd.DataFrame(requests.get(url).json())
        df_quote.columns = ['open time', 'open', 'high', 'low', 'close', 'volume', 'close time', 'asset volume', 'number of trades', 'taker buy asset volume', 'taker buy quote volume', 'ignore']

        return float(df_quote['close'].iloc[-1]) if len(df_quote)>0 else 0
    except Exception as e:
        raise e



def get_all_symbols():
    """
    Returns a list of all stock symbols.
    """
    yaml_files = [f for f in os.listdir('data') if f.endswith('.yaml')]
    list_symbols = []
    for file in yaml_files:
        with open(os.path.join('data', file), 'r') as f:
            yaml_content = yaml.safe_load(f)
            market = yaml_content.get('market')
            for item in yaml_content['symbols']:
                list_symbols.append([item, market])
    return list_symbols
