#!/usr/bin/env python3

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
    url="http://kosmorro.space",
    license="CECILL-C",
    description="A library to computes the ephemerides.",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["kosmorro", "astronomy", "ephemerides", "ephemeris"],
    packages=["kosmorrolib"],
    install_requires=[
        "skyfield>=1.21.0,<2.0.0",
        "numpy>=1.17.0,<2.0.0",
        "python-dateutil",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: CeCILL-C Free Software License Agreement (CECILL-C)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    python_requires=">=3.7",
)
