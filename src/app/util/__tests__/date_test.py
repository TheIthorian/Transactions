from datetime import datetime
from app.util.date import (
    DAYS_IN_MONTH,
    get_full_day_difference,
    get_full_month_difference,
    get_month_difference,
    to_integer,
)


class Test_to_integer:
    def test_returns_none_when_given_none(self):
        assert to_integer(None) == None

    def test_returns_miliseconds_since_unix_epoch_datetime(self):
        assert to_integer(datetime(2022, 1, 1, 1, 1, 1, 1)) == 1640998861

    def test_returns_miliseconds_since_unix_epoch_date(self):
        assert to_integer(datetime(2022, 1, 1).date()) == 1640995200


class Test_Date_Difference:
    def test_get_full_month_difference(self):
        end_date = datetime(2022, 10, 5).date()
        assert get_full_month_difference(end_date, end_date) == 0
        assert get_full_month_difference(end_date, datetime(2022, 9, 5).date()) == 1
        assert get_full_month_difference(end_date, datetime(2022, 11, 1).date()) == 0

        assert get_full_month_difference(end_date, datetime(2022, 11, 5).date()) == -1

        assert get_full_month_difference(end_date, datetime(2022, 2, 5).date()) == 8

        assert get_full_month_difference(end_date, datetime(2021, 11, 30).date()) == 10

    def test_get_full_day_difference(self):
        end_date = datetime(2022, 10, 5).date()
        assert get_full_day_difference(end_date, end_date) == 0
        assert get_full_day_difference(end_date, datetime(2022, 9, 5).date()) == 30
        assert get_full_day_difference(end_date, datetime(2022, 11, 5).date()) == -31

        assert get_full_day_difference(end_date, datetime(2022, 2, 5).date()) == 242

        assert get_full_day_difference(end_date, datetime(2021, 11, 30).date()) == 309

    def test_get_month_difference(self):
        end_date = datetime(2022, 10, 5).date()
        assert get_month_difference(end_date, end_date) == 0
        assert (
            get_month_difference(end_date, datetime(2021, 11, 30).date())
            == 309 / DAYS_IN_MONTH
        )
