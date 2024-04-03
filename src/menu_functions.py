from src import json_functions as jf
from src import quote_data as qd
from src import telegram_con as tg
from src import technical_indicators as ti

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
    market = input('Enter the market for the alert (tradfi/crypto): ').lower()

    alert = {'symbol': symbol, 'level': level, 'move': move, 'reason': reason, 'market': market, 'alert_type': 'price', 'type': 'manual'}
    alerts = jf.read_alerts('alerts.json')
    alerts.append(alert)
    jf.write_alerts('alerts.json', alerts)

def add_alert(symbol, level, move, reason, alert_type, market='stock'):
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
    print(f"Alert added for stock {symbol} when it moves {move} {level}. Reason: {reason}")

def run_alerts(run_alerts_command):
    """
    Runs the alerts based on the specified criteria.

    Args:
        run_alerts_command (bool): Indicates whether to actually send the alerts or just print them.

    Returns:
        None
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

        if market == "tradfi" and "=" not in symbol and "." not in symbol:
            asset_url = f"https://finviz.com/{'crypto_charts' if '-USD' in symbol else 'quote'}.ashx?t={symbol.replace('-USD', 'USD')}&p=d"
        elif market == "crypto":
            asset_url = f"https://www.tradingview.com/symbols/{symbol.replace('-USD', 'USD')}/"
        elif market == "tradfi" and "=" in symbol or "." in symbol:
            asset_url = f"https://finance.yahoo.com/quote/{symbol}?.tsrc=fin-srch"
        else:
            asset_url = ""

        if 'dma' in alert['alert_type']:
            if (price > level * 1.01 and move == 'above') or (price < level * 0.99 and move == 'below'):
                arrow = '↑' if move == 'above' else '↓'
                if run_alerts_command:
                    tg.send_telegram_message(f'${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
                print(f'${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
            else:
                new_alerts.append(alert)

        elif 'bb' in alert['alert_type']:
                if (price > level * 1.01 and move == 'above') or (price < level * 0.99 and move == 'below'):
                    arrow = '↑' if move == 'above' else '↓'
                    if run_alerts_command:
                        tg.send_telegram_message(f'${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
                    print(f'${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
                else:
                    new_alerts.append(alert)

        elif 'price' in alert['alert_type']:
            if (price > level and move == 'above') or (price < level and move == 'below'):
                arrow = '↑' if move == 'above' else '↓'
                if run_alerts_command:
                    tg.send_telegram_message(f'${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
                print(f'${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
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
                    print(f'${symbol} is now at {price} ({arrow} {level}). Reason: {reason} | {asset_url}')
            else:
                new_alerts.append(alert)
    _delete_alerts('automatic')
    jf.write_alerts('alerts.json', new_alerts)

def delete_all_alerts():
    """
    Deletes all alerts of a specific type from the configuration file after confirmation.
    """
    type = input('Enter the alert type to delete: (automatic/manual)').lower()
    confirmation = input(f'Are you sure you want to delete all alerts of type {type}? (yes/no): ').lower()
    if confirmation == 'yes':
        alerts = jf.read_alerts('alerts.json')
        alerts = [alert for alert in alerts if alert['type'] != type]
        jf.write_alerts('alerts.json', alerts)
    else:
        print("Operation cancelled.")

def print_symbol_alert():
    """
    Prints all alerts from the configuration file.
    """
    symbol = input('Enter the symbol: ').upper(); print(f"{symbol} does not exist.") if 'USDT' not in symbol and qd.get_stock_last_price(symbol) is None else None
    alerts = jf.read_alerts('alerts.json')
    for alert in alerts:
        if alert['alert_type'] == 'manual' and alert['symbol'] == symbol:
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
            all_time_high = round(qd.get_all_time_high(symbol), 2)
        elif market == 'crypto':
            all_time_high = round(qd.get_crypto_historical_data(symbol)['close'].max(),2)
        add_alert(symbol, all_time_high, 'above', 'New high', "price", market)

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
            all_time_low = round(qd.get_all_time_low(symbol), 2)
        elif market == 'crypto':
            all_time_low = round(qd.get_crypto_historical_data(symbol)['close'].min(),2)
        add_alert(symbol, all_time_low, 'below', 'New low', "price", market)

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
    If the RSI is above 70, it adds an alert indicating that the symbol may be overbought.
    If the RSI is below 30, it adds an alert indicating that the symbol may be oversold.
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
        
        rsi = ti.rsi(df)

        if rsi < 70:
            add_alert(symbol, 70, 'above', f"The RSI of {symbol} is above 70, indicating it may be overbought.", "rsi", market)
        if rsi > 30:
            add_alert(symbol, 30, 'below', f"The RSI of {symbol} is below 30, indicating it may be oversold.", "rsi", market)