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

from datetime import date, timedelta

from skyfield.errors import EphemerisRangeError
from skyfield.timelib import Time
from skyfield.searchlib import find_discrete, find_maxima, find_minima
from skyfield.units import Angle
from skyfield import almanac, eclipselib
from math import pi

from kosmorrolib.model import (
    Event,
    Object,
    Star,
    Planet,
    get_aster,
    ASTERS,
    EARTH,
)
from kosmorrolib.dateutil import translate_to_timezone
from kosmorrolib.enum import EventType, ObjectIdentifier, SeasonType, LunarEclipseType
from kosmorrolib.exceptions import OutOfRangeDateError
from kosmorrolib.core import get_timescale, get_skf_objects, flatten_list


def _search_conjunctions_occultations(
    start_time: Time, end_time: Time, timezone: int
) -> [Event]:
    """Function to search conjunction.

    **Warning:** this is an internal function, not intended for use by end-developers.

    Will return MOON and VENUS opposition on 2021-06-12:

    >>> conjunction = _search_conjunctions_occultations(get_timescale().utc(2021, 6, 12), get_timescale().utc(2021, 6, 13), 0)
    >>> len(conjunction)
    1
    >>> conjunction[0].objects
    [<Object type=SATELLITE name=MOON />, <Object type=PLANET name=VENUS />]

    Will return nothing if no conjunction happens:

    >>> _search_conjunctions_occultations(get_timescale().utc(2021, 6, 17),get_timescale().utc(2021, 6, 18), 0)
    []

    This function detects occultations too:

    >>> _search_conjunctions_occultations(get_timescale().utc(2021, 4, 17),get_timescale().utc(2021, 4, 18), 0)
    [<Event type=OCCULTATION objects=[<Object type=SATELLITE name=MOON />, <Object type=PLANET name=MARS />] start=2021-04-17 12:08:16.115650+00:00 end=None details=None />]
    """
    earth = get_skf_objects()["earth"]
    aster1 = None
    aster2 = None

    def is_in_conjunction(time: Time):
        earth_pos = earth.at(time)
        _, aster1_lon, _ = (
            earth_pos.observe(aster1.skyfield_object).apparent().ecliptic_latlon()
        )
        _, aster2_lon, _ = (
            earth_pos.observe(aster2.skyfield_object).apparent().ecliptic_latlon()
        )

        return ((aster1_lon.radians - aster2_lon.radians) / pi % 2.0).astype(
            "int8"
        ) == 0

    is_in_conjunction.rough_period = 60.0

    computed = []
    events = []

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
                    aster1_pos = (aster1.skyfield_object - earth).at(time)
                    aster2_pos = (aster2.skyfield_object - earth).at(time)
                    distance = aster1_pos.separation_from(aster2_pos).degrees

                    if (
                        distance - aster2.get_apparent_radius(time).degrees
                        < aster1.get_apparent_radius(time).degrees
                    ):
                        occulting_aster = (
                            [aster1, aster2]
                            if aster1_pos.distance().km < aster2_pos.distance().km
                            else [aster2, aster1]
                        )

                        events.append(
                            Event(
                                EventType.OCCULTATION,
                                occulting_aster,
                                translate_to_timezone(time.utc_datetime(), timezone),
                            )
                        )
                    else:
                        events.append(
                            Event(
                                EventType.CONJUNCTION,
                                [aster1, aster2],
                                translate_to_timezone(time.utc_datetime(), timezone),
                            )
                        )

        computed.append(aster1)

    return events


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

    >>> _search_oppositions(get_timescale().utc(2022, 12, 24), get_timescale().utc(2022, 12, 25), 0)
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
        aster_pos = earth_pos.observe(aster.skyfield_object).apparent()

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
            if int(get_angle(time)) != 180:
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
    """Function to search oppositions.

    **Warning:** this is an internal function, not intended for use by end-developers.

    Will return Mercury maimum elogation for September 14, 2021:

    >>> get_events(date(2021, 9, 14))
    [<Event type=MAXIMAL_ELONGATION objects=[<Object type=PLANET name=MERCURY />] start=2021-09-14 04:13:46.664879+00:00 end=None details={'deg': 26.8} />]
    """
    earth = get_skf_objects()["earth"]
    sun = get_skf_objects()["sun"]

    def get_elongation(planet: Object):
        def f(time: Time):
            sun_pos = (sun - earth).at(time)
            aster_pos = (planet.skyfield_object - earth).at(time)
            separation = sun_pos.separation_from(aster_pos)
            return separation.degrees

        f.rough_period = 1.0

        return f

    events = []

    for identifier in [ObjectIdentifier.MERCURY, ObjectIdentifier.VENUS]:
        planet = get_aster(identifier)
        times, elongations = find_maxima(
            start_time,
            end_time,
            f=get_elongation(planet),
            epsilon=1.0 / 24 / 3600,
            num=12,
        )

        for i, time in enumerate(times):
            elongation = round(elongations[i], 1)
            events.append(
                Event(
                    EventType.MAXIMAL_ELONGATION,
                    [planet],
                    translate_to_timezone(time.utc_datetime(), timezone),
                    details={"deg": elongation},
                )
            )

    return events


def _get_distance(to_aster: Object, from_aster: Object):
    def get_distance(time: Time):
        from_pos = from_aster.skyfield_object.at(time)
        to_pos = from_pos.observe(to_aster.skyfield_object)

        return to_pos.distance().km

    get_distance.rough_period = 1.0

    return get_distance


def _search_apogee(to_aster: Object, from_aster: Object = EARTH) -> callable:
    """Search for moon apogee

    **Warning:** this is an internal function, not intended for use by end-developers.

    Get the moon apogee:
    >>> _search_apogee(ASTERS[1])(get_timescale().utc(2021, 6, 8), get_timescale().utc(2021, 6, 9), 0)
    [<Event type=APOGEE objects=[<Object type=SATELLITE name=MOON />] start=2021-06-08 02:39:40.165271+00:00 end=None details={'distance_km': 406211.04850197025} />]

    Get the Earth's apogee:
    >>> _search_apogee(EARTH, from_aster=ASTERS[0])(get_timescale().utc(2021, 7, 5), get_timescale().utc(2021, 7, 6), 0)
    [<Event type=APOGEE objects=[<Object type=PLANET name=EARTH />] start=2021-07-05 22:35:42.148792+00:00 end=None details={'distance_km': 152100521.91712126} />]
    """

    def f(start_time: Time, end_time: Time, timezone: int) -> [Event]:
        events = []

        times, distances = find_maxima(
            start_time,
            end_time,
            f=_get_distance(to_aster, from_aster),
            epsilon=1.0 / 24 / 60,
        )

        for i, time in enumerate(times):
            events.append(
                Event(
                    EventType.APOGEE,
                    [to_aster],
                    translate_to_timezone(time.utc_datetime(), timezone),
                    details={"distance_km": distances[i]},
                )
            )

        return events

    return f


def _search_perigee(aster: Object, from_aster: Object = EARTH) -> callable:
    """Search for moon perigee

    **Warning:** this is an internal function, not intended for use by end-developers.

    Get the moon perigee:
    >>> _search_perigee(ASTERS[1])(get_timescale().utc(2021, 5, 26), get_timescale().utc(2021, 5, 27), 0)
    [<Event type=PERIGEE objects=[<Object type=SATELLITE name=MOON />] start=2021-05-26 01:56:01.983455+00:00 end=None details={'distance_km': 357313.9680798693} />]

    Get the Earth's perigee:
    >>> _search_perigee(EARTH, from_aster=ASTERS[0])(get_timescale().utc(2021, 1, 2), get_timescale().utc(2021, 1, 3), 0)
    [<Event type=PERIGEE objects=[<Object type=PLANET name=EARTH />] start=2021-01-02 13:59:00.495905+00:00 end=None details={'distance_km': 147093166.1686309} />]
    """

    def f(start_time: Time, end_time: Time, timezone: int) -> [Event]:
        events = []

        times, distances = find_minima(
            start_time,
            end_time,
            f=_get_distance(aster, from_aster),
            epsilon=1.0 / 24 / 60,
        )

        for i, time in enumerate(times):
            events.append(
                Event(
                    EventType.PERIGEE,
                    [aster],
                    translate_to_timezone(time.utc_datetime(), timezone),
                    details={"distance_km": distances[i]},
                )
            )

        return events

    return f


def _search_earth_season_change(
    start_time: Time, end_time: Time, timezone: int
) -> [Event]:
    """Function to find earth season change event.

    **Warning:** this is an internal function, not intended for use by end-developers.

    Will return JUNE SOLSTICE on 2020/06/20:

    >>> season_change = _search_earth_season_change(get_timescale().utc(2020, 6, 20), get_timescale().utc(2020, 6, 21), 0)
    >>> len(season_change)
    1
    >>> season_change[0].event_type
    <EventType.SEASON_CHANGE: 7>
    >>> season_change[0].details
    {'season': <SeasonType.JUNE_SOLSTICE: 1>}

    Will return nothing if there is no season change event in the period of time being calculated:

    >>> _search_earth_season_change(get_timescale().utc(2021, 6, 17), get_timescale().utc(2021, 6, 18), 0)
    []
    """
    events = []
    event_time, event_id = almanac.find_discrete(
        start_time, end_time, almanac.seasons(get_skf_objects())
    )
    if len(event_time) == 0:
        return []
    events.append(
        Event(
            EventType.SEASON_CHANGE,
            [],
            translate_to_timezone(event_time.utc_datetime()[0], timezone),
            details={"season": SeasonType(event_id[0])},
        )
    )
    return events


def _search_lunar_eclipse(start_time: Time, end_time: Time, timezone: int) -> [Event]:
    """Function to detect lunar eclipses.

    **Warning:** this is an internal function, not intended for use by end-developers.

    Will return a total lunar eclipse for 2021-05-26:

    >>> _search_lunar_eclipse(get_timescale().utc(2021, 5, 26), get_timescale().utc(2021, 5, 27), 0)
    [<Event type=LUNAR_ECLIPSE objects=[<Object type=SATELLITE name=MOON />] start=2021-05-26 08:47:54.795821+00:00 end=2021-05-26 13:49:34.353411+00:00 details={'type': <LunarEclipseType.TOTAL: 2>, 'maximum': datetime.datetime(2021, 5, 26, 11, 18, 42, 328842, tzinfo=datetime.timezone.utc)} />]

    >>> _search_lunar_eclipse(get_timescale().utc(2019, 7, 16), get_timescale().utc(2019, 7, 17), 0)
    [<Event type=LUNAR_ECLIPSE objects=[<Object type=SATELLITE name=MOON />] start=2019-07-16 18:39:53.391337+00:00 end=2019-07-17 00:21:51.378940+00:00 details={'type': <LunarEclipseType.PARTIAL: 1>, 'maximum': datetime.datetime(2019, 7, 16, 21, 30, 44, 170096, tzinfo=datetime.timezone.utc)} />]

    >>> _search_lunar_eclipse(get_timescale().utc(2017, 2, 11), get_timescale().utc(2017, 2, 12), 0)
    [<Event type=LUNAR_ECLIPSE objects=[<Object type=SATELLITE name=MOON />] start=2017-02-10 22:02:59.016572+00:00 end=2017-02-11 03:25:07.627886+00:00 details={'type': <LunarEclipseType.PENUMBRAL: 0>, 'maximum': datetime.datetime(2017, 2, 11, 0, 43, 51, 793786, tzinfo=datetime.timezone.utc)} />]
    """
    moon = get_aster(ObjectIdentifier.MOON)
    events = []
    t, y, details = eclipselib.lunar_eclipses(start_time, end_time, get_skf_objects())

    for ti, yi in zip(t, y):
        penumbra_radius = Angle(radians=details["penumbra_radius_radians"][0])
        _, max_lon, _ = (
            EARTH.skyfield_object.at(ti)
            .observe(moon.skyfield_object)
            .apparent()
            .ecliptic_latlon()
        )

        def is_in_penumbra(time: Time):
            _, lon, _ = (
                EARTH.skyfield_object.at(time)
                .observe(moon.skyfield_object)
                .apparent()
                .ecliptic_latlon()
            )

            moon_radius = details["moon_radius_radians"]

            return (
                abs(max_lon.radians - lon.radians)
                < penumbra_radius.radians + moon_radius
            )

        is_in_penumbra.rough_period = 60.0

        search_start_time = get_timescale().from_datetime(
            start_time.utc_datetime() - timedelta(days=1)
        )
        search_end_time = get_timescale().from_datetime(
            end_time.utc_datetime() + timedelta(days=1)
        )

        eclipse_start, _ = find_discrete(search_start_time, ti, is_in_penumbra)
        eclipse_end, _ = find_discrete(ti, search_end_time, is_in_penumbra)

        events.append(
            Event(
                EventType.LUNAR_ECLIPSE,
                [moon],
                start_time=translate_to_timezone(
                    eclipse_start[0].utc_datetime(), timezone
                ),
                end_time=translate_to_timezone(eclipse_end[0].utc_datetime(), timezone),
                details={
                    "type": LunarEclipseType(yi),
                    "maximum": translate_to_timezone(ti.utc_datetime(), timezone),
                },
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

    >>> get_events(date(2021, 4, 20))
    []

    Note that the events can only be found for a date range.
    Asking for the events with an out of range date will result in an exception:

    >>> get_events(date(1000, 1, 1))
    Traceback (most recent call last):
        ...
    kosmorrolib.exceptions.OutOfRangeDateError: The date must be between 1899-07-28 and 2053-10-08

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
            _search_conjunctions_occultations,
            _search_maximal_elongations,
            _search_apogee(ASTERS[1]),
            _search_perigee(ASTERS[1]),
            _search_apogee(EARTH, from_aster=ASTERS[0]),
            _search_perigee(EARTH, from_aster=ASTERS[0]),
            _search_earth_season_change,
            _search_lunar_eclipse,
        ]:
            found_events.append(fun(start_time, end_time, timezone))

        return sorted(flatten_list(found_events), key=lambda event: event.start_time)
    except EphemerisRangeError as error:
        start_date = translate_to_timezone(error.start_time.utc_datetime(), timezone)
        end_date = translate_to_timezone(error.end_time.utc_datetime(), timezone)

        start_date = date(start_date.year, start_date.month, start_date.day)
        end_date = date(end_date.year, end_date.month, end_date.day)

        raise OutOfRangeDateError(start_date, end_date) from error
