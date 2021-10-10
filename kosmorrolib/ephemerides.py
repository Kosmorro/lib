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

from datetime import date, datetime, timedelta
from typing import Union

from skyfield.searchlib import find_discrete, find_maxima
from skyfield.timelib import Time
from skyfield.constants import tau
from skyfield.errors import EphemerisRangeError

from .model import Position, AsterEphemerides, MoonPhase, Object, ASTERS
from .dateutil import translate_to_timezone, normalize_datetime
from .core import get_skf_objects, get_timescale, get_iau2000b
from .enum import MoonPhaseType
from .exceptions import OutOfRangeDateError

RISEN_ANGLE = -0.8333


def _get_skyfield_to_moon_phase(
    times: [Time], vals: [int], now: Time, timezone: int
) -> Union[MoonPhase, None]:
    tomorrow = get_timescale().utc(
        now.utc_datetime().year, now.utc_datetime().month, now.utc_datetime().day + 1
    )

    next_phase_time = None
    i = 0

    # Find the current moon phase:
    for i, time in enumerate(times):
        if now.utc_datetime() <= time.utc_datetime():
            if time.utc_datetime() >= tomorrow.utc_datetime():
                i -= 1
            break

    current_phase = MoonPhaseType(vals[i])

    if current_phase in [
        MoonPhaseType.NEW_MOON,
        MoonPhaseType.FIRST_QUARTER,
        MoonPhaseType.FULL_MOON,
        MoonPhaseType.LAST_QUARTER,
    ]:
        current_phase_time = translate_to_timezone(times[i].utc_datetime(), timezone)
    else:
        current_phase_time = None

    # Find the next moon phase
    for j in range(i + 1, len(times)):
        if vals[j] in [0, 2, 4, 6]:
            next_phase_time = translate_to_timezone(times[j].utc_datetime(), timezone)
            break

    return MoonPhase(current_phase, current_phase_time, next_phase_time)


def get_moon_phase(for_date: date = date.today(), timezone: int = 0) -> MoonPhase:
    """Calculate and return the moon phase for the given date, adjusted to the given timezone if any.

    Get the moon phase for the 27 March, 2021:

    >>> get_moon_phase(date(2021, 3, 27))
    <MoonPhase phase_type=MoonPhaseType.WAXING_GIBBOUS time=None next_phase_date=2021-03-28 18:48:10.902298+00:00>

    When the moon phase is a new moon, a first quarter, a full moon or a last quarter, you get the exact time
    of its happening too:

    >>> get_moon_phase(datetime(2021, 3, 28))
    <MoonPhase phase_type=MoonPhaseType.FULL_MOON time=2021-03-28 18:48:10.902298+00:00 next_phase_date=2021-04-04 10:02:27.393689+00:00>

    Get the moon phase for the 27 March, 2021, in the UTC+2 timezone:

    >>> get_moon_phase(date(2021, 3, 27), timezone=2)
    <MoonPhase phase_type=MoonPhaseType.WAXING_GIBBOUS time=None next_phase_date=2021-03-28 20:48:10.902298+02:00>

    Note that the moon phase can only be computed for a date range.
    Asking for the moon phase with an out of range date will result in an exception:

    >>> get_moon_phase(date(1000, 1, 1))
    Traceback (most recent call last):
        ...
    kosmorrolib.exceptions.OutOfRangeDateError: The date must be between 1899-08-09 and 2053-09-26
    """
    earth = get_skf_objects()["earth"]
    moon = get_skf_objects()["moon"]
    sun = get_skf_objects()["sun"]

    def moon_phase_at(time: Time):
        time._nutation_angles = get_iau2000b(time)
        current_earth = earth.at(time)
        _, mlon, _ = current_earth.observe(moon).apparent().ecliptic_latlon("date")
        _, slon, _ = current_earth.observe(sun).apparent().ecliptic_latlon("date")
        return (((mlon.radians - slon.radians) // (tau / 8)) % 8).astype(int)

    moon_phase_at.rough_period = 7.0  # one lunar phase per week

    today = get_timescale().utc(for_date.year, for_date.month, for_date.day)
    start_time = get_timescale().utc(for_date.year, for_date.month, for_date.day - 10)
    end_time = get_timescale().utc(for_date.year, for_date.month, for_date.day + 10)

    try:
        times, phases = find_discrete(start_time, end_time, moon_phase_at)
        return _get_skyfield_to_moon_phase(times, phases, today, timezone)

    except EphemerisRangeError as error:
        start = translate_to_timezone(error.start_time.utc_datetime(), timezone)
        end = translate_to_timezone(error.end_time.utc_datetime(), timezone)

        start = date(start.year, start.month, start.day) + timedelta(days=12)
        end = date(end.year, end.month, end.day) - timedelta(days=12)

        raise OutOfRangeDateError(start, end) from error


def get_ephemerides(
    position: Position, for_date: date = date.today(), timezone: int = 0
) -> [AsterEphemerides]:
    """Compute and return the ephemerides for the given position and date, adjusted to the given timezone if any.

    Compute the ephemerides for June 9th, 2021:

    >>> pos = Position(50.5824, 3.0624)
    >>> get_ephemerides(pos, date(2021, 6, 9))
    [<AsterEphemerides rise_time=2021-06-09 03:36:00 culmination_time=2021-06-09 11:47:00 set_time=2021-06-09 19:58:00 aster=<Object type=STAR name=SUN />>, <AsterEphemerides rise_time=2021-06-09 02:59:00 culmination_time=2021-06-09 11:02:00 set_time=2021-06-09 19:16:00 aster=<Object type=SATELLITE name=MOON />>, <AsterEphemerides rise_time=2021-06-09 04:06:00 culmination_time=2021-06-09 11:58:00 set_time=2021-06-09 19:49:00 aster=<Object type=PLANET name=MERCURY />>, <AsterEphemerides rise_time=2021-06-09 04:52:00 culmination_time=2021-06-09 13:13:00 set_time=2021-06-09 21:34:00 aster=<Object type=PLANET name=VENUS />>, <AsterEphemerides rise_time=2021-06-09 06:38:00 culmination_time=2021-06-09 14:40:00 set_time=2021-06-09 22:41:00 aster=<Object type=PLANET name=MARS />>, <AsterEphemerides rise_time=2021-06-09 23:43:00 culmination_time=2021-06-09 04:54:00 set_time=2021-06-09 10:01:00 aster=<Object type=PLANET name=JUPITER />>, <AsterEphemerides rise_time=2021-06-09 23:02:00 culmination_time=2021-06-09 03:41:00 set_time=2021-06-09 08:16:00 aster=<Object type=PLANET name=SATURN />>, <AsterEphemerides rise_time=2021-06-09 01:56:00 culmination_time=2021-06-09 09:18:00 set_time=2021-06-09 16:40:00 aster=<Object type=PLANET name=URANUS />>, <AsterEphemerides rise_time=2021-06-09 00:27:00 culmination_time=2021-06-09 06:13:00 set_time=2021-06-09 11:59:00 aster=<Object type=PLANET name=NEPTUNE />>, <AsterEphemerides rise_time=2021-06-09 22:22:00 culmination_time=2021-06-09 02:32:00 set_time=2021-06-09 06:38:00 aster=<Object type=PLANET name=PLUTO />>]

    Compute the ephemerides for June 9th, 2021:

    >>> get_ephemerides(pos, date(2021, 6, 9), timezone=2)
    [<AsterEphemerides rise_time=2021-06-09 05:36:00 culmination_time=2021-06-09 13:47:00 set_time=2021-06-09 21:58:00 aster=<Object type=STAR name=SUN />>, <AsterEphemerides rise_time=2021-06-09 04:59:00 culmination_time=2021-06-09 13:02:00 set_time=2021-06-09 21:16:00 aster=<Object type=SATELLITE name=MOON />>, <AsterEphemerides rise_time=2021-06-09 06:06:00 culmination_time=2021-06-09 13:58:00 set_time=2021-06-09 21:49:00 aster=<Object type=PLANET name=MERCURY />>, <AsterEphemerides rise_time=2021-06-09 06:52:00 culmination_time=2021-06-09 15:13:00 set_time=2021-06-09 23:34:00 aster=<Object type=PLANET name=VENUS />>, <AsterEphemerides rise_time=2021-06-09 08:38:00 culmination_time=2021-06-09 16:40:00 set_time=2021-06-09 00:44:00 aster=<Object type=PLANET name=MARS />>, <AsterEphemerides rise_time=2021-06-09 01:47:00 culmination_time=2021-06-09 06:54:00 set_time=2021-06-09 12:01:00 aster=<Object type=PLANET name=JUPITER />>, <AsterEphemerides rise_time=2021-06-09 01:06:00 culmination_time=2021-06-09 05:41:00 set_time=2021-06-09 10:16:00 aster=<Object type=PLANET name=SATURN />>, <AsterEphemerides rise_time=2021-06-09 03:56:00 culmination_time=2021-06-09 11:18:00 set_time=2021-06-09 18:40:00 aster=<Object type=PLANET name=URANUS />>, <AsterEphemerides rise_time=2021-06-09 02:27:00 culmination_time=2021-06-09 08:13:00 set_time=2021-06-09 13:59:00 aster=<Object type=PLANET name=NEPTUNE />>, <AsterEphemerides rise_time=2021-06-09 00:26:00 culmination_time=2021-06-09 04:32:00 set_time=2021-06-09 08:38:00 aster=<Object type=PLANET name=PLUTO />>]

    Objects may not rise or set on the given date (i.e. they rise the previous day or set the next day).
    When this happens, you will get `None` values on the rise or set time.
    Note that this is timezone-dependent:

    >>> get_ephemerides(Position(50.5876, 3.0624), date(2021, 9, 14), timezone=2)[1]
    <AsterEphemerides rise_time=2021-09-14 16:46:00 culmination_time=2021-09-14 20:29:00 set_time=None aster=<Object type=SATELLITE name=MOON />>

    If an objet does not rise nor set due to your latitude, then both rise and set will be `None`:

    >>> north_pole = Position(70, 20)
    >>> south_pole = Position(-70, 20)
    >>> get_ephemerides(north_pole, date(2021, 6, 20))
    [<AsterEphemerides rise_time=None culmination_time=2021-06-20 10:42:00 set_time=None aster=<Object type=STAR name=SUN />>, <AsterEphemerides rise_time=2021-06-20 14:30:00 culmination_time=2021-06-20 18:44:00 set_time=2021-06-20 22:53:00 aster=<Object type=SATELLITE name=MOON />>, <AsterEphemerides rise_time=2021-06-20 22:56:00 culmination_time=2021-06-20 09:47:00 set_time=2021-06-20 20:34:00 aster=<Object type=PLANET name=MERCURY />>, <AsterEphemerides rise_time=None culmination_time=2021-06-20 12:20:00 set_time=None aster=<Object type=PLANET name=VENUS />>, <AsterEphemerides rise_time=None culmination_time=2021-06-20 13:17:00 set_time=None aster=<Object type=PLANET name=MARS />>, <AsterEphemerides rise_time=2021-06-20 23:06:00 culmination_time=2021-06-20 03:04:00 set_time=2021-06-20 06:58:00 aster=<Object type=PLANET name=JUPITER />>, <AsterEphemerides rise_time=2021-06-20 23:28:00 culmination_time=2021-06-20 01:48:00 set_time=2021-06-20 04:05:00 aster=<Object type=PLANET name=SATURN />>, <AsterEphemerides rise_time=2021-06-20 21:53:00 culmination_time=2021-06-20 07:29:00 set_time=2021-06-20 17:02:00 aster=<Object type=PLANET name=URANUS />>, <AsterEphemerides rise_time=2021-06-20 22:51:00 culmination_time=2021-06-20 04:22:00 set_time=2021-06-20 09:50:00 aster=<Object type=PLANET name=NEPTUNE />>, <AsterEphemerides rise_time=None culmination_time=2021-06-20 00:40:00 set_time=None aster=<Object type=PLANET name=PLUTO />>]

    >>> get_ephemerides(north_pole, date(2021, 12, 21))
    [<AsterEphemerides rise_time=None culmination_time=2021-12-21 10:38:00 set_time=None aster=<Object type=STAR name=SUN />>, <AsterEphemerides rise_time=None culmination_time=2021-12-21 00:04:00 set_time=None aster=<Object type=SATELLITE name=MOON />>, <AsterEphemerides rise_time=None culmination_time=2021-12-21 11:33:00 set_time=None aster=<Object type=PLANET name=MERCURY />>, <AsterEphemerides rise_time=2021-12-21 11:58:00 culmination_time=2021-12-21 12:33:00 set_time=2021-12-21 13:08:00 aster=<Object type=PLANET name=VENUS />>, <AsterEphemerides rise_time=None culmination_time=2021-12-21 08:54:00 set_time=None aster=<Object type=PLANET name=MARS />>, <AsterEphemerides rise_time=2021-12-21 11:07:00 culmination_time=2021-12-21 14:43:00 set_time=2021-12-21 18:19:00 aster=<Object type=PLANET name=JUPITER />>, <AsterEphemerides rise_time=2021-12-21 11:32:00 culmination_time=2021-12-21 13:33:00 set_time=2021-12-21 15:33:00 aster=<Object type=PLANET name=SATURN />>, <AsterEphemerides rise_time=2021-12-21 09:54:00 culmination_time=2021-12-21 19:13:00 set_time=2021-12-21 04:37:00 aster=<Object type=PLANET name=URANUS />>, <AsterEphemerides rise_time=2021-12-21 10:49:00 culmination_time=2021-12-21 16:05:00 set_time=2021-12-21 21:21:00 aster=<Object type=PLANET name=NEPTUNE />>, <AsterEphemerides rise_time=None culmination_time=2021-12-21 12:31:00 set_time=None aster=<Object type=PLANET name=PLUTO />>]

    >>> get_ephemerides(south_pole, date(2021, 6, 20))
    [<AsterEphemerides rise_time=None culmination_time=2021-06-20 10:42:00 set_time=None aster=<Object type=STAR name=SUN />>, <AsterEphemerides rise_time=2021-06-20 11:10:00 culmination_time=2021-06-20 19:06:00 set_time=2021-06-20 01:20:00 aster=<Object type=SATELLITE name=MOON />>, <AsterEphemerides rise_time=2021-06-20 07:47:00 culmination_time=2021-06-20 09:47:00 set_time=2021-06-20 11:48:00 aster=<Object type=PLANET name=MERCURY />>, <AsterEphemerides rise_time=None culmination_time=2021-06-20 12:20:00 set_time=None aster=<Object type=PLANET name=VENUS />>, <AsterEphemerides rise_time=2021-06-20 12:14:00 culmination_time=2021-06-20 13:17:00 set_time=2021-06-20 14:21:00 aster=<Object type=PLANET name=MARS />>, <AsterEphemerides rise_time=2021-06-20 18:32:00 culmination_time=2021-06-20 03:04:00 set_time=2021-06-20 11:32:00 aster=<Object type=PLANET name=JUPITER />>, <AsterEphemerides rise_time=2021-06-20 15:20:00 culmination_time=2021-06-20 01:48:00 set_time=2021-06-20 12:12:00 aster=<Object type=PLANET name=SATURN />>, <AsterEphemerides rise_time=2021-06-20 04:32:00 culmination_time=2021-06-20 07:29:00 set_time=2021-06-20 10:26:00 aster=<Object type=PLANET name=URANUS />>, <AsterEphemerides rise_time=2021-06-20 21:28:00 culmination_time=2021-06-20 04:22:00 set_time=2021-06-20 11:13:00 aster=<Object type=PLANET name=NEPTUNE />>, <AsterEphemerides rise_time=None culmination_time=2021-06-20 00:40:00 set_time=None aster=<Object type=PLANET name=PLUTO />>]

    >>> get_ephemerides(south_pole, date(2021, 12, 22))
    [<AsterEphemerides rise_time=None culmination_time=2021-12-22 10:39:00 set_time=None aster=<Object type=STAR name=SUN />>, <AsterEphemerides rise_time=None culmination_time=2021-12-22 01:01:00 set_time=None aster=<Object type=SATELLITE name=MOON />>, <AsterEphemerides rise_time=None culmination_time=2021-12-22 11:35:00 set_time=None aster=<Object type=PLANET name=MERCURY />>, <AsterEphemerides rise_time=None culmination_time=2021-12-22 12:27:00 set_time=None aster=<Object type=PLANET name=VENUS />>, <AsterEphemerides rise_time=None culmination_time=2021-12-22 08:53:00 set_time=None aster=<Object type=PLANET name=MARS />>, <AsterEphemerides rise_time=2021-12-22 05:52:00 culmination_time=2021-12-22 14:40:00 set_time=2021-12-22 23:26:00 aster=<Object type=PLANET name=JUPITER />>, <AsterEphemerides rise_time=2021-12-22 02:41:00 culmination_time=2021-12-22 13:29:00 set_time=2021-12-22 00:21:00 aster=<Object type=PLANET name=SATURN />>, <AsterEphemerides rise_time=2021-12-22 16:01:00 culmination_time=2021-12-22 19:09:00 set_time=2021-12-22 22:17:00 aster=<Object type=PLANET name=URANUS />>, <AsterEphemerides rise_time=2021-12-22 08:59:00 culmination_time=2021-12-22 16:01:00 set_time=2021-12-22 23:04:00 aster=<Object type=PLANET name=NEPTUNE />>, <AsterEphemerides rise_time=None culmination_time=2021-12-22 12:27:00 set_time=None aster=<Object type=PLANET name=PLUTO />>]

    Note that the ephemerides can only be computed for a date range.
    Asking for the ephemerides with an out of range date will result in an exception:

    >>> get_ephemerides(pos, date(1000, 1, 1))
    Traceback (most recent call last):
        ...
    kosmorrolib.exceptions.OutOfRangeDateError: The date must be between 1899-07-29 and 2053-10-07
    """
    ephemerides = []

    def get_angle(for_aster: Object):
        def fun(time: Time) -> float:
            return (
                position.get_planet_topos()
                .at(time)
                .observe(for_aster.skyfield_object)
                .apparent()
                .altaz()[0]
                .degrees
            )

        fun.rough_period = 1.0
        return fun

    def is_risen(for_aster: Object):
        def fun(time: Time) -> bool:
            return get_angle(for_aster)(time) > RISEN_ANGLE

        fun.rough_period = 0.5
        return fun

    start_time = get_timescale().utc(
        for_date.year, for_date.month, for_date.day, -timezone
    )
    end_time = get_timescale().utc(
        for_date.year, for_date.month, for_date.day, 23 - timezone, 59, 59
    )

    try:
        for aster in ASTERS:
            rise_times, arr = find_discrete(start_time, end_time, is_risen(aster))

            culmination_time, _ = find_maxima(
                start_time,
                end_time,
                f=get_angle(aster),
                epsilon=1.0 / 3600 / 24,
                num=12,
            )

            if len(culmination_time) == 1:
                culmination_time = culmination_time[0]
            else:
                culmination_time = None

            rise_time, set_time = None, None

            if len(rise_times) == 2:
                rise_time = rise_times[0 if arr[0] else 1]
                set_time = rise_times[1 if not arr[1] else 0]
            elif len(rise_times) == 1:
                rise_time = rise_times[0] if arr[0] else None
                set_time = rise_times[0] if not arr[0] else None

            # Convert the Time instances to Python datetime objects
            if rise_time is not None:
                rise_time = normalize_datetime(
                    translate_to_timezone(
                        rise_time.utc_datetime().replace(microsecond=0), to_tz=timezone
                    )
                )

            if culmination_time is not None:
                culmination_time = normalize_datetime(
                    translate_to_timezone(
                        culmination_time.utc_datetime().replace(microsecond=0),
                        to_tz=timezone,
                    )
                )

            if set_time is not None:
                set_time = normalize_datetime(
                    translate_to_timezone(
                        set_time.utc_datetime().replace(microsecond=0), to_tz=timezone
                    )
                )

            ephemerides.append(
                AsterEphemerides(rise_time, culmination_time, set_time, aster=aster)
            )
    except EphemerisRangeError as error:
        start = translate_to_timezone(error.start_time.utc_datetime(), timezone)
        end = translate_to_timezone(error.end_time.utc_datetime(), timezone)

        start = date(start.year, start.month, start.day + 1)
        end = date(end.year, end.month, end.day - 1)

        raise OutOfRangeDateError(start, end) from error

    return ephemerides
