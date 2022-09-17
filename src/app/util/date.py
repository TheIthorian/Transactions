from datetime import date, datetime
import time
from typing import Union


def to_integer(dt_time: Union[datetime, date]) -> int:
    if dt_time is None:
        return None
    return int(time.mktime(dt_time.timetuple()))
