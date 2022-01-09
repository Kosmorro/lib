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

from abc import ABC, abstractmethod
from typing import Union
from datetime import datetime, timezone
from math import asin

from skyfield.api import Topos, Time, Angle
from skyfield.vectorlib import VectorSum as SkfPlanet

from .core import get_skf_objects, get_timescale
from .enum import MoonPhaseType, EventType, ObjectIdentifier, ObjectType


class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> dict:
        pass


class MoonPhase(Serializable):
    def __init__(
        self,
        phase_type: MoonPhaseType,
        time: datetime = None,
        next_phase_date: datetime = None,
    ):
        self.phase_type = phase_type
        self.time = time
        self.next_phase_date = next_phase_date

    def __repr__(self):
        return "<MoonPhase phase_type=%s time=%s next_phase_date=%s>" % (
            self.phase_type,
            self.time,
            self.next_phase_date,
        )

    def get_next_phase(self):
        """Helper to get the Moon phase that follows the one described by the object.

        If the current Moon phase is New Moon or Waxing crescent, the next one will be First Quarter:

        >>> moon_phase = MoonPhase(MoonPhaseType.NEW_MOON)
        >>> moon_phase.get_next_phase()
        <MoonPhaseType.FIRST_QUARTER: 2>

        >>> moon_phase = MoonPhase(MoonPhaseType.NEW_MOON)
        >>> moon_phase.get_next_phase()
        <MoonPhaseType.FIRST_QUARTER: 2>

        If the current Moon phase is First Quarter or Waxing gibbous, the next one will be Full Moon:

        >>> moon_phase = MoonPhase(MoonPhaseType.FIRST_QUARTER)
        >>> moon_phase.get_next_phase()
        <MoonPhaseType.FULL_MOON: 4>

        >>> moon_phase = MoonPhase(MoonPhaseType.WAXING_GIBBOUS)
        >>> moon_phase.get_next_phase()
        <MoonPhaseType.FULL_MOON: 4>

        If the current Moon phase is Full Moon or Waning gibbous, the next one will be Last Quarter:

        >>> moon_phase = MoonPhase(MoonPhaseType.FULL_MOON)
        >>> moon_phase.get_next_phase()
        <MoonPhaseType.LAST_QUARTER: 6>

        >>> moon_phase = MoonPhase(MoonPhaseType.WANING_GIBBOUS)
        >>> moon_phase.get_next_phase()
        <MoonPhaseType.LAST_QUARTER: 6>

        If the current Moon phase is Last Quarter Moon or Waning crescent, the next one will be New Moon:

        >>> moon_phase = MoonPhase(MoonPhaseType.LAST_QUARTER)
        >>> moon_phase.get_next_phase()
        <MoonPhaseType.NEW_MOON: 0>

        >>> moon_phase = MoonPhase(MoonPhaseType.WANING_CRESCENT)
        >>> moon_phase.get_next_phase()
        <MoonPhaseType.NEW_MOON: 0>
        """
        if self.phase_type in [MoonPhaseType.NEW_MOON, MoonPhaseType.WAXING_CRESCENT]:
            return MoonPhaseType.FIRST_QUARTER
        if self.phase_type in [
            MoonPhaseType.FIRST_QUARTER,
            MoonPhaseType.WAXING_GIBBOUS,
        ]:
            return MoonPhaseType.FULL_MOON
        if self.phase_type in [MoonPhaseType.FULL_MOON, MoonPhaseType.WANING_GIBBOUS]:
            return MoonPhaseType.LAST_QUARTER

        return MoonPhaseType.NEW_MOON

    def serialize(self) -> dict:
        return {
            "phase": self.phase_type.name,
            "time": self.time.isoformat() if self.time is not None else None,
            "next": {
                "phase": self.get_next_phase().name,
                "time": self.next_phase_date.isoformat(),
            },
        }


class Object(Serializable):
    """
    An astronomical object.
    """

    def __init__(
        self,
        identifier: ObjectIdentifier,
        skyfield_object: SkfPlanet,
        radius: float = None,
    ):
        """
        Initialize an astronomical object

        :param ObjectIdentifier identifier: the official name of the object (may be internationalized)
        :param str skyfield_object: the object from Skyfield library
        :param float radius: the radius (in km) of the object
        """
        self.identifier = identifier
        self.skyfield_object = skyfield_object
        self.radius = radius

    def __repr__(self):
        return "<Object type=%s name=%s />" % (
            self.get_type().name,
            self.identifier.name,
        )

    @abstractmethod
    def get_type(self) -> ObjectType:
        pass

    def get_apparent_radius(self, for_date: Union[Time, datetime]) -> Angle:
        """Calculate the apparent radius, in degrees, of the object from the given place at a given time.

        **Warning:** this is an internal function, not intended for use by end-developers.

        For an easier usage, this method accepts datetime and Skyfield's Time objects:

        >>> sun = ASTERS[0]
        >>> sun.get_apparent_radius(datetime(2021, 6, 9, tzinfo=timezone.utc))
        <Angle 00deg 31' 31.6">

        >>> sun.get_apparent_radius(get_timescale().utc(2021, 6, 9))
        <Angle 00deg 31' 31.6">

        Source of the algorithm: https://rhodesmill.org/skyfield/examples.html#what-is-the-angular-diameter-of-a-planet-given-its-radius

        :param for_date: the date for which the apparent radius has to be returned
        :return: an object representing a Skyfield angle
        """
        if isinstance(for_date, datetime):
            for_date = get_timescale().from_datetime(for_date)

        ra, dec, distance = (
            EARTH.skyfield_object.at(for_date)
            .observe(self.skyfield_object)
            .apparent()
            .radec()
        )

        return Angle(radians=asin(self.radius / distance.km) * 2.0)

    def serialize(self) -> dict:
        """Serialize the given object

        >>> planet = Planet(ObjectIdentifier.MARS, "MARS")
        >>> planet.serialize()
        {'identifier': 'MARS', 'type': 'PLANET', 'radius': None}
        """
        return {
            "identifier": self.identifier.name,
            "type": self.get_type().name,
            "radius": self.radius,
        }


class Star(Object):
    def get_type(self) -> ObjectType:
        return ObjectType.STAR


class Planet(Object):
    def get_type(self) -> ObjectType:
        return ObjectType.PLANET


class DwarfPlanet(Planet):
    def get_type(self) -> ObjectType:
        return ObjectType.DWARF_PLANET


class Satellite(Object):
    def get_type(self) -> ObjectType:
        return ObjectType.SATELLITE


class Event(Serializable):
    def __init__(
        self,
        event_type: EventType,
        objects: [Object],
        start_time: datetime,
        end_time: Union[datetime, None] = None,
        details: {str: any} = None,
    ):
        self.event_type = event_type
        self.objects = objects
        self.start_time = start_time
        self.end_time = end_time
        self.details = details

    def __repr__(self):
        return "<Event type=%s objects=%s start=%s end=%s details=%s />" % (
            self.event_type.name,
            self.objects,
            self.start_time,
            self.end_time,
            self.details,
        )

    def get_description(self, show_details: bool = True) -> str:
        description = self.event_type.value % self._get_objects_name()
        if show_details and self.details is not None:
            description += " ({:s})".format(self.details)
        return description

    def _get_objects_name(self):
        if len(self.objects) == 1:
            return self.objects[0].name

        return tuple(object.name for object in self.objects)

    def serialize(self) -> dict:
        return {
            "objects": [object.serialize() for object in self.objects],
            "EventType": self.event_type.name,
            "starts_at": self.start_time.isoformat(),
            "ends_at": self.end_time.isoformat() if self.end_time is not None else None,
            "details": self.details,
        }


class AsterEphemerides(Serializable):
    def __init__(
        self,
        rise_time: Union[datetime, None],
        culmination_time: Union[datetime, None],
        set_time: Union[datetime, None],
        aster: Object,
    ):
        self.rise_time = rise_time
        self.culmination_time = culmination_time
        self.set_time = set_time
        self.object = aster

    def __repr__(self):
        return (
            "<AsterEphemerides rise_time=%s culmination_time=%s set_time=%s aster=%s>"
            % (self.rise_time, self.culmination_time, self.set_time, self.object)
        )

    def serialize(self) -> dict:
        return {
            "object": self.object.serialize(),
            "rise_time": self.rise_time.isoformat()
            if self.rise_time is not None
            else None,
            "culmination_time": self.culmination_time.isoformat()
            if self.culmination_time is not None
            else None,
            "set_time": self.set_time.isoformat()
            if self.set_time is not None
            else None,
        }


EARTH = Planet(ObjectIdentifier.EARTH, get_skf_objects()["EARTH"])

ASTERS = [
    Star(ObjectIdentifier.SUN, get_skf_objects()["SUN"], radius=696342),
    Satellite(ObjectIdentifier.MOON, get_skf_objects()["MOON"], radius=1737.4),
    Planet(ObjectIdentifier.MERCURY, get_skf_objects()["MERCURY"], radius=2439.7),
    Planet(ObjectIdentifier.VENUS, get_skf_objects()["VENUS"], radius=6051.8),
    Planet(ObjectIdentifier.MARS, get_skf_objects()["MARS"], radius=3396.2),
    Planet(
        ObjectIdentifier.JUPITER, get_skf_objects()["JUPITER BARYCENTER"], radius=71492
    ),
    Planet(
        ObjectIdentifier.SATURN, get_skf_objects()["SATURN BARYCENTER"], radius=60268
    ),
    Planet(
        ObjectIdentifier.URANUS, get_skf_objects()["URANUS BARYCENTER"], radius=25559
    ),
    Planet(
        ObjectIdentifier.NEPTUNE, get_skf_objects()["NEPTUNE BARYCENTER"], radius=24764
    ),
    Planet(ObjectIdentifier.PLUTO, get_skf_objects()["PLUTO BARYCENTER"], radius=1185),
]


def get_aster(identifier: ObjectIdentifier) -> Object:
    """Return the aster with the given identifier

    >>> get_aster(ObjectIdentifier.SATURN)
    <Object type=PLANET name=SATURN />

    You can also use it to get the `EARTH` object, even though it has its own constant:
    <Object type=PLANET name=EARTH />
    """
    if identifier == ObjectIdentifier.EARTH:
        return EARTH

    for aster in ASTERS:
        if aster.identifier == identifier:
            return aster


class Position:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude
        self._topos = None

    def get_planet_topos(self) -> Topos:
        if self._topos is None:
            self._topos = EARTH.skyfield_object + Topos(
                latitude_degrees=self.latitude, longitude_degrees=self.longitude
            )

        return self._topos
