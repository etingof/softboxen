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

from softboxen.client.resources.box import route


class RouteTestCase(unittest.TestCase):

    def setUp(self):
        super(RouteTestCase, self).setUp()

        self.conn = mock.Mock()

        with open('tests/unit/client/resources/samples'
                  '/route.json') as f:
            self.json_doc = json.load(f)

        self.conn.get.return_value.json.return_value = self.json_doc

        self.route = route.Route(
            self.conn, '/softboxen/v1/boxen/1/routes/1')

    def test__parse_attributes(self):
        self.route._parse_attributes(self.json_doc)

        self.assertEqual('10.0.0.0/24', self.route.dst)
        self.assertEqual('10.0.0.1', self.route.gw)
        self.assertEqual(0, self.route.metric)
        self.assertEqual(
            '/softboxen/v1/boxen/1/routes/1', self.route.path)


class RouteCollectionTestCase(unittest.TestCase):

    def setUp(self):
        super(RouteCollectionTestCase, self).setUp()

        self.conn = mock.Mock()

        with open('tests/unit/client/resources/samples/'
                  'route_collection.json') as f:
            self.json_doc = json.load(f)

        self.conn.get.return_value.json.return_value = self.json_doc

        self.route_col = route.RouteCollection(
            self.conn, '/softboxen/v1/boxen/1/routes')

    def test__parse_attributes(self):
        self.route_col._parse_attributes(self.json_doc)

        self.assertEqual(
            ['/softboxen/v1/boxen/1/routes/1'],
            self.route_col.members_identities)

    @mock.patch.object(route, 'Route', autospec=True)
    def test_get_member(self, mock_route):
        self.route_col.get_member('/softboxen/v1/boxen/1/routes/1')

        mock_route.assert_called_once_with(
            self.route_col._conn, '/softboxen/v1/boxen/1/routes/1')

    @mock.patch.object(route, 'Route', autospec=True)
    def test_get_members(self, mock_route):
        members = list(self.route_col)

        mock_route.assert_called_once_with(
            self.route_col._conn, '/softboxen/v1/boxen/1/routes/1')

        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
