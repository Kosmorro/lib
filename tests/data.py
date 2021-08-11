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

import unittest

from kosmorrolib import model, core
from kosmorrolib.enum import ObjectIdentifier


class DataTestCase(unittest.TestCase):
    def test_object_radius_must_be_set_to_get_apparent_radius(self):
        o = model.Planet(ObjectIdentifier.SATURN, "SATURN")

        with self.assertRaises(ValueError) as context:
            o.get_apparent_radius(
                core.get_timescale().now(), core.get_skf_objects()["earth"]
            )

        self.assertEqual(("Missing radius for SATURN",), context.exception.args)


if __name__ == "__main__":
    unittest.main()
