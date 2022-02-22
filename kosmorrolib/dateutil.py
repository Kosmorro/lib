#!/usr/bin/env python3

#    Kosmorrolib - The Library To Compute Your Ephemerides
#    Copyright (C) 2021  Jérôme Deuchnord <jerome@deuchnord.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from datetime import datetime, timezone, timedelta


def translate_to_timezone(date: datetime, to_tz: int):
    """Convert a datetime from a timezone to another.

    >>> translate_to_timezone(datetime(2021, 6, 9, 5, 0, 0, tzinfo=timezone.utc), 2)
    datetime.datetime(2021, 6, 9, 7, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)))

    >>> translate_to_timezone(datetime(2021, 6, 9, 5, 0, 0, tzinfo=timezone(timedelta(hours=1))), 2)
    datetime.datetime(2021, 6, 9, 6, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)))

    If the datetime has no timezone information, then it is interpreted as UTC:

    >>> translate_to_timezone(datetime(2021, 6, 9, 5, 0, 0), 2)
    datetime.datetime(2021, 6, 9, 7, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)))
    """
    source_tz = date.tzinfo if date.tzinfo is not None else timezone.utc

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

    new_date = datetime(
        date.year, date.month, date.day, date.hour, date.minute
    ).replace(microsecond=0)

    if date.second >= 30:
        new_date += timedelta(minutes=1)

    return new_date
