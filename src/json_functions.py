
import json

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
