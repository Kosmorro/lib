#!/usr/bin/env python3

from datetime import date

from skyfield.errors import EphemerisRangeError
from skyfield.timelib import Time
from skyfield.searchlib import find_discrete, find_maxima, find_minima
from numpy import pi

from .model import Event, Star, Planet, ASTERS
from .dateutil import translate_to_timezone
from .enum import EventType, ObjectIdentifier
from .exceptions import OutOfRangeDateError
from .core import get_timescale, get_skf_objects, flatten_list


def _search_conjunction(start_time: Time, end_time: Time, timezone: int) -> [Event]:
    earth = get_skf_objects()["earth"]
    aster1 = None
    aster2 = None

    def is_in_conjunction(time: Time):
        earth_pos = earth.at(time)
        _, aster1_lon, _ = (
            earth_pos.observe(aster1.get_skyfield_object()).apparent().ecliptic_latlon()
        )
        _, aster2_lon, _ = (
            earth_pos.observe(aster2.get_skyfield_object()).apparent().ecliptic_latlon()
        )

        return ((aster1_lon.radians - aster2_lon.radians) / pi % 2.0).astype(
            "int8"
        ) == 0

    is_in_conjunction.rough_period = 60.0

    computed = []
    conjunctions = []

    for aster1 in ASTERS:
        # Ignore the Sun
        if isinstance(aster1, Star):
            continue

        for aster2 in ASTERS:
            if isinstance(aster2, Star) or aster2 == aster1 or aster2 in computed:
                continue

            times, is_conjs = find_discrete(start_time, end_time, is_in_conjunction)

            for i, time in enumerate(times):
                if is_conjs[i]:
                    aster1_pos = (aster1.get_skyfield_object() - earth).at(time)
                    aster2_pos = (aster2.get_skyfield_object() - earth).at(time)
                    distance = aster1_pos.separation_from(aster2_pos).degrees

                    if distance - aster2.get_apparent_radius(
                        time, earth
                    ) < aster1.get_apparent_radius(time, earth):
                        occulting_aster = (
                            [aster1, aster2]
                            if aster1_pos.distance().km < aster2_pos.distance().km
                            else [aster2, aster1]
                        )

                        conjunctions.append(
                            Event(
                                EventType.OCCULTATION,
                                occulting_aster,
                                translate_to_timezone(time.utc_datetime(), timezone),
                            )
                        )
                    else:
                        conjunctions.append(
                            Event(
                                EventType.CONJUNCTION,
                                [aster1, aster2],
                                translate_to_timezone(time.utc_datetime(), timezone),
                            )
                        )

        computed.append(aster1)

    return conjunctions


def _search_oppositions(start_time: Time, end_time: Time, timezone: int) -> [Event]:
    """Function to search oppositions.

    **Warning:** this is an internal function, not intended for use by end-developers.

    Will return Mars opposition on 2020-10-13:

    >>> oppositions = _search_oppositions(get_timescale().utc(2020, 10, 13), get_timescale().utc(2020, 10, 14), 0)
    >>> len(oppositions)
    1
    >>> oppositions[0].objects[0]
    <Object type=PLANET name=MARS />

    Will return nothing if no opposition happens:

    >>> _search_oppositions(get_timescale().utc(2021, 3, 20), get_timescale().utc(2021, 3, 21), 0)
    []
    """
    earth = get_skf_objects()["earth"]
    sun = get_skf_objects()["sun"]
    aster = None

    def is_oppositing(time: Time) -> [bool]:
        diff = get_angle(time)
        return diff > 180

    def get_angle(time: Time):
        earth_pos = earth.at(time)

        sun_pos = earth_pos.observe(
            sun
        ).apparent()  # Never do this without eyes protection!
        aster_pos = earth_pos.observe(get_skf_objects()[aster.skyfield_name]).apparent()

        _, lon1, _ = sun_pos.ecliptic_latlon()
        _, lon2, _ = aster_pos.ecliptic_latlon()

        return lon1.degrees - lon2.degrees

    is_oppositing.rough_period = 1.0
    events = []

    for aster in ASTERS:
        if not isinstance(aster, Planet) or aster.identifier in [
            ObjectIdentifier.MERCURY,
            ObjectIdentifier.VENUS,
        ]:
            continue

        times, _ = find_discrete(start_time, end_time, is_oppositing)
        for time in times:
            if get_angle(time) < 0:
                # If the angle is negative, then it is actually a false positive.
                # Just ignoring it.
                continue

            events.append(
                Event(
                    EventType.OPPOSITION,
                    [aster],
                    translate_to_timezone(time.utc_datetime(), timezone),
                )
            )

    return events


def _search_maximal_elongations(
    start_time: Time, end_time: Time, timezone: int
) -> [Event]:
    earth = get_skf_objects()["earth"]
    sun = get_skf_objects()["sun"]
    aster = None

    def get_elongation(time: Time):
        sun_pos = (sun - earth).at(time)
        aster_pos = (aster.get_skyfield_object() - earth).at(time)
        separation = sun_pos.separation_from(aster_pos)
        return separation.degrees

    get_elongation.rough_period = 1.0

    events = []

    for aster in ASTERS:
        if aster.skyfield_name not in ["MERCURY", "VENUS"]:
            continue

        times, elongations = find_maxima(
            start_time, end_time, f=get_elongation, epsilon=1.0 / 24 / 3600, num=12
        )

        for i, time in enumerate(times):
            elongation = elongations[i]
            events.append(
                Event(
                    EventType.MAXIMAL_ELONGATION,
                    [aster],
                    translate_to_timezone(time.utc_datetime(), timezone),
                    details="{:.3n}°".format(elongation),
                )
            )

    return events


def _get_moon_distance():
    earth = get_skf_objects()["earth"]
    moon = get_skf_objects()["moon"]

    def get_distance(time: Time):
        earth_pos = earth.at(time)
        moon_pos = earth_pos.observe(moon).apparent()

        return moon_pos.distance().au

    get_distance.rough_period = 1.0

    return get_distance


def _search_moon_apogee(start_time: Time, end_time: Time, timezone: int) -> [Event]:
    moon = ASTERS[1]
    events = []

    times, _ = find_maxima(
        start_time, end_time, f=_get_moon_distance(), epsilon=1.0 / 24 / 60
    )

    for time in times:
        events.append(
            Event(
                EventType.MOON_APOGEE,
                [moon],
                translate_to_timezone(time.utc_datetime(), timezone),
            )
        )

    return events


def _search_moon_perigee(start_time: Time, end_time: Time, timezone: int) -> [Event]:
    moon = ASTERS[1]
    events = []

    times, _ = find_minima(
        start_time, end_time, f=_get_moon_distance(), epsilon=1.0 / 24 / 60
    )

    for time in times:
        events.append(
            Event(
                EventType.MOON_PERIGEE,
                [moon],
                translate_to_timezone(time.utc_datetime(), timezone),
            )
        )

    return events


def get_events(for_date: date = date.today(), timezone: int = 0) -> [Event]:
    """Calculate and return a list of events for the given date, adjusted to the given timezone if any.

    Find events that happen on April 4th, 2020 (show hours in UTC):

    >>> get_events(date(2020, 4, 4))
    [<Event type=CONJUNCTION objects=[<Object type=PLANET name=MERCURY />, <Object type=PLANET name=NEPTUNE />] start=2020-04-04 01:14:39.063308+00:00 end=None details=None />]

    Find events that happen on April 4th, 2020 (show timezones in UTC+2):

    >>> get_events(date(2020, 4, 4), 2)
    [<Event type=CONJUNCTION objects=[<Object type=PLANET name=MERCURY />, <Object type=PLANET name=NEPTUNE />] start=2020-04-04 03:14:39.063267+02:00 end=None details=None />]

    Find events that happen on April 3rd, 2020 (show timezones in UTC-2):

    >>> get_events(date(2020, 4, 3), -2)
    [<Event type=CONJUNCTION objects=[<Object type=PLANET name=MERCURY />, <Object type=PLANET name=NEPTUNE />] start=2020-04-03 23:14:39.063388-02:00 end=None details=None />]

    If there is no events for the given date, then an empty list is returned:

    >>> get_events(date(2021, 3, 20))
    []

    :param for_date: the date for which the events must be calculated
    :param timezone: the timezone to adapt the results to. If not given, defaults to 0.
    :return: a list of events found for the given date.
    """

    start_time = get_timescale().utc(
        for_date.year, for_date.month, for_date.day, -timezone
    )
    end_time = get_timescale().utc(
        for_date.year, for_date.month, for_date.day + 1, -timezone
    )

    try:
        found_events = []

        for fun in [
            _search_oppositions,
            _search_conjunction,
            _search_maximal_elongations,
            _search_moon_apogee,
            _search_moon_perigee,
        ]:
            found_events.append(fun(start_time, end_time, timezone))

        return sorted(flatten_list(found_events), key=lambda event: event.start_time)
    except EphemerisRangeError as error:
        start_date = translate_to_timezone(error.start_time.utc_datetime(), timezone)
        end_date = translate_to_timezone(error.end_time.utc_datetime(), timezone)

        start_date = date(start_date.year, start_date.month, start_date.day)
        end_date = date(end_date.year, end_date.month, end_date.day)

        raise OutOfRangeDateError(start_date, end_date) from error
