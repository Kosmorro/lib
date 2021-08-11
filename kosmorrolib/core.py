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

from skyfield.api import Loader
from skyfield.timelib import Time
from skyfield.nutationlib import iau2000b

from skyfield_data import get_skyfield_data_path

LOADER = Loader(get_skyfield_data_path())


def get_timescale():
    return LOADER.timescale()


def get_skf_objects():
    return LOADER("de421.bsp")


def get_iau2000b(time: Time):
    return iau2000b(time.tt)


def flatten_list(the_list: list):
    new_list = []
    for item in the_list:
        if isinstance(item, list):
            for item2 in flatten_list(item):
                new_list.append(item2)
            continue

        new_list.append(item)

    return new_list
