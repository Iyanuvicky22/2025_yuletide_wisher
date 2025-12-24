"""
Pass
"""
import pandas as pd
import datetime as dt
import random
import smtplib


file_path = r"data\fourth_trial.csv"
data = pd.read_csv(file_path)

# check 
today = dt.datetime.now()
today_tuple = (today.month, today.day)
new_dict = {(data_row.month, data_row.day): data_row for (index, data_row) in data.iterrows()}

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        pass

except FileNotFoundError:
    file_path = r"birthdays.csv"
    data = pd.read_csv(file_path)


print(main.get_tsla_stock_price())