#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import json
import unittest
from http import client as http_client
from unittest import mock

import requests

from softboxen import exceptions
from softboxen.client import rest_client


class RestClientMethodsTestCase(unittest.TestCase):

    def setUp(self):
        super(RestClientMethodsTestCase, self).setUp()
        self.conn = rest_client.RestClient(
            'http://softboxen.com:1234', username='foo', password='secret',
            verify=True)
        self.data = {
            'box': 'data'
        }
        self.headers = {
            'X-Box': 'header'
        }

    @mock.patch.object(rest_client.RestClient, '_http_call', autospec=True)
    def test_get(self, mock__http_call):
        self.conn.get(
            path='box/path', data=self.data.copy(),
            headers=self.headers.copy())

        mock__http_call.assert_called_once_with(
            mock.ANY, 'GET', 'box/path',
            data=self.data, headers=self.headers, timeout=60)

    @mock.patch.object(rest_client.RestClient, '_http_call', autospec=True)
    def test_post(self, mock__http_call):
        self.conn.post(path='box/path', data=self.data.copy(),
                       headers=self.headers.copy())

        mock__http_call.assert_called_once_with(
            mock.ANY, 'POST', 'box/path', data=self.data,
            headers=self.headers, timeout=60)

    @mock.patch.object(rest_client.RestClient, '_http_call', autospec=True)
    def test_patch(self, mock__http_call):
        self.conn.patch(
            path='box/path', data=self.data.copy(),
            headers=self.headers.copy())

        mock__http_call.assert_called_once_with(
            mock.ANY, 'PATCH', 'box/path', data=self.data,
            headers=self.headers, timeout=60)

    @mock.patch.object(rest_client.RestClient, '_http_call', autospec=True)
    def test_put(self, mock__http_call):
        self.conn.put(
            path='box/path', data=self.data.copy(),
            headers=self.headers.copy())

        mock__http_call.assert_called_once_with(
            mock.ANY, 'PUT', 'box/path', data=self.data,
            headers=self.headers, timeout=60)

    @mock.patch.object(rest_client.RestClient, '_http_call', autospec=True)
    def test_delete(self, mock__http_call):
        self.conn.delete(
            path='box/path', data=self.data.copy(),
            headers=self.headers.copy())

        mock__http_call.assert_called_once_with(
            mock.ANY, 'DELETE', 'box/path', data=self.data,
            headers=self.headers, timeout=60)

    def test_set_http_basic_auth(self):
        self.assertEqual(('foo', 'secret'), self.conn._session.auth)

    def test_close(self):
        session = mock.Mock(spec=requests.Session)
        self.conn._session = session
        self.conn.close()
        session.close.assert_called_once_with()


class LowLevelRestClientTestCase(unittest.TestCase):

    def setUp(self):
        super(LowLevelRestClientTestCase, self).setUp()
        self.conn = rest_client.RestClient(
            'http://softboxen.com:1234', verify=True)
        self.data = {'box': 'data'}
        self.headers = {'X-Box': 'header'}
        self.session = mock.Mock(spec=requests.Session)
        self.conn._session = self.session
        self.request = self.session.request
        self.request.return_value.status_code = http_client.OK

    def test_ok_get(self):
        self.conn._http_call(
            'GET', path='box/path', headers=self.headers)

        self.request.assert_called_once_with(
            'GET', 'http://softboxen.com:1234/box/path',
            headers=self.headers, json=None)

    def test_ok_get_url_redirect_false(self):
        self.conn._http_call(
            'GET', path='box/path', headers=self.headers,
            allow_redirects=False)

        self.request.assert_called_once_with(
            'GET', 'http://softboxen.com:1234/box/path',
            headers=self.headers, json=None, allow_redirects=False)

    def test_ok_post(self):
        self.conn._http_call(
            'POST', path='box/path', data=self.data.copy(),
            headers=self.headers)

        self.request.assert_called_once_with(
            'POST', 'http://softboxen.com:1234/box/path',
            json=self.data, headers=self.headers)

    def test_ok_put(self):
        self.conn._http_call(
            'PUT', path='box/path', data=self.data.copy(),
            headers=self.headers)

        self.request.assert_called_once_with(
            'PUT', 'http://softboxen.com:1234/box/path',
            json=self.data, headers=self.headers)

    def test_ok_delete(self):
        expected_headers = self.headers

        self.conn._http_call(
            'DELETE', path='box/path', headers=self.headers.copy())

        self.request.assert_called_once_with(
            'DELETE', 'http://softboxen.com:1234/box/path',
            headers=expected_headers, json=None)

    def test_connection_error(self):
        self.request.side_effect = requests.exceptions.ConnectionError

        self.assertRaises(
            exceptions.NetworkError, self.conn._http_call, 'GET')

    def test_unknown_http_error(self):
        self.request.return_value.status_code = http_client.CONFLICT
        self.request.return_value.json.side_effect = ValueError('no json')

        with self.assertRaisesRegex(exceptions.HTTPError,
                                    'unknown error') as cm:
            self.conn._http_call(
                'GET', 'http://softboxen.com')

        exc = cm.exception

        self.assertEqual(http_client.CONFLICT, exc.status_code)
        self.assertIsNone(exc.body)

    def test_known_http_error(self):
        self.request.return_value.status_code = http_client.BAD_REQUEST

        with open('tests/unit/client/resources/samples/error.json') as f:
            self.request.return_value.json.return_value = json.load(f)

        with self.assertRaisesRegex(
                exceptions.BadRequestError,
                'Box is hopelessly broken') as cm:
            self.conn._http_call('GET', 'http://softboxen.com')

        exc = cm.exception

        self.assertEqual(http_client.BAD_REQUEST, exc.status_code)
        self.assertIsNotNone(exc.body)

    def test_not_found_error(self):
        self.request.return_value.status_code = http_client.NOT_FOUND
        self.request.return_value.json.side_effect = ValueError('no json')

        with self.assertRaisesRegex(
                exceptions.ResourceNotFoundError,
                'Resource http://softboxen.com not found') as cm:
            self.conn._http_call('GET', 'http://softboxen.com')

        exc = cm.exception

        self.assertEqual(http_client.NOT_FOUND, exc.status_code)

    def test_server_error(self):
        self.request.return_value.status_code = (
            http_client.INTERNAL_SERVER_ERROR)

        self.request.return_value.json.side_effect = ValueError('no json')

        with self.assertRaisesRegex(
                exceptions.ServerSideError, 'unknown error') as cm:
            self.conn._http_call('GET', 'http://softboxen.com')

        exc = cm.exception

        self.assertEqual(http_client.INTERNAL_SERVER_ERROR, exc.status_code)

    def test_access_error(self):
        self.request.return_value.status_code = http_client.FORBIDDEN
        self.request.return_value.json.side_effect = ValueError('no json')

        with self.assertRaisesRegex(
                exceptions.AccessError, 'unknown error') as cm:
            self.conn._http_call('GET', 'http://softboxen.com')

        exc = cm.exception

        self.assertEqual(http_client.FORBIDDEN, exc.status_code)
