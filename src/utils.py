from datetime import datetime, timedelta
import time
import datetime
from datetime import datetime
import pandas as pd
import os

def current_datetime_to_epoc(days_to_subtract: int):
    date_period = datetime.now() - timedelta(days=days_to_subtract)
    return date_period.timestamp()

def epoch_to_datetime(epoch_date: int):
    if len(str(epoch_date)) > 10:
        epoch_date = str(epoch_date)[:-3]
    timeArray = time.localtime(int(epoch_date))
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def isNaN(num):
    return num != num

def listToString(s): 
    return "".join(s) 

def ConvertList(var_list: list):
    it = iter(var_list)
    return dict(zip(it, it))

def get_year_date_first_day():
    return datetime.now().year

# "%d-%m-%Y"
def get_days_ytd(todays_date: str, date_format: str ):
    year = get_year_date_first_day()
    base_date = f"01-01-{year}"
    a = datetime.strptime(base_date, date_format)
    b = datetime.strptime(todays_date, date_format)
    daydiff = a.weekday() - b.weekday()
    return round(((b-a).days - daydiff) / 7 * 5 + min(daydiff,5) - (max(b.weekday() - 4, 0) % 5),0)

# '%Y-%m-%d'
def get_todays_date(date_format:str):
    return datetime.now().strftime(f'{date_format}')

def get_yesterdays_date(date_format:str):
    return (datetime.now() - timedelta(days=1)).strftime(f'{date_format}')

def get_last_n_days_date(date_format:str, n:int):
    return (datetime.now() - timedelta(days=n)).strftime(f'{date_format}')

def print_formated_numbers(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

def export_excel(file_path, df_data):
    if os.path.exists(file_path):
        os.remove(file_path)

    df_data.to_excel (file_path, index = None, header=True) 
