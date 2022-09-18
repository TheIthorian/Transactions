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
    month_difference = (d1.year - d2.year) * MONTHS_IN_YEAR + d1.month - d2.month

    # Adjust for mid-month days
    month_difference += 1 if d1.day > d2.day else 0
    month_difference -= 1 if d1.day < d2.day else 0

    return month_difference


def get_full_day_difference(d1: date, d2: date) -> int:
    return (d1 - d2).days


def get_month_difference(d1: date, d2: date) -> int:
    return get_full_day_difference(d1, d2) / DAYS_IN_MONTH
