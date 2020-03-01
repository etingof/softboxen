#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import copy
import unittest
from http import client as http_client
from unittest import mock

from softboxen import exceptions
from softboxen.client.resources import base


class ResourceTestCase(unittest.TestCase):

    def setUp(self):
        super(ResourceTestCase, self).setUp()
        self.conn = mock.Mock()
        self.conn.get.return_value.json.return_value = {}
        self.base_resource = base.Resource(
            connection=self.conn, path='//softboxen')
        self.conn.reset_mock()

    def test_load(self):
        self.base_resource.load()
        self.conn.get.assert_called_once_with(path='//softboxen')

    def test_create_no_redir(self):
        base.Resource.create(
            connection=self.conn, path='//softboxen', field='value')
        self.conn.post.assert_called_once_with(
            path='//softboxen',
            allow_redirects=False,
            data={'field': 'value'})

    def test_create_redir(self):
        mock_rsp = self.conn.post.return_value
        mock_rsp.status_code = 302
        mock_rsp.geturl.return_value = '//softboxen/1'

        base.Resource.create(
            connection=self.conn, path='//softboxen', filed='value')

        self.conn.post.assert_called_once_with(
            path='//softboxen',
            allow_redirects=False,
            data={'filed': 'value'})

        self.conn.get.assert_called_once_with(path='//softboxen/1')

    def test_delete(self):
        self.base_resource.delete()
        self.conn.delete.assert_called_once_with(path='//softboxen')


class TestResource(base.Resource):

    def __init__(self, connection, identity):
        super(TestResource, self).__init__(
            connection, '/softboxen/%s' % identity)
        self.identity = identity

    def _parse_attributes(self, json_doc):
        pass


class TestResourceCollection(base.ResourceCollection):

    @property
    def _resource_type(self):
        return TestResource

    def __init__(self, connection):
        super(TestResourceCollection, self).__init__(
            connection, '/softboxen')


class ResourceCollectionBaseTestCase(unittest.TestCase):

    def setUp(self):
        super(ResourceCollectionBaseTestCase, self).setUp()
        self.conn = mock.MagicMock()
        self.test_resource_collection = TestResourceCollection(self.conn)
        self.conn.reset_mock()

    def test_get_member(self):
        self.test_resource_collection.members_identities = ('1',)
        result = self.test_resource_collection.get_member('1')
        self.assertIsInstance(result, TestResource)
        self.assertEqual('1', result.identity)

    def test_get_member_for_invalid_id(self):
        self.test_resource_collection.members_identities = ('1',)
        self.conn.get.side_effect = exceptions.ResourceNotFoundError(
            method='GET', url='http:///softboxen.com:8000/softboxen'
                              '/v1/softboxen/2',
            response=mock.MagicMock(status_code=http_client.NOT_FOUND))
        self.assertRaises(exceptions.ResourceNotFoundError,
                          self.test_resource_collection.get_member, '2')
        self.conn.get.assert_called_once_with(path='/softboxen/2')

    def test_get_members(self):
        self.test_resource_collection.members_identities = ('1', '2')
        result = list(self.test_resource_collection)
        self.assertIsInstance(result, list)
        for val in result:
            self.assertIsInstance(val, TestResource)
            self.assertTrue(val.identity in ('1', '2'))


class TestCollectionField(base.CollectionField):
    string = base.Field('String', required=True)
    integer = base.Field('Integer', converter=int)


MAPPING = {
    'raw': 'real',
    'raw1': 'real1',
    'raw2': 'real2'
}


class FullResource(base.Resource):

    string = base.Field('String', required=True)
    integer = base.Field('Integer', converter=int)
    collection_field = TestCollectionField('CollectionField')
    enumeration_field = base.EnumerationField(
        'Enumeration', MAPPING)


TEST_JSON = {
    'String': 'a string',
    'Integer': '42',
    'CollectionField': [
        {
            'String': 'box one',
            'Integer': 1
        },
        {
            'String': 'box two',
            'Integer': 2
        }
    ]
}


class FullResourceTestCase(unittest.TestCase):

    def setUp(self):
        super(FullResourceTestCase, self).setUp()
        self.conn = mock.Mock()
        self.json = copy.deepcopy(TEST_JSON)
        self.conn.get.return_value.json.return_value = self.json
        self.test_resource = FullResource(self.conn)

    def test_ok(self):
        self.assertEqual('a string', self.test_resource.string)
        self.assertEqual(42, self.test_resource.integer)
        self.assertEqual(
            'box one', self.test_resource.collection_field[0].string)
        self.assertEqual(2, self.test_resource.collection_field[1].integer)

    def test_missing_required(self):
        del self.json['String']
        self.assertRaisesRegex(
            exceptions.MissingAttributeError,
            'String', self.test_resource.load)

    def test_malformed_int(self):
        self.json['Integer'] = 'banana'
        self.assertRaisesRegex(
            exceptions.MalformedAttributeError,
            'attribute Integer is malformed.*invalid literal for int',
            self.test_resource.load)
