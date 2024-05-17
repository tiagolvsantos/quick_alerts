# Financial assets alerts system

This is a stock alert system written in Python. It allows users to set alerts for specific stocks and notifies them when the stock reaches a certain level or hits a new all-time high or low.

## Modules

- `json_functions`: This module contains functions for handling JSON data.
- `quote_data`: This module contains functions for handling quote data.
- `telegram_con`: This module contains functions for handling Telegram connections.
- `technical_indicators`: This module contains functions for calculating technical indicators.


## Features

Our application provides a variety of features to help you manage your alerts:

1. **Add Alert**: Add a new alert.
2. **Run Alerts**: Run all existing alerts.
3. **Delete Type Alerts**: Delete all alerts of a specific type.
4. **Delete Alerts for a Symbol**: Delete all alerts associated with a specific symbol.
5. **Print Manual Alerts**: Print all manual alerts.
6. **Print Symbol Alerts**: Print all alerts associated with a specific symbol.
7. **Create Alerts for New Highs/Lows**: Create alerts for new highs or lows.
8. **Create Alerts 50 DMA**: Create alerts for 50-day moving averages.
9. **Create Alerts BBbands Outside Bands**: Create alerts for Bollinger Bands outside bands.
10. **Create Alerts RSI**: Create alerts for Relative Strength Index (RSI).
11. **Exit**: Exit the application.

### Options

- **Enable Sound**: Enable sound for alerts.
- **Add Bulk Alerts**: Add multiple alerts at once using a `bulk_alerts.xls` file.


## How to Run
- If you want to run alerts on telegram:
  - Set telegram_bot_token and telegram_chat_id as environment vars on your system 
- To run this application, navigate to the directory containing the `main.py` file in your terminal and type `python main.py`.

### Command-Line Arguments

This application supports the following command-line arguments:

- `--run_alerts_command`: This argument is a boolean flag. If it's specified when running the script, the application will automatically run the alerts check (equivalent to choosing option '2' from the menu). If it's not specified, the application will start normally and wait for the user to choose an option from the menu.

Here's how you can use this argument:

```bash
python main.py --run_alerts_command
```

## Dependencies

This project requires Python 3.6 or higher and the following Python packages:

- yfinance
- pandas
- requests

You can install these packages using pip:
pip install yfinance pandas requests

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Images
![Alt text](https://github.com/tiagolvsantos/quick_alerts/blob/main/assets/running_alerts.png?raw=true)