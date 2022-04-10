import datetime
import pandas as pd


def parse_datetime(date: str, format="%d-%m-%Y") -> datetime.datetime:
    return datetime.datetime.strptime(date.strip(), format)


def date_range(start: datetime.datetime, end: datetime.datetime, freq="M"):
    dr = pd.date_range(start=start, end=end, freq=freq)
    return [start] + list(dr.to_pydatetime()) + [end]
