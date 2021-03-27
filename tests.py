import doctest

from kosmorrolib import *

for module in [events, ephemerides]:
    doctest.testmod(module, verbose=True)
