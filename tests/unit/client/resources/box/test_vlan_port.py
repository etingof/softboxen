#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import json
import sys
import unittest
from unittest import mock

from softboxen.client.resources.box import port
from softboxen.client.resources.box import vlan_port


class VlanPortTestCase(unittest.TestCase):

    def setUp(self):
        super(VlanPortTestCase, self).setUp()

        self.conn = mock.Mock()

        with open('tests/unit/client/resources/samples/vlan_port.json') as f:
            self.json_doc = json.load(f)

        self.conn.get.return_value.json.return_value = self.json_doc

        self.vlan_port = vlan_port.VlanPort(
            self.conn, '/softboxen/v1/boxen/1/ports/1/vlans/1')

    def test__parse_attributes(self):
        self.vlan_port._parse_attributes(self.json_doc)

        self.assertEqual('VLAN port', self.vlan_port.name)
        self.assertEqual('VLAN #1 access port', self.vlan_port.description)
        self.assertEqual('/softboxen/v1/boxen/1/ports/1/vlans/1',
                         self.vlan_port.path)
        self.assertIsInstance(self.vlan_port.port, port.Port)

    def test_port(self):
        self.conn.get.return_value.json.reset_mock()

        with open('tests/unit/client/resources/samples/'
                  'port.json') as f:
            self.conn.get.return_value.json.return_value = json.load(f)

        expected = self.vlan_port.port

        self.assertIsInstance(expected, port.Port)

        self.conn.get.return_value.json.assert_called_once_with()


class VlanPortCollectionTestCase(unittest.TestCase):

    def setUp(self):
        super(VlanPortCollectionTestCase, self).setUp()

        self.conn = mock.Mock()

        with open('tests/unit/client/resources/samples/'
                  'vlan_port_collection.json') as f:
            self.json_doc = json.load(f)

        self.conn.get.return_value.json.return_value = self.json_doc

        self.port_col = vlan_port.VlanPortCollection(
            self.conn, '/softboxen/v1/boxen/1/ports/1/vlans')

    def test__parse_attributes(self):
        self.port_col._parse_attributes(self.json_doc)

        self.assertEqual(
            ['/softboxen/v1/boxen/1/ports/1/vlans/1'],
            self.port_col.members_identities)

    @mock.patch.object(vlan_port, 'VlanPort', autospec=True)
    def test_get_member(self, mock_port):
        self.port_col.get_member('/softboxen/v1/boxen/1/ports/1/vlans/1')

        mock_port.assert_called_once_with(
            self.port_col._conn, '/softboxen/v1/boxen/1/ports/1/vlans/1')

    @mock.patch.object(vlan_port, 'VlanPort', autospec=True)
    def test_get_members(self, mock_port):
        members = list(self.port_col)

        mock_port.assert_called_once_with(
            self.port_col._conn, '/softboxen/v1/boxen/1/ports/1/vlans/1')

        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
