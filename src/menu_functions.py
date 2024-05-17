from src import json_functions as jf
from src import quote_data as qd
from src import telegram_con as tg
from src import technical_indicators as ti
import time
import numpy as np
import os
import json
import pandas as pd
from datetime import datetime
from binance.client import Client
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' 
import pygame.mixer
import warnings
# Ignore pandas FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)


client = Client(os.getenv('binance_api_key'), os.getenv('binance_api_secret'))

def _delete_alerts(type):
    """
    Delete alerts of a specific type from the 'alerts.json' file.

    Args:
        type (str): The type of alerts to be deleted.

    Returns:
        None
    """
    type = "automatic"
    alerts = jf.read_alerts('alerts.json')
    alerts = [alert for alert in alerts if alert['type'] != type]
    jf.write_alerts('alerts.json', alerts)

def add_alert_interactive():
    """
    Adds a new alert to the configuration file.
    """
    symbol = input('Enter the symbol: ').upper(); print(f"{symbol} does not exist.") if 'USDT' not in symbol and qd.get_stock_last_price(symbol) is None else None
    level = next((float(level_input) for level_input in iter(lambda: input('Enter the price level: '), 'q') if level_input.replace('.','',1).isdigit()), 'q')
    move = ''
    while (move := input('Enter the move (above/below): ').lower()) not in ['above', 'below']: print("Invalid move. Please enter 'above' or 'below'.")
    reason = input('Enter the reason for the alert: ').lower()
    while (market := input('Enter the market for the alert (tradfi/crypto): ').lower()) not in ['tradfi', 'crypto']: print("Invalid move. Please enter 'tradfi' or 'crypto'.")

    alert = {'symbol': symbol, 'level': level, 'move': move, 'reason': reason, 'market': market, 'alert_type': 'price', 'type': 'manual'}
    alerts = jf.read_alerts('alerts.json')
    alerts.append(alert)
    jf.write_alerts('alerts.json', alerts)

def add_alert(symbol, level, move, reason, alert_type, market='tradfi'):
    """
    Adds a new alert.

    Parameters:
    stock (str): The stock symbol.
    level (float): The price level.
    move (str): The direction of the price movement ('above' or 'below').
    reason (str): The reason for the alert.
    """
    alert = {
        'symbol': symbol,
        'level': level,
        'move': move,
        'reason': reason,
        'market': market,
        'type': "automatic",
        'alert_type': alert_type
    }
    alerts = jf.read_alerts('alerts.json')
    alerts.append(alert)
    jf.write_alerts('alerts.json', alerts)
    print(f"Alert added for symbol {symbol} when it moves {move} {level}. Reason: {reason}")

def run_alerts(run_alerts_command, play_sound, asset_url_enabled=False):
    """
    Runs the alerts based on the specified criteria.

    Args:
        run_alerts_command (bool): Flag indicating whether to run the alerts or not.
        play_sound (bool): Flag indicating whether to play a sound when an alert is triggered.
        asset_url_enabled (bool, optional): Flag indicating whether to include asset URLs in the alert messages. Defaults to False.
    """
    ## Alert sound
    pygame.mixer.init()
    pygame.mixer.music.load('.\\assets\\beep.mp3')

    alerts = jf.read_alerts('alerts.json')
    new_alerts = []
    counter = 0

    for alert in alerts:
        print(alert)
        symbol = alert['symbol']
        level = alert['level']
        move = alert['move']
        reason = alert['reason']
        market = alert['market']

        counter += 1
        if counter % 25 == 0:
            counter = 0
            time.sleep(5) 

        if market == 'tradfi':
            price = qd.get_stock_last_price(symbol)
        else:
            price = qd.get_crypto_last_price(symbol)

        if price is not None:
            price = round(price, 2)
        else:
            print(f"Could not get the price for stock {symbol}. Skipping this stock.")
            continue

        if market == "tradfi" and "=" not in symbol and "." not in symbol and asset_url_enabled:
            asset_url = f"https://finviz.com/{'crypto_charts' if '-USD' in symbol else 'quote'}.ashx?t={symbol.replace('-USD', 'USD')}&p=d"
        elif market == "crypto" and asset_url_enabled:
            asset_url = f"https://www.tradingview.com/symbols/{symbol.replace('-USD', 'USD')}/"
        elif (market == "tradfi" and "=" in symbol or "." in symbol) and asset_url_enabled:
            asset_url = f"https://finance.yahoo.com/quote/{symbol}?.tsrc=fin-srch"
        else:
            asset_url = ""

        if 'dma' in alert['alert_type']:
            if (price > level * 1.01 and move == 'above') or (price < level * 0.99 and move == 'below'):
                arrow = '↑' if move == 'above' else '↓'
                if run_alerts_command:
                    tg.send_telegram_message(f'${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
                if play_sound == True:
                    pygame.mixer.music.play()
            else:
                new_alerts.append(alert)

        elif 'bb' in alert['alert_type']:
                if (price > level * 1.01 and move == 'above') or (price < level * 0.99 and move == 'below'):
                    arrow = '↑' if move == 'above' else '↓'
                    if run_alerts_command:
                        tg.send_telegram_message(f'${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
                    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
                    if play_sound == True:
                       pygame.mixer.music.play()
                else:
                    new_alerts.append(alert)

        elif 'price' in alert['alert_type']:
            if (price > level and move == 'above') or (price < level and move == 'below'):
                arrow = '↑' if move == 'above' else '↓'
                if run_alerts_command:
                    tg.send_telegram_message(f'${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
                if play_sound == True:
                    pygame.mixer.music.play()
            else:
                new_alerts.append(alert)

        elif 'rsi' in alert['alert_type']:
            if market == 'tradfi':
                rsi = ti.rsi(qd.get_tradfi_historical_data(symbol))
            elif market == 'crypto':
                rsi = ti.rsi(qd.get_crypto_historical_data(symbol))
                
            if (rsi > level and move == 'above') or (rsi < level and move == 'below'):
                arrow = '↑' if move == 'above' else '↓'
                if run_alerts_command:
                    tg.send_telegram_message(f'${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
                if play_sound == True:
                    pygame.mixer.music.play()
            else:
                new_alerts.append(alert)
    #_delete_alerts('automatic')
    jf.write_alerts('alerts.json', new_alerts)

def _get_type():
    while True:
        alert_type = input('Enter the alert type to delete: (automatic/manual)').lower()
        if alert_type in ['automatic', 'manual']:
            return alert_type
        else:
            print("Invalid input. Please enter 'automatic' or 'manual'.")

def _get_alert_type():
    while True:
        alert_type = input('Enter the alert type to delete: (rsi/bb/dma/price)').lower()
        if alert_type in ['rsi', 'bb', 'dma', 'price']:
            return alert_type
        else:
            print("Invalid input. Please enter 'rsi', 'bb', 'dma', or 'price'.")

def _confirm_deletion(type):
    while True:
        confirmation = input(f'Are you sure you want to delete all alerts of type {type}? (yes/no): ').lower()
        if confirmation in ['yes', 'no']:
            return confirmation
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def delete_type_alerts():
    """
    Deletes all alerts of a specific type from the configuration file after confirmation.
    """
    type = _get_type()
    alert_type = _get_alert_type()
    confirmation = _confirm_deletion(type)
    new_alerts = []
    if confirmation == 'yes':
        alerts = jf.read_alerts('alerts.json')
        for alert in alerts:
            if alert['type'] == type and alert['alert_type'] == alert_type:
                #print(f"Deleting alert: {alert}")
                continue
            new_alerts.append(alert)
        jf.write_alerts('alerts.json', new_alerts)
    else:
        print("Operation cancelled.")

def print_symbol_alert():
    """
    Prints all alerts from the configuration file.
    """
    symbol = input('Enter the symbol: ').upper(); print(f"{symbol} does not exist.") if 'USDT' not in symbol and qd.get_stock_last_price(symbol) is None else None
    alerts = jf.read_alerts('alerts.json')
    for alert in alerts:
        if alert['type'] == 'manual' and alert['symbol'] == symbol:
            print(f"${alert['symbol']}, Level: {alert['level']}, Move: {alert['move']}, Reason: {alert['reason']}")

def print_manual_alerts():
    """
    Prints all manual alerts from the configuration file.
    """
    alerts = jf.read_alerts('alerts.json')
    for alert in alerts:
        if alert['type'] == 'manual':
            print(f"${alert['symbol']}, Level: {alert['level']}, Move: {alert['move']}, Reason: {alert['reason']}")

def delete_alerts_for_stock():
    """
    Deletes all alerts for a specific stock from the configuration file.
    """
    stock = input('Enter the stock symbol: ').upper()
    alerts = jf.read_alerts('alerts.json')
    alerts = [alert for alert in alerts if alert['stock'] != stock]
    jf.write_alerts('alerts.json', alerts)

def create_alerts_for_new_highs():
    """
    Creates alerts for new all-time highs for symbols in the market.
    """
    list_symbols = qd.get_all_symbols()
    for record in list_symbols:
        market = record[1]
        symbol = record[0]
        if market == 'tradfi':
            new_high = round(qd.get_all_time_high(symbol), 2)
        elif market == 'crypto':
            new_high = round(qd.get_crypto_historical_data(symbol)['close'].max(),2)
        add_alert(symbol, new_high, 'above', 'New high', "price", market)

def create_alerts_for_new_lows():
    """
    Creates alerts for new all-time lows for symbols.
    
    This function retrieves a list of symbols using `qd.get_all_symbols()`.
    For each symbol, it checks the market type and calculates the all-time low value.
    If the market type is 'tradfi', it uses `qd.get_all_time_low()` to get the all-time low value.
    If the market type is not 'tradfi', it uses `qd.get_crypto_historical_data()` to get the minimum close value.
    Finally, it calls the `add_alert()` function to add an alert for the symbol with the all-time low value.
    """
    list_symbols = qd.get_all_symbols()
    for record in list_symbols:
        market = record[1]
        symbol = record[0]
        if market == 'tradfi':
            new_low = round(qd.get_all_time_low(symbol), 2)
        elif market == 'crypto':
            new_low = round(qd.get_crypto_historical_data(symbol)['close'].min(),2)
        add_alert(symbol, new_low, 'below', 'New low', "price", market)

def create_moving_average_alerts(period):
    """
    Creates moving average alerts for a given period.

    Parameters:
    - period (int): The number of days to calculate the moving average.

    Returns:
    None
    """
    list_symbols = qd.get_all_symbols()
    for record in list_symbols:
        market = record[1]
        symbol = record[0]
        if market == 'tradfi':
            data = qd.get_tradfi_historical_data(symbol)
            if len(data) > 0:
                moving_average = round(data['close'].rolling(window=period).mean(), 2).tail(1).values[0] if len(qd.get_tradfi_historical_data(symbol)) > 0 else None
                price = round(qd.get_stock_last_price(symbol),2)
            else:
                continue
        elif market == 'crypto':
            data = qd.get_crypto_historical_data(symbol)
            if len(data) > 0:
                moving_average = round(data['close'].rolling(window=period).mean(),2).tail(1).values[0]
                price = round(qd.get_crypto_last_price(symbol),2)
            else:
                continue
        if price > moving_average:
            add_alert(symbol, moving_average, 'below', f"The current price of {symbol} is below its {period}-day moving average.", "dma", market)
        else:
            add_alert(symbol, moving_average, 'above', f"The current price of {symbol} is above its {period}-day moving average.", "dma", market)

def create_bollinger_bands_alerts():
    list_symbols = qd.get_all_symbols()
    for record in list_symbols:
        market = record[1]
        symbol = record[0]
        if market == 'tradfi':
            df = qd.get_tradfi_historical_data(symbol)
        elif market == 'crypto':
            df = qd.get_crypto_historical_data(symbol)
        
        price = round(df['close'].iloc[-1],2)
        bbup = round((df['close'].rolling(20).mean() + df['close'].rolling(20).std() * 2).iloc[-1], 2)
        bbdown = round((df['close'].rolling(20).mean() - df['close'].rolling(20).std() * 2).iloc[-1], 2)

        if price > bbdown:
            add_alert(symbol, bbdown, 'below', f"The current price of {symbol} is below its BBdown band.", "bb", market)
        if price < bbup:
            add_alert(symbol, bbup, 'above', f"The current price of {symbol} is above its BBup band.", "bb", market)

def create_rsi_alerts():
    """
    Creates RSI alerts for all symbols.

    This function retrieves historical data for each symbol and calculates the RSI (Relative Strength Index).
    If the RSI is above 85, it adds an alert indicating that the symbol may be overbought.
    If the RSI is below 25, it adds an alert indicating that the symbol may be oversold.
    The alerts are added using the `add_alert` function.

    Parameters:
        None

    Returns:
        None
    """
    list_symbols = qd.get_all_symbols()
    for record in list_symbols:
        market = record[1]
        symbol = record[0]
        if market == 'tradfi':
            df = qd.get_tradfi_historical_data(symbol)
        elif market == 'crypto':
            df = qd.get_crypto_historical_data(symbol)
        
        rsi = ti.rsi(df, 7)

        if rsi < 70:
            add_alert(symbol, 85, 'above', f"The RSI of {symbol} is above 85, indicating it may be overbought.", "rsi", market)
        if rsi > 30:
            add_alert(symbol, 25, 'below', f"The RSI of {symbol} is below 25, indicating it may be oversold.", "rsi", market)

def get_binance_twap(symbol):
    # Get the historical trades
    trades = client.get_historical_trades(symbol=symbol)

    # Calculate the TWAP
    prices = np.array([float(trade['price']) for trade in trades])
    times = np.array([float(trade['time']) / 1000 for trade in trades])  # Convert to seconds
    weights = np.diff(times, prepend=times[0])
    twap = np.average(prices, weights=weights)

    now = datetime.now()

    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")


    print(f'{dt_string} | {symbol}@{prices[-1]} -> TWAP: {round(twap,2)}')

def get_binance_oi_change(symbol, prev_open_interest, threshold=1000):

    # Get the open interest
    open_interest = client.futures_open_interest(symbol=symbol)
    oi = float(open_interest['openInterest'])
    # If this is the first iteration, set prev_open_interest and continue
    if prev_open_interest is None:
        return oi


    # If the open interest has changed drastically, print an alert
    if abs(oi - float(prev_open_interest)) >= threshold:
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | OI on {symbol} has changed drastically: {prev_open_interest} -> {oi}')

    return oi

def add_bulk_alerts():

    df = pd.read_excel('data\\bulk_alerts.xls')

    # Convert the dataframe to JSON format and save it
    df.to_json('alerts_bulk.json', orient='records')

    with open('alerts.json', 'r') as file:
        alerts = json.load(file)

    with open('alerts_bulk.json', 'r') as file:
        bulk_alerts = json.load(file)

    alerts += bulk_alerts

    with open('alerts.json', 'w') as file:
        json.dump(alerts, file)