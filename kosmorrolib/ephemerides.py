#!/usr/bin/env python3

import datetime
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

    phases = list(MoonPhaseType)
    current_phase = None
    current_phase_time = None
    next_phase_time = None
    i = 0

    if len(times) == 0:
        return None

    for i, time in enumerate(times):
        if now.utc_iso() <= time.utc_iso():
            if vals[i] in [0, 2, 4, 6]:
                if time.utc_datetime() < tomorrow.utc_datetime():
                    current_phase_time = time
                    current_phase = phases[vals[i]]
                else:
                    i -= 1
                    current_phase_time = None
                    current_phase = phases[vals[i]]
            else:
                current_phase = phases[vals[i]]

            break

    for j in range(i + 1, len(times)):
        if vals[j] in [0, 2, 4, 6]:
            next_phase_time = times[j]
            break

    return MoonPhase(
        current_phase,
        translate_to_timezone(current_phase_time.utc_datetime(), timezone)
        if current_phase_time is not None
        else None,
        translate_to_timezone(next_phase_time.utc_datetime(), timezone)
        if next_phase_time is not None
        else None,
    )


def get_moon_phase(
    for_date: datetime.date = datetime.date.today(), timezone: int = 0
) -> MoonPhase:
    """Calculate and return the moon phase for the given date, adjusted to the given timezone if any.

    Get the moon phase for the 27 March, 2021:

    >>> get_moon_phase(datetime.date.fromisoformat("2021-03-27"))
    <MoonPhase phase_type=MoonPhaseType.WAXING_GIBBOUS time=None next_phase_date=2021-03-28 18:48:10.902298+00:00>

    Get the moon phase for the 27 March, 2021, in the UTC+2 timezone:

    >>> get_moon_phase(datetime.date.fromisoformat("2021-03-27"), timezone=2)
    <MoonPhase phase_type=MoonPhaseType.WAXING_GIBBOUS time=None next_phase_date=2021-03-28 20:48:10.902298+02:00>
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
    time1 = get_timescale().utc(for_date.year, for_date.month, for_date.day - 10)
    time2 = get_timescale().utc(for_date.year, for_date.month, for_date.day + 10)

    try:
        times, phase = find_discrete(time1, time2, moon_phase_at)
    except EphemerisRangeError as error:
        start = translate_to_timezone(error.start_time.utc_datetime(), timezone)
        end = translate_to_timezone(error.end_time.utc_datetime(), timezone)

        start = datetime.date(start.year, start.month, start.day) + datetime.timedelta(
            days=12
        )
        end = datetime.date(end.year, end.month, end.day) - datetime.timedelta(days=12)

        raise OutOfRangeDateError(start, end) from error

    return _get_skyfield_to_moon_phase(times, phase, today, timezone)


def get_ephemerides(
    position: Position, date: datetime.date = datetime.date.today(), timezone: int = 0
) -> [AsterEphemerides]:
    """Compute and return the ephemerides for the given position and date, adjusted to the given timezone if any.

    Compute the ephemerides for June 9th, 2021:

    >>> pos = Position(50.5824, 3.0624)
    >>> get_ephemerides(pos, datetime.date(2021, 6, 9))
    [<AsterEphemerides rise_time=2021-06-09 03:36:00 culmination_time=2021-06-09 11:47:00 set_time=2021-06-09 19:58:00 aster=<Object type=STAR name=SUN />>, <AsterEphemerides rise_time=2021-06-09 02:59:00 culmination_time=2021-06-09 11:02:00 set_time=2021-06-09 19:16:00 aster=<Object type=SATELLITE name=MOON />>, <AsterEphemerides rise_time=2021-06-09 04:06:00 culmination_time=2021-06-09 11:58:00 set_time=2021-06-09 19:49:00 aster=<Object type=PLANET name=MERCURY />>, <AsterEphemerides rise_time=2021-06-09 04:52:00 culmination_time=2021-06-09 13:13:00 set_time=2021-06-09 21:34:00 aster=<Object type=PLANET name=VENUS />>, <AsterEphemerides rise_time=2021-06-09 06:38:00 culmination_time=2021-06-09 14:40:00 set_time=2021-06-09 22:41:00 aster=<Object type=PLANET name=MARS />>, <AsterEphemerides rise_time=2021-06-09 23:43:00 culmination_time=2021-06-09 04:54:00 set_time=2021-06-09 10:01:00 aster=<Object type=PLANET name=JUPITER />>, <AsterEphemerides rise_time=2021-06-09 23:02:00 culmination_time=2021-06-09 03:41:00 set_time=2021-06-09 08:16:00 aster=<Object type=PLANET name=SATURN />>, <AsterEphemerides rise_time=2021-06-09 01:56:00 culmination_time=2021-06-09 09:18:00 set_time=2021-06-09 16:40:00 aster=<Object type=PLANET name=URANUS />>, <AsterEphemerides rise_time=2021-06-09 00:27:00 culmination_time=2021-06-09 06:13:00 set_time=2021-06-09 11:59:00 aster=<Object type=PLANET name=NEPTUNE />>, <AsterEphemerides rise_time=2021-06-09 22:22:00 culmination_time=2021-06-09 02:32:00 set_time=2021-06-09 06:38:00 aster=<Object type=PLANET name=PLUTO />>]

    Compute the ephemerides for June 9th, 2021:

    >>> get_ephemerides(pos, datetime.date(2021, 6, 9), timezone=2)
    [<AsterEphemerides rise_time=2021-06-09 05:36:00 culmination_time=2021-06-09 13:47:00 set_time=2021-06-09 21:58:00 aster=<Object type=STAR name=SUN />>, <AsterEphemerides rise_time=2021-06-09 04:59:00 culmination_time=2021-06-09 13:02:00 set_time=2021-06-09 21:16:00 aster=<Object type=SATELLITE name=MOON />>, <AsterEphemerides rise_time=2021-06-09 06:06:00 culmination_time=2021-06-09 13:58:00 set_time=2021-06-09 21:49:00 aster=<Object type=PLANET name=MERCURY />>, <AsterEphemerides rise_time=2021-06-09 06:52:00 culmination_time=2021-06-09 15:13:00 set_time=2021-06-09 23:34:00 aster=<Object type=PLANET name=VENUS />>, <AsterEphemerides rise_time=2021-06-09 08:38:00 culmination_time=2021-06-09 16:40:00 set_time=2021-06-09 00:44:00 aster=<Object type=PLANET name=MARS />>, <AsterEphemerides rise_time=2021-06-09 01:47:00 culmination_time=2021-06-09 06:54:00 set_time=2021-06-09 12:01:00 aster=<Object type=PLANET name=JUPITER />>, <AsterEphemerides rise_time=2021-06-09 01:06:00 culmination_time=2021-06-09 05:41:00 set_time=2021-06-09 10:16:00 aster=<Object type=PLANET name=SATURN />>, <AsterEphemerides rise_time=2021-06-09 03:56:00 culmination_time=2021-06-09 11:18:00 set_time=2021-06-09 18:40:00 aster=<Object type=PLANET name=URANUS />>, <AsterEphemerides rise_time=2021-06-09 02:27:00 culmination_time=2021-06-09 08:13:00 set_time=2021-06-09 13:59:00 aster=<Object type=PLANET name=NEPTUNE />>, <AsterEphemerides rise_time=2021-06-09 00:26:00 culmination_time=2021-06-09 04:32:00 set_time=2021-06-09 08:38:00 aster=<Object type=PLANET name=PLUTO />>]
    """
    ephemerides = []

    def get_angle(for_aster: Object):
        def fun(time: Time) -> float:
            return (
                position.get_planet_topos()
                .at(time)
                .observe(for_aster.get_skyfield_object())
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

    start_time = get_timescale().utc(date.year, date.month, date.day, -timezone)
    end_time = get_timescale().utc(
        date.year, date.month, date.day, 23 - timezone, 59, 59
    )

    try:
        for aster in ASTERS:
            rise_times, arr = find_discrete(start_time, end_time, is_risen(aster))
            try:
                culmination_time, _ = find_maxima(
                    start_time,
                    end_time,
                    f=get_angle(aster),
                    epsilon=1.0 / 3600 / 24,
                    num=12,
                )
                culmination_time = (
                    culmination_time[0] if len(culmination_time) > 0 else None
                )
            except ValueError:
                culmination_time = None

            if len(rise_times) == 2:
                rise_time = rise_times[0 if arr[0] else 1]
                set_time = rise_times[1 if not arr[1] else 0]
            else:
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

        start = datetime.date(start.year, start.month, start.day + 1)
        end = datetime.date(end.year, end.month, end.day - 1)

        raise OutOfRangeDateError(start, end) from error

    return ephemerides
