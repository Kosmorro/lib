#!/usr/bin/env python3

#    Kosmorro - Compute The Next Ephemerides
#    Copyright (C) 2019  Jérôme Deuchnord <jerome@deuchnord.fr>
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
