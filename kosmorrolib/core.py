#!/usr/bin/env python3

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
