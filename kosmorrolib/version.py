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

"""
Kosmorrolib's versioning follows the `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_ standard,
meaning that:

* the versions always follow the X.Y.Z format, where X, Y and Z are natural numbers.
* the major version (X) never changes unless a change breaks compatibility (any breaking compatibility change in the
  same major version is considered as a bug)
* the minor version (Y) never changes unless new features are introduced
* the patch version (Z) never changes unless there are bug fixes
"""

MAJOR_VERSION = 0
"""The major version of the library"""

MINOR_VERSION = 9
"""The minor version of the library"""

PATCH_VERSION = 0
"""The patch version of the library"""

VERSION = '%d.%d.%d' % (MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)
"""
The library version in a readable for human beings format.
Useful for instance, if you want to display it to the end user.

If you need to check the version in your program, you should prefer using the MAJOR_VERSION, MINOR_MINOR_VERSION and
PATCH_VERSION constants instead.
"""
