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

from core import alert_deprecation
from sys import version_info

python_version = (version_info.major, version_info.minor)
msg_python = (
    '\nOn Python 3.7, you can also use the "importlib-metadata" package.'
    if python_version == (3, 7)
    else ""
)

alert_deprecation(
    'Module "kosmorrolib.__version__" is deprecated since version 1.1. '
    "Use the importlib.metadata module provided by Python 3.8+: "
    "https://docs.python.org/3/library/importlib.metadata.html." + msg_python
)

__title__ = "kosmorrolib"
__description__ = "A library to compute your ephemerides"
__url__ = "http://kosmorro.space/lib"
__version__ = "1.0.4"
__author__ = "Jérôme Deuchnord"
__author_email__ = "jerome@deuchnord.fr"
__license__ = "AGPL-v3"
__copyright__ = "2021 - Jérôme Deuchnord"
