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

from kosmorrolib import dateutil
from datetime import datetime


class DateUtilTestCase(unittest.TestCase):
    def test_translate_to_timezone(self):
        date = dateutil.translate_to_timezone(datetime(2020, 6, 9, 4), to_tz=-2)
        self.assertEqual(2, date.hour)

        date = dateutil.translate_to_timezone(datetime(2020, 6, 9, 0), to_tz=2)
        self.assertEqual(2, date.hour)

        date = dateutil.translate_to_timezone(
            datetime(2020, 6, 9, 8), to_tz=2, from_tz=6
        )
        self.assertEqual(4, date.hour)

        date = dateutil.translate_to_timezone(
            datetime(2020, 6, 9, 1), to_tz=0, from_tz=2
        )
        self.assertEqual(8, date.day)
        self.assertEqual(23, date.hour)


if __name__ == "__main__":
    unittest.main()
