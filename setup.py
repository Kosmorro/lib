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

import pathlib
from setuptools import setup, find_packages

from kosmorrolib.__version__ import __version__

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="kosmorrolib",
    version=__version__,
    author="Jérôme Deuchnord",
    author_email="jerome@deuchnord.fr",
    url="http://kosmorro.space/lib",
    license="AGPL-v3",
    description="A library to computes the ephemerides.",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["kosmorro", "astronomy", "ephemerides", "ephemeris"],
    packages=["kosmorrolib"],
    install_requires=[
        "skyfield>=1.21.0,<2.0.0",
        "skyfield-data>=3.0.0,<4.0.0",
        "numpy>=1.17.0,<2.0.0",
        "python-dateutil",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    python_requires=">=3.7",
)
