from src import json_functions as jf
from src import quote_data as qd
from src import telegram_con as tg

def add_alert_interactive():
    """
    Adds a new alert to the configuration file.
    """
    symbol = input('Enter the symbol: ').upper(); print(f"{symbol} does not exist.") if qd.get_stock_last_price(symbol) is None else None
    level = next((float(level_input) for level_input in iter(lambda: input('Enter the price level: '), 'q') if level_input.replace('.','',1).isdigit()), 'q')
    move = ''
    while (move := input('Enter the move (above/below): ').lower()) not in ['above', 'below']: print("Invalid move. Please enter 'above' or 'below'.")
    reason = input('Enter the reason for the alert: ').lower()
    market = input('Enter the market for the alert (tradfi/crypto): ').lower()

    alert = {'symbol': symbol, 'level': level, 'move': move, 'reason': reason, 'market': market, 'alert_type': 'manual'}
    alerts = jf.read_alerts('alerts.json')
    alerts.append(alert)
    jf.write_alerts('alerts.json', alerts)

def add_alert(symbol, level, move, reason, market='stock'):
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
        'alert_type': "automatic"
    }
    alerts = jf.read_alerts('alerts.json')
    alerts.append(alert)
    jf.write_alerts('alerts.json', alerts)
    print(f"Alert added for stock {symbol} when it moves {move} {level}. Reason: {reason}")

def run_alerts():
    """
    Runs all alerts and sends a message if the stock price is above or below the alert level.
    If an alert is triggered, it is deleted.
    """
    alerts = jf.read_alerts('alerts.json')

    new_alerts = []
    for alert in alerts:
        symbol = alert['symbol']
        level = alert['level']
        move = alert['move']
        reason = alert['reason']
        market = alert['market']
        if market == 'tradfi':
            price = qd.get_stock_last_price(symbol)
        else:
            price = qd.get_crypto_last_price(symbol)

        if price is not None:
            price = round(price, 2)
        else:
            print(f"Could not get the price for stock {symbol}. Skipping this stock.")
            continue

        if market == "tradefi":
            finviz = f"https://finviz.com/{'crypto_charts' if '-USD' in symbol else 'quote'}.ashx?t={symbol.replace('-USD', 'USD')}&p=d"
        else:
            finviz = ""

        if '50-day moving average' in alert['reason']:
            if (price > level * 1.01 and move == 'above') or (price < level * 0.99 and move == 'below'):
                arrow = '↑' if move == 'above' else '↓'
                tg.send_telegram_message(f'${symbol} is now at {price} ({arrow} {level} 50DMA). Reason: {reason} | {finviz}')
            else:
                new_alerts.append(alert)
        else:
            if (price > level and move == 'above') or (price < level and move == 'below'):
                arrow = '↑' if move == 'above' else '↓'
                tg.send_telegram_message(f'${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {finviz}')
            else:
                new_alerts.append(alert)
    jf.write_alerts('alerts.json', new_alerts)

def delete_all_alerts():
    """
    Deletes all alerts of a specific type from the configuration file after confirmation.
    """
    alert_type = input('Enter the alert type to delete: (automatic/manual)').lower()
    confirmation = input(f'Are you sure you want to delete all alerts of type {alert_type}? (yes/no): ').lower()
    if confirmation == 'yes':
        alerts = jf.read_alerts('alerts.json')
        alerts = [alert for alert in alerts if alert['alert_type'] != alert_type]
        jf.write_alerts('alerts.json', alerts)
    else:
        print("Operation cancelled.")

def print_all_alerts():
    """
    Prints all alerts from the configuration file.
    """
    alerts = jf.read_alerts('alerts.json')
    for alert in alerts:
        if alert['alert_type'] == 'manual':
            print(f"Stock: {alert['stock']}, Level: {alert['level']}, Move: {alert['move']}, Reason: {alert['reason']}")

def delete_alerts_for_stock():
    """
    Deletes all alerts for a specific stock from the configuration file.
    """
    stock = input('Enter the stock symbol: ').upper()
    alerts = jf.read_alerts('alerts.json')
    alerts = [alert for alert in alerts if alert['stock'] != stock]
    jf.write_alerts('alerts.json', alerts)

def create_alerts_for_new_all_time_highs():
    """
    Creates alerts for new all-time highs for symbols in the market.
    """
    list_symbols = qd.get_all_symbols()
    for symbol in list_symbols:
        market = symbol[1]
        if symbol[1] == 'tradfi':
            all_time_high = round(qd.get_all_time_high(symbol[0]), 2)
        else:
            all_time_high = round(qd.get_crypto_historical_data(symbol[0])['close'].max(),2)
        add_alert(symbol[0], all_time_high, 'above', 'New all-time high', market)

def create_alerts_for_new_all_time_lows():
    """
    Creates alerts for new all-time lows for symbols.
    
    This function retrieves a list of symbols using `qd.get_all_symbols()`.
    For each symbol, it checks the market type and calculates the all-time low value.
    If the market type is 'tradfi', it uses `qd.get_all_time_low()` to get the all-time low value.
    If the market type is not 'tradfi', it uses `qd.get_crypto_historical_data()` to get the minimum close value.
    Finally, it calls the `add_alert()` function to add an alert for the symbol with the all-time low value.
    """
    list_symbols = qd.get_all_symbols()
    for symbol in list_symbols:
        market = symbol[1]
        if symbol[1] == 'tradfi':
            all_time_low = round(qd.get_all_time_low(symbol[0]), 2)
        else:
            all_time_low = round(qd.get_crypto_historical_data(symbol[0])['close'].min(),2)
        add_alert(symbol[0], all_time_low, 'below', 'New 52 week low', market)

def create_moving_average_alerts():
    """
    Adds an alert if the stock's current price is above or below its 50-day moving average.

    Parameters:
    stock (str): The stock symbol.

    Returns:
    None
    """
    list_symbols = qd.get_all_symbols()
    for symbol in list_symbols:
        market = symbol[1]
        if symbol[1] == 'tradfi':
            moving_average = round(qd.get_tradfi_historical_data(symbol[0])['close'].rolling(window=50).mean(), 2).tail(1).values[0]
        else:
            moving_average = round(qd.get_crypto_historical_data(symbol[0])['close'].rolling(window=50).mean(),2).tail(1).values[0]

        add_alert(symbol[0], moving_average, 'above', f"The current price of {symbol[0]} is above its 50-day moving average.", market)
        add_alert(symbol[0], moving_average, 'below', f"The current price of {symbol[0]} is below its 50-day moving average.", market)
