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

from enum import Enum


class MoonPhaseType(Enum):
    """An enumeration of moon phases."""

    NEW_MOON = 0
    WAXING_CRESCENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL_MOON = 4
    WANING_GIBBOUS = 5
    LAST_QUARTER = 6
    WANING_CRESCENT = 7


class SeasonType(Enum):
    MARCH_EQUINOX = 0
    JUNE_SOLSTICE = 1
    SEPTEMBER_EQUINOX = 2
    DECEMBER_SOLSTICE = 3


class EventType(Enum):
    """An enumeration for the supported event types."""

    OPPOSITION = 1
    CONJUNCTION = 2
    OCCULTATION = 3
    MAXIMAL_ELONGATION = 4
    PERIGEE = 5
    APOGEE = 6
    SEASON_CHANGE = 7
    LUNAR_ECLIPSE = 8


class LunarEclipseType(Enum):
    """An enumeration of lunar eclipse types"""

    PENUMBRAL = 0
    PARTIAL = 1
    TOTAL = 2


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
