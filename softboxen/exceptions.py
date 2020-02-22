#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

from http import client as http_client
import logging


LOG = logging.getLogger(__name__)


class SoftboxenError(Exception):
    """General Softboxen error."""

    message = None

    def __init__(self, **kwargs):
        if self.message and kwargs:
            self.message = self.message % kwargs

        super(SoftboxenError, self).__init__(self.message)


class InvalidInputError(SoftboxenError):
    message = 'Invalid input: %(error)s'


class NetworkError(SoftboxenError):
    message = 'Unable to connect to %(url)s. Error: %(error)s'


class MissingAttributeError(SoftboxenError):
    message = ('The attribute %(attribute)s is missing from the '
               'resource %(resource)s')


class MalformedAttributeError(SoftboxenError):
    message = ('The attribute %(attribute)s is malformed in the '
               'resource %(resource)s: %(error)s')


class InvalidParameterValueError(SoftboxenError):
    message = ('The parameter "%(parameter)s" value "%(value)s" is invalid. '
               'Valid values are: %(valid_values)s')


class ExtensionNotFoundError(SoftboxenError):
    message = ('Cannot find CLI extension for %(vendor)s, %(model)s, '
               '%(version)s')


class HTTPError(SoftboxenError):
    """Basic exception for HTTP errors"""

    status_code = None
    """HTTP status code."""

    body = None
    """Error JSON document, if present."""

    message = 'HTTP %(method)s %(url)s returned code %(code)s. %(error)s'

    def __init__(self, method, url, response):
        self.status_code = response.status_code
        try:
            body = response.json()

        except ValueError:
            LOG.warning('Error response from %(method)s %(url)s '
                        'with status code %(code)s has no JSON body',
                        {'method': method, 'url': url, 'code':
                         self.status_code})
            error = 'unknown error'

        else:
            self.body = body.get('error', {})
            error = body.get('error', 'unknown error')

        kwargs = {'method': method, 'url': url, 'code': self.status_code,
                  'error': error}

        LOG.debug('HTTP response for %(method)s %(url)s: '
                  'status code: %(code)s, error: %(error)s', kwargs)

        super(HTTPError, self).__init__(**kwargs)


class BadRequestError(HTTPError):
    pass


class ResourceNotFoundError(HTTPError):
    message = 'Resource %(url)s not found'


class ServerSideError(HTTPError):
    pass


class AccessError(HTTPError):
    pass


def handle_error_response(method, url, response):
    """Turn HTTP code into raised exception."""
    if response.status_code < http_client.BAD_REQUEST:
        return

    elif response.status_code == http_client.NOT_FOUND:
        raise ResourceNotFoundError(method, url, response)

    elif response.status_code == http_client.BAD_REQUEST:
        raise BadRequestError(method, url, response)

    elif response.status_code in (http_client.UNAUTHORIZED,
                                  http_client.FORBIDDEN):
        raise AccessError(method, url, response)

    elif response.status_code >= http_client.INTERNAL_SERVER_ERROR:
        raise ServerSideError(method, url, response)

    else:
        raise HTTPError(method, url, response)
