#!/usr/bin/env python3

from datetime import datetime, timezone, timedelta


def translate_to_timezone(date: datetime, to_tz: int, from_tz: int = None):
    if from_tz is not None:
        source_tz = timezone(timedelta(hours=from_tz))
    else:
        source_tz = timezone.utc

    return date.replace(tzinfo=source_tz).astimezone(
        tz=timezone(timedelta(hours=to_tz))
    )


def normalize_datetime(date: datetime) -> datetime:
    """Round the seconds in the given datetime

    >>> normalize_datetime(datetime(2021, 6, 9, 2, 30, 29))
    datetime.datetime(2021, 6, 9, 2, 30)

    >>> normalize_datetime(datetime(2021, 6, 9, 2, 30, 30))
    datetime.datetime(2021, 6, 9, 2, 31)

    >>> normalize_datetime(datetime(2021, 6, 9, 23, 59, 59))
    datetime.datetime(2021, 6, 10, 0, 0)

    >>> normalize_datetime(datetime(2021, 12, 31, 23, 59, 59))
    datetime.datetime(2022, 1, 1, 0, 0)
    """

    new_date = datetime(date.year, date.month, date.day, date.hour, date.minute)

    if date.second >= 30:
        new_date += timedelta(minutes=1)

    return new_date
