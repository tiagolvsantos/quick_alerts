import json
import requests
import yfinance as yf
import pandas as pd
import time

def read_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config['telegram_bot_token'], config['telegram_chat_id']

def read_alerts(file_path):
    with open(file_path, 'r') as file:
        alerts = json.load(file)
    return alerts

def write_alerts(file_path, alerts):
    with open(file_path, 'w') as file:
        json.dump(alerts, file)

def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a message to a Telegram chat using the provided bot token and chat ID.

    Args:
        bot_token (str): The Telegram bot token.
        chat_id (str): The Telegram chat ID.
        message (str): The message to send.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)

def add_alert_interactive():
    """
    Adds a new alert to the configuration file.
    """
    stock = input('Enter the stock symbol: ').upper()
    if _get_stock_price(stock) is None:
        print(f"Stock {stock} does not exist.")
        return
    level = float(input('Enter the price level: '))
    move = ''
    while move not in ['above', 'below']:
        move = input('Enter the move (above/below): ').lower()
        if move not in ['above', 'below']:
            print("Invalid move. Please enter 'above' or 'below'.")
    reason = input('Enter the reason for the alert: ').lower()
    alert = {'stock': stock, 'level': level, 'move': move, 'reason': reason, 'alert_type': 'manual'}
    alerts = read_alerts('alerts.json')
    alerts.append(alert)
    write_alerts('alerts.json', alerts)

def add_alert(stock, level, move, reason):
    """
    Adds a new alert.

    Parameters:
    stock (str): The stock symbol.
    level (float): The price level.
    move (str): The direction of the price movement ('above' or 'below').
    reason (str): The reason for the alert.
    """
    alert = {
        'stock': stock,
        'level': level,
        'move': move,
        'reason': reason,
        'alert_type': "automatic"
    }
    alerts = read_alerts('alerts.json')
    alerts.append(alert)
    write_alerts('alerts.json', alerts)
    print(f"Alert added for stock {stock} when it moves {move} {level}. Reason: {reason}")

def run_alerts():
    """
    Runs all alerts and sends a message if the stock price is above or below the alert level.
    If an alert is triggered, it is deleted.
    """
    bot_token, chat_id = read_config('config.json')
    alerts = read_alerts('alerts.json')
    new_alerts = []
    for alert in alerts:
        stock = alert['stock']
        level = alert['level']
        move = alert['move']
        reason = alert['reason']
        price = _get_stock_price(stock)

        if price is not None:
            price = round(price, 2)
        else:
            print(f"Could not get the price for stock {stock}. Skipping this stock.")
            continue

        if '50-day moving average' in alert['reason']:
            if (price > level * 1.01 and move == 'above') or (price < level * 0.99 and move == 'below'):
                arrow = '↑' if move == 'above' else '↓'
                send_telegram_message(bot_token, chat_id, f'Stock ${stock} is now at {price} ({arrow} {level}). Reason: {reason}')
            else:
                new_alerts.append(alert)
        else:
            if (price > level and move == 'above') or (price < level and move == 'below'):
                arrow = '↑' if move == 'above' else '↓'
                send_telegram_message(bot_token, chat_id, f'Stock ${stock} is now at {price} ({arrow} {level}). Reason: {reason}')
            else:
                new_alerts.append(alert)
    write_alerts('alerts.json', new_alerts)

def delete_all_alerts():
    """
    Deletes all alerts of a specific type from the configuration file after confirmation.
    """
    alert_type = input('Enter the alert type to delete: (automatic/manual)').lower()
    confirmation = input(f'Are you sure you want to delete all alerts of type {alert_type}? (yes/no): ').lower()
    if confirmation == 'yes':
        alerts = read_alerts('alerts.json')
        alerts = [alert for alert in alerts if alert['alert_type'] != alert_type]
        write_alerts('alerts.json', alerts)
    else:
        print("Operation cancelled.")

def print_all_alerts():
    """
    Prints all alerts from the configuration file.
    """
    alerts = read_alerts('alerts.json')
    for alert in alerts:
        if alert['alert_type'] == 'manual':
            print(f"Stock: {alert['stock']}, Level: {alert['level']}, Move: {alert['move']}, Reason: {alert['reason']}")

def delete_alerts_for_stock():
    """
    Deletes all alerts for a specific stock from the configuration file.
    """
    stock = input('Enter the stock symbol: ').upper()
    alerts = read_alerts('alerts.json')
    alerts = [alert for alert in alerts if alert['stock'] != stock]
    write_alerts('alerts.json', alerts)

def create_alerts_for_new_all_time_highs():
    """
    Creates an alert for each stock in the S&P 500 when it reaches a new all-time high.
    """
    sp500_stocks = _get_stocks()
    for stock in sp500_stocks:
        all_time_high = _get_all_time_high(stock)
        add_alert(stock, all_time_high, 'above', 'New all-time high')

def create_alerts_for_new_all_time_highs():
    """
    Creates an alert for each stock in the S&P 500 when it reaches a new all-time high.
    """
    sp500_stocks = _get_stocks()
    for stock in sp500_stocks:
        all_time_high = round(_get_all_time_high(stock),2)
        add_alert(stock, all_time_high, 'above', 'New all-time high')  

def create_alerts_for_new_all_time_lows():
    """
    Creates an alert for each stock in the S&P 500 when it reaches a new all-time low.
    """
    sp500_stocks = _get_stocks()
    for stock in sp500_stocks:
        all_time_low = round(_get_all_time_low(stock), 2)
        add_alert(stock, all_time_low, 'below', 'New all-time low')    

def create_alerts_for_new_all_time_lows():
    """
    Creates an alert for each stock in the S&P 500 when it reaches a new all-time low.
    """
    sp500_stocks = _get_stocks()
    for stock in sp500_stocks:
        all_time_low = round(_get_all_time_low(stock), 2)
        add_alert(stock, all_time_low, 'below', 'New all-time low')    

def create_moving_average_alerts():
    """
    Adds an alert if the stock's current price is above or below its 50-day moving average.

    Parameters:
    stock (str): The stock symbol.

    Returns:
    None
    """
    sp500_stocks = _get_stocks()
    for stock in sp500_stocks:   
        data = yf.download(stock, period="50d",progress=False)
        moving_average = round(data['Close'].mean(),2)
        add_alert(stock, moving_average, 'above', f"The current price of {stock} is above its 50-day moving average.")
        add_alert(stock, moving_average, 'below', f"The current price of {stock} is below its 50-day moving average.")

def _get_stock_price(stock):
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

def _get_all_time_high(stock):
    """
    Returns the all-time high price for a stock.
    """
    data = yf.Ticker(stock)
    history = data.history(period="max")
    return history['High'].max()

def _get_all_time_low(stock):
    """
    Returns the all-time low price for a stock.
    """
    data = yf.Ticker(stock)
    history = data.history(period="max")
    return history['Low'].min()

def _get_stocks():
    """
    Returns a list of all S&P 500 stocks.
    """
    stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'BRK-B', 'V', 'JNJ', 'WMT', 'JPM',
          'ASML','COST','MA','HD','MCD','LLY','NFLX','ACN','ADBE','AMGN','AVGO',
          'BAC','PEP','CRM','KO','CSCO','CVX','XOM','TSLA','DIS','NVDA','PYPL',
          'META','TSM','INTC','QCOM','TMUS','ABT','NKE','ORCL','UNH','ABBV',
          'LMT','RTX','TXN','IBM','NOW','AMD','NEE','DHR','HON','UPS','SBUX',
          'GS','MRK','CAT','MDT','BLK','CHTR','FIS','PLD','AMT','TMO','BMY',
          'NET','PLTR','ZM','SNOW','DOCU','ROKU','SQ','CRWD','SHOP','DDOG',
          'DKNG','PFE','CVS','GM','F','GE','WFC','C','BABA','JD','TGT','LOW',
          'GM', 'BKNG','UBER','LYFT','Z','EBAY','ETSY','ROKU','SNAP','PINS',
          'CMG','COIN','ARM','NKE','HUT','TSLA','NIO','FSLY','ZM','MATW','HI',
          'CSV','SCI','ANF','EL','STZ','BF-B','DEO','BUD','ABEV','MO','PM','LVS',
          'MGM','WYNN','RCL','CCL','NCLH','MAR','HLT','EXPE','BKNG','TRIP','LYV',
          'YUM','MKC','DNUT','GIS','HSY','KR','SHAK','TSN','HRL','DPZ','QSR','WEN',
          'AKAM','ZS','CRWD','NET','PANW','FTNT','CHKP','SPLK','DOCU',
          'BAC','CVS','WBA','COST','TGT','KR','WMT','DG','DLTR','COST','TJX','ROST',
          'HD','LOW','BBY','TSCO','ORLY','AZO','AAP','ULTA','LULU','RH','TJX',
          'CRWD','CROX','EXPE','ZIM','EURN','FRO','GNK','GOGL','NAT','NMM','SBLK',
          'STNG','FDX','UPS','FTNT','GFS','O','OXY','CVX','XOM','COP','PSX','VLO',
          'OLN','SWBI','MARA','RIOT','MSTR','HUT','HOOD','SEB','PLUG','TLRY','CGC',
          'AIR.PA','SAF.PA','RHM.DE','LDO.MI','ENGI.PA','ORA.PA','VIE.PA','SU.PA',
          'MC.PA','CDI.PA','KER.PA','RMS.PA','EL.PA','ADYEN.AS','ASML.AS','HEIA.AS',
          'MUV2.DE','SAP.DE','CAP.PA','AF.PA','BNP.PA','ACA.PA','CS.PA','BN.PA','GLE.PA',
          'ES=F','CL=F','NG=F','GC=F','SI=F','HG=F','NQ=F','RTY=F','BTC-USD',
          'ETH-USD','ADA-USD','BNB-USD','SOL1-USD','XRP-USD','DOGE-USD','LTC-USD']
    
    return list(set(stocks))


def main():
    """
    The main function that runs the menu loop.
    """
    while True:
        print_menu()
        choice = input('Enter your choice: ')
        if choice == '1':
            add_alert_interactive()
        elif choice == '2':
            try:
                while True:
                    run_alerts()
                    time.sleep(600)  # Sleep for 10 minutes
            except KeyboardInterrupt:
                print("Interrupted by user. Exiting...")
        elif choice == '3':
            delete_all_alerts()
        elif choice == '4':
            delete_alerts_for_stock()
        elif choice == '5':
            print_all_alerts()
        elif choice == '6':
            create_alerts_for_new_all_time_highs()
        elif choice == '7':
            create_alerts_for_new_all_time_lows()
        elif choice == '8':
            create_moving_average_alerts()
        elif choice == '9':
            print('Exiting...')
            break
        else:
            print('Invalid choice. Please try again.')

def print_menu():
    """
    Prints the menu.
    """
    print('1. Add alert')
    print('2. Run alerts')
    print('3. Delete all alerts')
    print('4. Delete alerts for a stock')
    print('5. Print all alerts')
    print('6. Create alerts for new all-time highs')
    print('7. Create alerts for new all-time lows')
    print('8. Create alerts 50 DMA')
    print('9. Exit')
if __name__ == "__main__":
    main()


