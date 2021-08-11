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

import functools
from unittest import mock


def expect_assertions(assert_fun, num=1):
    """Asserts that an assertion function is called as expected.

    This is very useful when the assertions are in loops.
    To use it, create a nested function in the the tests function.
    The nested function will receive as parameter the mocked assertion function to use in place of the original one.
    Finally, run the nested function.

    Example of use:

    >>> # the function we tests:
    >>> def my_sum_function(n, m):
    >>>     # some code here
    >>>     pass

    >>> # The unit tests:
    >>> def test_sum(self):
    >>>     @expect_assertions(self.assertEqual, num=10):
    >>>     def make_assertions(assert_equal):
    >>>         for i in range (-5, 5):
    >>>             for j in range(-5, 5):
    >>>                 assert_equal(i + j, my_sum_function(i, j)
    >>>
    >>>     make_assertions()  # You don't need to give any parameter, the decorator does it for you.

    :param assert_fun: the assertion function to tests
    :param num: the number of times the assertion function is expected to be called
    """
    assert_fun_mock = mock.Mock(side_effect=assert_fun)

    def fun_decorator(fun):
        @functools.wraps(fun)
        def sniff_function():
            fun(assert_fun_mock)

            count = assert_fun_mock.call_count
            if count != num:
                raise AssertionError(
                    "Expected %d call(s) to function %s but called %d time(s)."
                    % (num, assert_fun.__name__, count)
                )

        return sniff_function

    return fun_decorator
