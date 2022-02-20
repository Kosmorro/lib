#!/usr/bin/env python3

from doctest import testmod, NORMALIZE_WHITESPACE

from kosmorrolib import *


if __name__ == "__main__":
    failures = 0
    tests = 0

    for module in [events, ephemerides, model]:
        (f, t) = testmod(module, optionflags=NORMALIZE_WHITESPACE)
        failures += f
        tests += t

    if failures == 0:
        print("All %d tests successfully passed." % tests)
    else:
        exit(1)
