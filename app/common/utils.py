import datetime


def parse_datetime(date: str, format="%d-%m-%Y") -> datetime.datetime:
    return datetime.datetime.strptime(date.strip(), format)
