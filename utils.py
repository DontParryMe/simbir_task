import csv
from datetime import datetime


def get_current_day():
    current_date = datetime.now()
    return current_date.day


def fibonacci(n: int) -> int:
    if n <= 0:
        raise Exception('fibonacci: Unexpected n')
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        a, b = 0, 1
        for _ in range(3, n + 1):
            a, b = b, a + b
        return b


def format_date(date_string: str) -> str:
    date_format = "%b %d, %Y %I:%M:%S %p"
    parsed_date = datetime.strptime(date_string, date_format)
    formatted_date = parsed_date.strftime("%d %B %Y %H:%M:%S")
    return formatted_date


def is_date(date_string: str) -> bool:
    date_format = "%b %d, %Y %I:%M:%S %p"
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False


def write_csv(transactions, filename="output.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        for row_data in transactions:
            csv_writer.writerow(row_data)
