#!/usr/bin/python3
from datetime import datetime, timedelta

def get_month(text):
    dt = datetime.strptime(text, "%B")
    return dt.strftime("%B").upper()

def main():
    text = "SEPTEMBER"
    print(get_month(text))

main()
