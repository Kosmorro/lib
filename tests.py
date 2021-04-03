#!/usr/bin/env python3

import doctest

from kosmorrolib import *


if __name__ == "__main__":
    failures = 0
    tests = 0

    for module in [events, ephemerides]:
        (f, t) = doctest.testmod(module)
        failures += f
        tests += t

    if failures == 0:
        print("✔ All %d tests successfully passed." % tests)
    else:
        exit(1)
