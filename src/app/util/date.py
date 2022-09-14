from datetime import date, datetime
import time
from typing import Union


def to_integer(dt_time: Union[datetime, date]):
    return time.mktime(dt_time.timetuple())
