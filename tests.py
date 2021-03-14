import doctest

from kosmorrolib import *

for module in [events]:
    doctest.testmod(module, verbose=True)
