# Kosmorrolib - a library to compute your ephemerides!
[![Coverage Status](https://coveralls.io/repos/github/Kosmorro/lib/badge.svg?branch=main)](https://coveralls.io/github/Kosmorro/lib?branch=main) [![Version on PyPI](https://img.shields.io/pypi/v/kosmorrolib)](https://pypi.org/project/kosmorrolib) [![Discord](https://img.shields.io/discord/650237632533757965?logo=discord&label=%23kosmorro)](https://discord.gg/nyemBqE)

## Installation

### Requirements

Kosmorrolib requires the following software to work:

- Python ≥ 3.7.0
- PIP

### Production environment

Keep in mind that Kosmorrolib is not considered as stable for now.

#### PyPI

Kosmorrolib is available [on PyPI](https://pypi.org/project/kosmorrolib/): `pip install kosmorrolib`.

### Development environment

First, install [Pipenv](https://pypi.org/project/pipenv/).

Clone this repository and run `pipenv sync` to install all the dependencies.
And that's all, your development environment is ready for the fight! 👏

## Using the Kosmorrolib

The Kosmorrolib provides three functions that you can use in your code:

```python
#!/usr/bin/env python3

import kosmorrolib
from datetime import date

position = kosmorrolib.Position(50.5824, 3.0624)

# Get the moon phase for today
moon_phase = kosmorrolib.get_moon_phase()

# Get the moon phase for June 9th, 2021
moon_phase = kosmorrolib.get_moon_phase(date.fromisoformat('2021-06-09'))

# Get a list of objects representing the ephemerides of today.
ephemerides = kosmorrolib.get_ephemerides(position)

# Get a list of objects representing the ephemerides of June 9th, 2021.
ephemerides = kosmorrolib.get_ephemerides(position, date.fromisoformat('2021-06-09'))

# Get a list of objects representing the events of today.
events = kosmorrolib.get_events()

# Get a list of objects representing the events on June 9th, 2021.
events = kosmorrolib.get_events(date.fromisoformat('2021-06-09'))

# Note that each method provides an optional parameter for the timezone:
moon_phase = kosmorrolib.get_moon_phase(timezone=2)
ephemerides = kosmorrolib.get_ephemerides(position, timezone=2)
events = kosmorrolib.get_events(timezone=2)
```
