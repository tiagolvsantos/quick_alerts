# Stock Alert System

This is a stock alert system written in Python. It allows users to set alerts for specific stocks and notifies them when the stock reaches a certain level or hits a new all-time high or low.

## Features

1. Add alert: Users can add a new alert for a specific stock.
2. Run alerts: The system checks all alerts and notifies the user if any stock has reached the alert level.
3. Delete all alerts: Users can delete all alerts.
4. Delete alerts for a stock: Users can delete all alerts for a specific stock.
5. Print all alerts: The system prints all alerts to the console.
6. Create alerts for new all-time highs: The system creates alerts for all S&P 500 stocks when they reach a new all-time high.
7. Create alerts for new all-time lows: The system creates alerts for all S&P 500 stocks when they reach a new all-time low.
8. Create alerts 50 DMA crossing
9. Exit: Exit the application.

## How to Run
- Set telegram_bot_token and telegram_chat_id as environment vars on your system 
- To run this application, navigate to the directory containing the `main.py` file in your terminal and type `python main.py`.

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