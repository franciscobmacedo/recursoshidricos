from typing import Literal, Union
import datetime
import logging
import pandas as pd
import unidecode

import calendar


def parse_datetime(date: str, format="%d-%m-%Y") -> datetime.datetime:
    return datetime.datetime.strptime(date.strip(), format)


def month_last_day(ts: Union[datetime.datetime, datetime.date]):
    return calendar.monthrange(ts.year, ts.month)[1]


def date_range(
    start: datetime.datetime, end: datetime.datetime, freq: Literal["MS", "YS"]
) -> list[list[datetime.datetime, datetime.datetime]]:
    """returns a list of lists of a month interval. Can be further improved for different freq."""
    dr = list(pd.date_range(start=start, end=end, freq=freq).to_pydatetime())
    if dr[-1] != end:
        dr = dr + [end]
    if freq == "MS":
        return [[d, d.replace(day=month_last_day(d))] for d in dr]
    elif freq == "YS":
        return [[d, datetime.datetime(d.year, 12, 31)] for d in dr]


# Print iterations progress
def print_progress_bar(
    iteration: int, total: int, prefix="", suffix="", decimals=1, length=100, fill="█"
):
    """
    Call in a loop to create terminal progress bar
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    logging.info(f"\r{prefix} |{bar}| {percent}% {suffix}")
    if iteration == total:
        logging.info("\n")


def string_contains_array(string: str, array: list) -> bool:
    clean_string = unidecode.unidecode(string.lower())
    return any(x in clean_string for x in array)
