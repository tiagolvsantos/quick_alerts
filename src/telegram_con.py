import requests
import os

def send_telegram_message(message):
    """
    Sends a message to a Telegram chat using the provided bot token and chat ID.

    Args:
        message (str): The message to send.
    """
    bot_token = os.getenv('telegram_bot_token')
    chat_id = os.getenv('telegram_chat_id')
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)
