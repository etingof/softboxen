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

from softboxen.client.resources.box import box
from softboxen.client.resources.box import credentials
from softboxen.client.resources.box import route


class BoxTestCase(unittest.TestCase):

    def setUp(self):
        super(BoxTestCase, self).setUp()

        self.conn = mock.Mock()

        with open('tests/unit/client/resources/samples/box.json') as f:
            self.json_doc = json.load(f)

        self.conn.get.return_value.json.return_value = self.json_doc

        self.box = box.Box(self.conn, '/softboxen/v1/boxen/1')

    def test__parse_attributes(self):
        self.box._parse_attributes(self.json_doc)

        self.assertEqual('Cisco 5300', self.box.description)
        self.assertEqual('rt-1', self.box.hostname)
        self.assertEqual('10.0.0.1', self.box.mgmt_address)
        self.assertEqual('1', self.box.version)
        self.assertEqual('5300', self.box.model)
        self.assertEqual('cisco', self.box.vendor)
        self.assertEqual('123e4567-e89b-12d3-a456-426655440000', self.box.uuid)
        self.assertEqual('/softboxen/v1/boxen/1', self.box.path)
        self.assertEqual([], self.box.credentials.members_identities)
        self.assertEqual([], self.box.routes.members_identities)

    def test_credentials(self):
        self.conn.get.return_value.json.reset_mock()

        with open('tests/unit/client/resources/samples/'
                  'credentials_collection.json') as f:
            self.conn.get.return_value.json.return_value = json.load(f)

        expected = self.box.credentials

        self.assertIsInstance(
            expected, credentials.CredentialsCollection)

        self.conn.get.return_value.json.assert_called_once_with()

    def test_routes(self):
        self.conn.get.return_value.json.reset_mock()

        with open('tests/unit/client/resources/samples/'
                  'route_collection.json') as f:
            self.conn.get.return_value.json.return_value = json.load(f)

        expected = self.box.routes

        self.assertIsInstance(
            expected, route.RouteCollection)

        self.conn.get.return_value.json.assert_called_once_with()


class BoxCollectionTestCase(unittest.TestCase):

    def setUp(self):
        super(BoxCollectionTestCase, self).setUp()

        self.conn = mock.Mock()

        with open('tests/unit/client/resources/samples/'
                  'box_collection.json') as f:
            self.json_doc = json.load(f)

        self.conn.get.return_value.json.return_value = self.json_doc

        self.box_col = box.BoxCollection(
            self.conn, '/softboxen/v1/boxen')

    def test__parse_attributes(self):
        self.box_col._parse_attributes(self.json_doc)

        self.assertEqual(
            ['/softboxen/v1/boxen/1'], self.box_col.members_identities)

    @mock.patch.object(box, 'Box', autospec=True)
    def test_get_member(self, mock_box):
        self.box_col.get_member('/softboxen/v1/boxen/1')

        mock_box.assert_called_once_with(
            self.box_col._conn, '/softboxen/v1/boxen/1')

    @mock.patch.object(box, 'Box', autospec=True)
    def test_get_members(self, mock_box):
        members = list(self.box_col)

        mock_box.assert_called_once_with(
            self.box_col._conn, '/softboxen/v1/boxen/1')

        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
