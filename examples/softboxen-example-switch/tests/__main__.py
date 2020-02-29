#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#
import unittest

suite = unittest.TestLoader().loadTestsFromNames(
    ['tests.unit.__main__.suite']
)


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    exit(not result.wasSuccessful())
