import json
import requests
import yfinance as yf

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

def get_stock_price(stock):
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

def add_alert():
    """
    Adds a new alert to the configuration file.
    """
    stock = input('Enter the stock symbol: ').upper()
    if get_stock_price(stock) is None:
        print(f"Stock {stock} does not exist.")
        return
    level = float(input('Enter the price level: '))
    move = ''
    while move not in ['above', 'below']:
        move = input('Enter the move (above/below): ').lower()
        if move not in ['above', 'below']:
            print("Invalid move. Please enter 'above' or 'below'.")
    reason = input('Enter the reason for the alert: ').lower()
    alert = {'stock': stock, 'level': level, 'move': move, 'reason': reason}
    alerts = read_alerts('alerts.json')
    alerts.append(alert)
    write_alerts('alerts.json', alerts)

def run_alerts():
    """
    Runs the alerts and sends Telegram messages if the stock price meets the alert criteria.
    """
    bot_token, chat_id = read_config('config.json')
    alerts = read_alerts('alerts.json')
    for alert in alerts:
        stock = alert['stock']
        level = alert['level']
        move = alert['move']
        reason = alert['reason']
        price = get_stock_price(stock)
        if (price > level and move == 'above') or (price < level and move == 'below'):
            arrow = '↑' if move == 'above' else '↓'
            send_telegram_message(bot_token, chat_id, f'Stock {stock} is now at {price} ({arrow} {level}). Reason: {reason}')

def delete_all_alerts():
    """
    Deletes all alerts from the configuration file after confirmation.
    """
    confirmation = input('Are you sure you want to delete all alerts? (yes/no): ').lower()
    if confirmation == 'yes':
        _ = read_alerts('alerts.json')
        write_alerts('alerts.json', [])
    else:
        print("Operation cancelled.")

def print_all_alerts():
    """
    Prints all alerts from the configuration file.
    """
    alerts = read_alerts('alerts.json')
    for alert in alerts:
        print(f"Stock: {alert['stock']}, Level: {alert['level']}, Move: {alert['move']}")

def delete_alerts_for_stock():
    """
    Deletes all alerts for a specific stock from the configuration file.
    """
    stock = input('Enter the stock symbol: ').upper()
    alerts = read_alerts('alerts.json')
    alerts = [alert for alert in alerts if alert['stock'] != stock]
    write_alerts('alerts.json', alerts)

def main():
    """
    The main function that displays the menu and handles user input.
    """
    while True:
        print('1. Add alert')
        print('2. Run alerts')
        print('3. Delete all alerts')
        print('4. Delete alerts for a stock')
        print('5. Print all alerts')
        print('6. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            add_alert()
        elif choice == '2':
            run_alerts()
        elif choice == '3':
            delete_all_alerts()
        elif choice == '4':
            delete_alerts_for_stock()
        elif choice == '5':
            print_all_alerts()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()