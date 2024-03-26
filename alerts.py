import json
import requests
import yfinance as yf

def read_config(file_path):
    """
    Reads the configuration file and returns the alerts, telegram bot token, and telegram chat ID.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        tuple: A tuple containing the alerts (list), telegram bot token (str), and telegram chat ID (str).
    """
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config['alerts'], config['telegram_bot_token'], config['telegram_chat_id']

def write_config(file_path, alerts, bot_token, chat_id):
    """
    Writes the alerts, telegram bot token, and telegram chat ID to the configuration file.

    Args:
        file_path (str): The path to the configuration file.
        alerts (list): The list of alerts.
        bot_token (str): The telegram bot token.
        chat_id (str): The telegram chat ID.
    """
    with open(file_path, 'w') as file:
        json.dump({'alerts': alerts, 'telegram_bot_token': bot_token, 'telegram_chat_id': chat_id}, file)

def get_stock_price(stock):
    """
    Retrieves the last price of a stock using its symbol.

    Args:
        stock (str): The stock symbol.

    Returns:
        float: The last price of the stock.
    """
    ticker = yf.Ticker(stock)
    return ticker.fast_info['lastPrice']

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
    stock = input('Enter stock symbol: ').upper()
    level = float(input('Enter level: '))
    move = input('Enter move (above/below): ').lower()
    alerts, bot_token, chat_id = read_config('config.json')
    alerts.append({'stock': stock, 'level': level, 'move': move})
    write_config('config.json', alerts, bot_token, chat_id)

def run_alerts():
    """
    Runs the alerts and sends Telegram messages if the stock price meets the alert criteria.
    """
    alerts, bot_token, chat_id = read_config('config.json')
    for alert in alerts:
        stock = alert['stock']
        level = alert['level']
        move = alert['move']
        price = get_stock_price(stock)
        if (price > level and move == 'above') or (price < level and move == 'below'):
            send_telegram_message(bot_token, chat_id, f'Stock {stock} is now at {price}')

def delete_all_alerts():
    """
    Deletes all alerts from the configuration file.
    """
    _, bot_token, chat_id = read_config('config.json')
    write_config('config.json', [], bot_token, chat_id)

def print_all_alerts():
    """
    Prints all alerts from the configuration file.
    """
    alerts, _, _ = read_config('config.json')
    for alert in alerts:
        print(f"Stock: {alert['stock']}, Level: {alert['level']}, Move: {alert['move']}")

def main():
    """
    The main function that displays the menu and handles user input.
    """
    while True:
        print('1. Add alert')
        print('2. Run alerts')
        print('3. Delete all alerts')
        print('4. Print all alerts')
        print('5. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            add_alert()
        elif choice == '2':
            try:
                while True:
                    run_alerts()
            except KeyboardInterrupt:
                pass
        elif choice == '3':
            delete_all_alerts()
        elif choice == '4':
            print_all_alerts()
        elif choice == '5':
            break

if __name__ == "__main__":
    main()