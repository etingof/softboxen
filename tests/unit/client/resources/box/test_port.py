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


class PortTestCase(unittest.TestCase):

    def setUp(self):
        super(PortTestCase, self).setUp()

        self.conn = mock.Mock()

        with open('tests/unit/client/resources/samples/port.json') as f:
            self.json_doc = json.load(f)

        self.conn.get.return_value.json.return_value = self.json_doc

        self.port = port.Port(self.conn, '/softboxen/v1/boxen/1/ports/1')

    def test__parse_attributes(self):
        self.port._parse_attributes(self.json_doc)

        self.assertEqual('port 1', self.port.name)
        self.assertEqual('Port 1', self.port.description)
        self.assertEqual('access', self.port.mode)
        self.assertEqual('10g', self.port.speed)
        self.assertEqual('/softboxen/v1/boxen/1/ports/1', self.port.path)
        self.assertEqual([], self.port.trunk_vlans.members_identities)
        self.assertIsInstance(self.port.access_vlan, vlan_port.VlanPort)
        self.assertIsInstance(self.port.trunk_native_vlan, vlan_port.VlanPort)

    def test_access_vlan(self):
        self.conn.get.return_value.json.reset_mock()

        with open('tests/unit/client/resources/samples/'
                  'vlan_port.json') as f:
            self.conn.get.return_value.json.return_value = json.load(f)

        expected = self.port.access_vlan

        self.assertIsInstance(
            expected, vlan_port.VlanPort)

        self.conn.get.return_value.json.assert_called_once_with()

    def test_trunk_vlans(self):
        self.conn.get.return_value.json.reset_mock()

        with open('tests/unit/client/resources/samples/'
                  'vlan_port_collection.json') as f:
            self.conn.get.return_value.json.return_value = json.load(f)

        expected = self.port.trunk_vlans

        self.assertIsInstance(
            expected, vlan_port.VlanPortCollection)

        self.conn.get.return_value.json.assert_called_once_with()

    def test_trunk_native_vlan(self):
        self.conn.get.return_value.json.reset_mock()

        with open('tests/unit/client/resources/samples/'
                  'vlan_port.json') as f:
            self.conn.get.return_value.json.return_value = json.load(f)

        expected = self.port.trunk_native_vlan

        self.assertIsInstance(
            expected, vlan_port.VlanPort)

        self.conn.get.return_value.json.assert_called_once_with()

    @mock.patch.object(vlan_port, 'VlanPort', autospec=True)
    def test_add_access_vlan(self, mock_vlan_port):
        self.port.add_access_vlan(field='value')
        mock_vlan_port.create.assert_called_once_with(
            self.conn, '/softboxen/v1/boxen/1/ports/1/access_vlan',
            field='value')

    @mock.patch.object(vlan_port, 'VlanPort', autospec=True)
    def test_add_trunk_vlan(self, mock_vlan_port):
        self.port.add_trunk_vlan(field='value')
        mock_vlan_port.create.assert_called_once_with(
            self.conn, '/softboxen/v1/boxen/1/ports/1/trunk_vlans',
            field='value')

    @mock.patch.object(vlan_port, 'VlanPort', autospec=True)
    def test_add_trunk_native_vlan(self, mock_vlan_port):
        self.port.add_trunk_native_vlan(field='value')
        mock_vlan_port.create.assert_called_once_with(
            self.conn, '/softboxen/v1/boxen/1/ports/1/trunk_native_vlan',
            field='value')


class PortCollectionTestCase(unittest.TestCase):

    def setUp(self):
        super(PortCollectionTestCase, self).setUp()

        self.conn = mock.Mock()

        with open('tests/unit/client/resources/samples/'
                  'port_collection.json') as f:
            self.json_doc = json.load(f)

        self.conn.get.return_value.json.return_value = self.json_doc

        self.port_col = port.PortCollection(
            self.conn, '/softboxen/v1/boxen/1/ports')

    def test__parse_attributes(self):
        self.port_col._parse_attributes(self.json_doc)

        self.assertEqual(
            ['/softboxen/v1/boxen/1/ports/1'],
            self.port_col.members_identities)

    @mock.patch.object(port, 'Port', autospec=True)
    def test_get_member(self, mock_port):
        self.port_col.get_member('/softboxen/v1/boxen/1/ports/1')

        mock_port.assert_called_once_with(
            self.port_col._conn, '/softboxen/v1/boxen/1/ports/1')

    @mock.patch.object(port, 'Port', autospec=True)
    def test_get_members(self, mock_port):
        members = list(self.port_col)

        mock_port.assert_called_once_with(
            self.port_col._conn, '/softboxen/v1/boxen/1/ports/1')

        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
