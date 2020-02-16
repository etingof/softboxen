#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import unittest

suite = unittest.TestLoader().loadTestsFromNames(
    ['tests.unit.client.resources.box.test_box.suite',
     'tests.unit.client.resources.box.test_credentials.suite',
     'tests.unit.client.resources.box.test_port.suite',
     'tests.unit.client.resources.box.test_route.suite',
     'tests.unit.client.resources.box.test_vlan.suite',
     'tests.unit.client.resources.box.test_vlan_port.suite']
)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
