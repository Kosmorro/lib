#!/usr/bin/env python3

from enum import Enum, auto


class MoonPhaseType(Enum):
    """An enumeration of moon phases."""

    NEW_MOON = 1
    WAXING_CRESCENT = 2
    FIRST_QUARTER = 3
    WAXING_GIBBOUS = 4
    FULL_MOON = 5
    WANING_GIBBOUS = 6
    LAST_QUARTER = 7
    WANING_CRESCENT = 8


class EventType(Enum):
    """An enumeration for the supported event types."""

    OPPOSITION = 1
    CONJUNCTION = 2
    OCCULTATION = 3
    MAXIMAL_ELONGATION = 4
    MOON_PERIGEE = 5
    MOON_APOGEE = 6


class ObjectType(Enum):
    """An enumeration of object types"""

    STAR = 0
    PLANET = 1
    DWARF_PLANET = 11
    SATELLITE = 2


class ObjectIdentifier(Enum):
    """An enumeration of identifiers for objects"""

    SUN = 0
    EARTH = 1
    MOON = 11
    MERCURY = 2
    VENUS = 3
    MARS = 4
    JUPITER = 5
    SATURN = 6
    URANUS = 7
    NEPTUNE = 8
    PLUTO = 9
