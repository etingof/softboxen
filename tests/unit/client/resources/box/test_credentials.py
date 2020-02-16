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

from softboxen.client.resources.box import credentials


class CredentialsTestCase(unittest.TestCase):

    def setUp(self):
        super(CredentialsTestCase, self).setUp()

        self.conn = mock.Mock()

        with open('tests/unit/client/resources/samples'
                  '/credentials.json') as f:
            self.json_doc = json.load(f)

        self.conn.get.return_value.json.return_value = self.json_doc

        self.creds = credentials.Credentials(
            self.conn, '/softboxen/v1/boxen/1/credentials/1')

    def test__parse_attributes(self):
        self.creds._parse_attributes(self.json_doc)

        self.assertEqual('password', self.creds.protocol)
        self.assertEqual('admin', self.creds.user)
        self.assertEqual('secret', self.creds.password)
        self.assertEqual(
            '/softboxen/v1/boxen/1/credentials/1', self.creds.path)


class CredentialsCollectionTestCase(unittest.TestCase):

    def setUp(self):
        super(CredentialsCollectionTestCase, self).setUp()

        self.conn = mock.Mock()

        with open('tests/unit/client/resources/samples/'
                  'credentials_collection.json') as f:
            self.json_doc = json.load(f)

        self.conn.get.return_value.json.return_value = self.json_doc

        self.creds_col = credentials.CredentialsCollection(
            self.conn, '/softboxen/v1/boxen/1/credentials')

    def test__parse_attributes(self):
        self.creds_col._parse_attributes(self.json_doc)

        self.assertEqual(
            ['/softboxen/v1/boxen/1/credentials/1'],
            self.creds_col.members_identities)

    @mock.patch.object(credentials, 'Credentials', autospec=True)
    def test_get_member(self, mock_credentials):
        self.creds_col.get_member('/softboxen/v1/boxen/1/credentials/1')

        mock_credentials.assert_called_once_with(
            self.creds_col._conn, '/softboxen/v1/boxen/1/credentials/1')

    @mock.patch.object(credentials, 'Credentials', autospec=True)
    def test_get_members(self, mock_credentials):
        members = list(self.creds_col)

        mock_credentials.assert_called_once_with(
            self.creds_col._conn, '/softboxen/v1/boxen/1/credentials/1')

        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
