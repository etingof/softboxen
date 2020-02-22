#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import copy
import logging

from softboxen import exceptions

LOG = logging.getLogger(__name__)


class Field:
    """Scalar field of a JSON object.

    :param path: JSON field to fetch the value from. Either a string,
        or a list of strings in case of a nested field.
    :param required: whether this field is required. Missing required
        fields result in MissingAttributeError.
    :param default: the default value to use when the field is missing.
        Only has effect when the field is not required.
    :param converter: a callable to transform and/or validate the received
        value.
    """

    def __init__(self, path, required=False, default=None, converter=None):
        if not isinstance(path, list):
            path = [path]

        elif not path:
            raise exceptions.InvalidInputError(
                error='Path cannot be empty')

        self._path = path
        self._required = required
        self._default = default
        self._converter = converter

    def _load(self, body, resource, nested_in=None):
        """Load a field from a JSON object.

        :param body: parsed JSON body.
        :param resource: `Resource` instance for which the field is
            loaded.
        :param nested_in: parent resource path.
        :raises: MissingAttributeError if a required field is missing.
        :raises: MalformedAttributeError on invalid field value or type.
        :returns: field value.
        """
        name = self._path[-1]
        for path_item in self._path[:-1]:
            body = body.get(path_item, {})

        try:
            item = body[name]

        except KeyError:
            if self._required:
                path = (nested_in or []) + self._path
                raise exceptions.MissingAttributeError(
                    attribute='/'.join(path),
                    resource=resource.path)
            else:
                return self._default

        if self._converter is None:
            return item

        try:
            return self._converter(item)

        except Exception as exc:
            path = (nested_in or []) + self._path
            raise exceptions.MalformedAttributeError(
                attribute='/'.join(path),
                resource=resource.path,
                error=exc)


def _collect_fields(resource):
    """Collect fields from JSON document.

    :param resource: `Resource` instance.
    :returns: generator of tuples (key, field)
    """
    for attr in dir(resource.__class__):
        field = getattr(resource.__class__, attr)
        if isinstance(field, Field):
            yield (attr, field)


class CollectionField(Field):
    """A list of objects field."""

    def __init__(self, *args, **kwargs):
        super(CollectionField, self).__init__(*args, **kwargs)
        self._subfields = dict(_collect_fields(self))

    def _load(self, body, resource, nested_in=None):
        """Load a field from a JSON object.

        :param body: parent JSON body.
        :param resource: parent resource.
        :param nested_in: parent resource name.
        :returns: a new list object containing subfields.
        """
        nested_in = (nested_in or []) + self._path
        values = super(CollectionField, self)._load(body, resource)
        if values is None:
            return

        instances = []
        for value in values:
            instance = copy.copy(self)
            for attr, field in self._subfields.items():
                # Hide the Field object behind the real value
                setattr(instance, attr, field._load(
                    value, resource, nested_in))
            instances.append(instance)

        return instances


class EnumerationField(Field):
    """Enumerated field of a JSON object.

    :param field: JSON field to fetch the value from.
    :param mapping: a `dict` to look up mapped values at.
    :param required: whether this field is required. Missing required
        fields result in MissingAttributeError.
    :param default: the default value to use when the field is missing.
    """
    def __init__(self, field, mapping, required=False, default=None):
        if not isinstance(mapping, dict):
            raise exceptions.InvalidInputError(
                error="%s initializer must be a "
                      "dict" % self.__class__.__name__)

        super(EnumerationField, self).__init__(
            field, required=required, default=default,
            converter=mapping.get)


class Resource:
    """Represent a JSON document.

    JSON document fields are set as object attributes with
    `Field` instances as values.

    Lazily loads hyperlinked JSON documents.

    :param connection: A RestClient instance
    :param path: sub-URI path to the resource.
    """

    def __init__(self, connection, path=''):
        self._conn = connection
        self._path = path
        self._json = None

        self.load()

    def _parse_attributes(self, json_doc):
        """Parse the attributes of a resource.

        Parsed JSON fields are set to `self` as declared in the class.

        :param json_doc: parsed JSON document in form of Python types
        """
        for attr, field in _collect_fields(self):
            setattr(self, attr, field._load(json_doc, self))

    def load(self):
        """Load and parse JSON document.

        :raises: ResourceNotFoundError
        :raises: NetworkError
        :raises: HTTPError
        """
        data = self._conn.get(path=self._path)
        self._json = data.json() if data.content else {}

        LOG.debug('Received representation of %(type)s %(path)s: %(json)s',
                  {'type': self.__class__.__name__,
                   'path': self._path, 'json': self._json})
        self._parse_attributes(self._json)

    @property
    def json(self):
        return self._json

    @property
    def path(self):
        return self._path


def get_sub_resource_path_by(resource, subresource_name):
    """Helper function to find the subresource path

    :param resource: Resource instance on which the name
        gets queried upon.
    :param subresource_name: name of the resource attribute.
    :returns: Resource path.
    """
    if not subresource_name:
        raise exceptions.InvalidInputError(
            error='subresource cannot be empty')

    if not isinstance(subresource_name, list):
        subresource_name = [subresource_name]

    body = resource.json
    for path_item in subresource_name:
        body = body.get(path_item, {})

    if not body:
        raise exceptions.MissingAttributeError(
            attribute='/'.join(subresource_name), resource=resource.path)

    try:
        return get_member_identity(body)

    except (TypeError, KeyError):
        attribute = '/'.join(subresource_name)
        raise exceptions.MissingAttributeError(
            attribute=attribute, resource=resource.path)


def get_member_identity(member):
    """Return member identity.

    Expected JSON document structured like this:

    {
        "_links": {
            "self": "/path/to/member"
        }
    }

    :param member: JSON document containing collection member
    :returns: Member document location
    """
    path = member.get('_links')
    if not path:
        raise exceptions.MissingAttributeError(
            attribute='_links', resource=member)

    path = path.get('self')
    if not path:
        raise exceptions.MissingAttributeError(
            attribute='_links', resource=member)

    return path.rstrip('/')


def get_members_identities(members):
    """Return members identities from a collection.

    Expected JSON document structured like this:

    [
        {
            "_links": {
                "self": "/path/to/member"
            }
        }
    ]

    :param members: A sequence of JSON documents referring to members
    :returns: A sequence of member paths
    """
    members_list = []
    for member in members:
        member = get_member_identity(member)
        if not member:
            continue

        members_list.append(member)

    return members_list


class ResourceCollection(Resource):
    """Represent a collection of references to JSON documents.

    :param connection: A RestClient instance
    :param path: sub-URI path to the resource collection.
    """
    MEMBERS_ATTR = 'members'

    members_identities = Field(
        MEMBERS_ATTR, default=[], converter=get_members_identities)

    def __init__(self, connection, path):
        super(ResourceCollection, self).__init__(
            connection, path)
        LOG.debug('Received %(count)d member(s) for %(type)s %(path)s',
                  {'count': len(self.members_identities),
                   'type': self.__class__.__name__, 'path': self._path})

    @property
    def _resource_type(self):
        """`Resource` subclass that the collection contains."""
        return Resource

    def get_member(self, identity):
        """Return `Resource` object identified by `identity`.

        Lazily pulls `Resource` object from the collection.

        :param identity: The identity of the `Resource` object
            in the collection
        :returns: The `Resource` object
        :raises: ResourceNotFoundError
        """
        return self._resource_type(self._conn, identity)

    def __iter__(self):
        for identity in self.members_identities:
            yield self.get_member(identity)
