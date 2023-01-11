import pytz
import datetime
import time

def get_current_date():
    current_time = datetime.datetime.now(pytz.timezone('Asia/Tashkent')).date()
    return current_time.strftime('%Y-%m-%d')