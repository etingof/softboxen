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

from softboxen.client.resources.box import vlan


class VlanTestCase(unittest.TestCase):

    def setUp(self):
        super(VlanTestCase, self).setUp()

        self.conn = mock.Mock()

        with open('tests/unit/client/resources/samples'
                  '/vlan.json') as f:
            self.json_doc = json.load(f)

        self.conn.get.return_value.json.return_value = self.json_doc

        self.vlan = vlan.Vlan(
            self.conn, '/softboxen/v1/vlans/1')

    def test__parse_attributes(self):
        self.vlan._parse_attributes(self.json_doc)

        self.assertEqual(1, self.vlan.number)
        self.assertEqual('segment 1', self.vlan.name)
        self.assertEqual('VLAN 1', self.vlan.description)
        self.assertEqual(
            '/softboxen/v1/vlans/1', self.vlan.path)


class VlanCollectionTestCase(unittest.TestCase):

    def setUp(self):
        super(VlanCollectionTestCase, self).setUp()

        self.conn = mock.Mock()

        with open('tests/unit/client/resources/samples/'
                  'vlan_collection.json') as f:
            self.json_doc = json.load(f)

        self.conn.get.return_value.json.return_value = self.json_doc

        self.vlan_col = vlan.VlanCollection(
            self.conn, '/softboxen/v1/vlans')

    def test__parse_attributes(self):
        self.vlan_col._parse_attributes(self.json_doc)

        self.assertEqual(
            ['/softboxen/v1/vlans/1'],
            self.vlan_col.members_identities)

    @mock.patch.object(vlan, 'Vlan', autospec=True)
    def test_get_member(self, mock_vlan):
        self.vlan_col.get_member('/softboxen/v1/vlans/1')

        mock_vlan.assert_called_once_with(
            self.vlan_col._conn, '/softboxen/v1/vlans/1')

    @mock.patch.object(vlan, 'Vlan', autospec=True)
    def test_get_members(self, mock_vlan):
        members = list(self.vlan_col)

        mock_vlan.assert_called_once_with(
            self.vlan_col._conn, '/softboxen/v1/vlans/1')

        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
