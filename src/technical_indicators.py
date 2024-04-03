import pandas as pd

def rsi(df: pd.DataFrame, periods = 14, ema = True):
    """
    Calculates the Relative Strength Index (RSI) for a given DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the 'close' column.
    - periods (int): The number of periods to consider for the RSI calculation. Default is 14.
    - ema (bool): If True, uses exponential moving average. If False, uses simple moving average. Default is True.

    Returns:
    - float: The RSI value for the last period.

    """
    df["close"] = pd.to_numeric(df["close"])
    close_delta = df['close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
        # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return round(rsi.iloc[-1],2)


def ichimoku(df):
    high_prices = df['high']
    close_prices = df['close']
    low_prices = df['low']

    # Tenkan-sen (Conversion Line)
    nine_period_high = high_prices.rolling(window=9).max()
    nine_period_low = low_prices.rolling(window=9).min()
    df['tenkan_sen'] = (nine_period_high + nine_period_low) / 2

    # Kijun-sen (Base Line)
    twenty_six_period_high = high_prices.rolling(window=26).max()
    twenty_six_period_low = low_prices.rolling(window=26).min()
    df['kijun_sen'] = (twenty_six_period_high + twenty_six_period_low) / 2

    # Senkou Span A (Leading Span A)
    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)

    # Senkou Span B (Leading Span B)
    fifty_two_period_high = high_prices.rolling(window=52).max()
    fifty_two_period_low = low_prices.rolling(window=52).min()
    df['senkou_span_b'] = ((fifty_two_period_high + fifty_two_period_low) / 2).shift(26)

    # Chikou Span (Lagging Span)
    df['chikou_span'] = close_prices.shift(-26)

    return df

def get_ichimoku_conversion_line(df):
    df = ichimoku(df)
    return round(df['tenkan_sen'].iloc[-1],2)