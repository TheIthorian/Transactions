from datetime import date, datetime
import time
from typing import Union

DAYS_IN_YEAR = 365
MONTHS_IN_YEAR = 12
DAYS_IN_MONTH = DAYS_IN_YEAR / MONTHS_IN_YEAR


def to_integer(dt_time: Union[datetime, date]) -> int:
    if dt_time is None:
        return None
    return int(time.mktime(dt_time.timetuple()))


def get_full_month_difference(d1: date, d2: date) -> int:
    return (d1.year - d2.year) * MONTHS_IN_YEAR + d1.month - d2.month


def get_full_day_difference(d1: date, d2: date) -> int:
    return (
        (d1.year - d2.year) * DAYS_IN_YEAR
        + (d1.month - d2.month) * DAYS_IN_MONTH
        + d1.day
        + d2.day
    )


def get_month_difference(d1: date, d2: date) -> int:
    print("get_full_day_difference", get_full_day_difference(d1, d2))
    print("get_month_difference", get_full_day_difference(d1, d2) / DAYS_IN_MONTH)
    return get_full_day_difference(d1, d2) / DAYS_IN_MONTH
