#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Union
from datetime import datetime

from numpy import pi, arcsin

from skyfield.api import Topos, Time
from skyfield.vectorlib import VectorSum as SkfPlanet

from .core import get_skf_objects
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
        self, identifier: ObjectIdentifier, skyfield_name: str, radius: float = None
    ):
        """
        Initialize an astronomical object

        :param ObjectIdentifier identifier: the official name of the object (may be internationalized)
        :param str skyfield_name: the internal name of the object in Skyfield library
        :param float radius: the radius (in km) of the object
        :param AsterEphemerides ephemerides: the ephemerides associated to the object
        """
        self.identifier = identifier
        self.skyfield_name = skyfield_name
        self.radius = radius

    def __repr__(self):
        return "<Object type=%s name=%s />" % (
            self.get_type().name,
            self.identifier.name,
        )

    def get_skyfield_object(self) -> SkfPlanet:
        return get_skf_objects()[self.skyfield_name]

    @abstractmethod
    def get_type(self) -> ObjectType:
        pass

    def get_apparent_radius(self, time: Time, from_place) -> float:
        """
        Calculate the apparent radius, in degrees, of the object from the given place at a given time.
        :param time:
        :param from_place:
        :return:
        """
        if self.radius is None:
            raise ValueError("Missing radius for %s" % self.identifier.name)

        return (
            360
            / pi
            * arcsin(
                self.radius
                / from_place.at(time).observe(self.get_skyfield_object()).distance().km
            )
        )

    def serialize(self) -> dict:
        return {
            "identifier": self.identifier.name,
            "type": self.get_type(),
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
        details: str = None,
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


EARTH = Planet(ObjectIdentifier.EARTH, "EARTH")

ASTERS = [
    Star(ObjectIdentifier.SUN, "SUN", radius=696342),
    Satellite(ObjectIdentifier.MOON, "MOON", radius=1737.4),
    Planet(ObjectIdentifier.MERCURY, "MERCURY", radius=2439.7),
    Planet(ObjectIdentifier.VENUS, "VENUS", radius=6051.8),
    Planet(ObjectIdentifier.MARS, "MARS", radius=3396.2),
    Planet(ObjectIdentifier.JUPITER, "JUPITER BARYCENTER", radius=71492),
    Planet(ObjectIdentifier.SATURN, "SATURN BARYCENTER", radius=60268),
    Planet(ObjectIdentifier.URANUS, "URANUS BARYCENTER", radius=25559),
    Planet(ObjectIdentifier.NEPTUNE, "NEPTUNE BARYCENTER", radius=24764),
    Planet(ObjectIdentifier.PLUTO, "PLUTO BARYCENTER", radius=1185),
]


class Position:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude
        self._topos = None

    def get_planet_topos(self) -> Topos:
        if self._topos is None:
            self._topos = EARTH.get_skyfield_object() + Topos(
                latitude_degrees=self.latitude, longitude_degrees=self.longitude
            )

        return self._topos
