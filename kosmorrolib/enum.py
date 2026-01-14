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

    def localize(self, position: Position) -> LocalizedSeasonType:
        """Return the local season that corresponds to the given position's latitude.

        Args:
            season (SeasonType): The season to localize.
            position (Position): The position to localize the season for.

        Returns:
            SeasonType: The localized season.

        Raises:
            ValueError: If the latitude is 0 (equator).

        )

        >>> from kosmorrolib import Position
        >>> SeasonType.MARCH_EQUINOX.localize(Position(0, 1))
        Traceback (most recent call last):
            ...
        ValueError: Cannot localize seasons for this latitude.

        >>> SeasonType.MARCH_EQUINOX.localize(Position(1, 1))
        <LocalizedSeasonType.SPRING: 1>

        >>> SeasonType.MARCH_EQUINOX.localize(Position(-1, 1))
        <LocalizedSeasonType.AUTUMN: 3>
        """
        if position.latitude == 0:  # Equator
            raise ValueError("Cannot localize seasons for this latitude.")

        if position.latitude < 0:  # Southern hemisphere
            seasons = {
                self.MARCH_EQUINOX: LocalizedSeasonType.AUTUMN,
                self.JUNE_SOLSTICE: LocalizedSeasonType.WINTER,
                self.SEPTEMBER_EQUINOX: LocalizedSeasonType.SPRING,
                self.DECEMBER_SOLSTICE: LocalizedSeasonType.SUMMER,
            }

        else:  # Nothern hemisphere
            seasons = {
                self.MARCH_EQUINOX: LocalizedSeasonType.SPRING,
                self.JUNE_SOLSTICE: LocalizedSeasonType.SUMMER,
                self.SEPTEMBER_EQUINOX: LocalizedSeasonType.AUTUMN,
                self.DECEMBER_SOLSTICE: LocalizedSeasonType.WINTER,
            }

        return seasons[self]


class LocalizedSeasonType(Enum):
    WINTER = 0
    SPRING = 1
    SUMMER = 2
    AUTUMN = 3


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
