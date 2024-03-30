import requests


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
