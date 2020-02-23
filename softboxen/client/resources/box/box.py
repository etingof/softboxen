#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import logging

from softboxen.client.resources import base
from softboxen.client.resources.box import credentials
from softboxen.client.resources.box import route
from softboxen.client.resources.box import port

LOG = logging.getLogger(__name__)


class Box(base.Resource):
    """A class representing a ComputerSystem

    :param connection: A RestClient instance
    :param identity: The identity of the System resource
    """

    vendor = base.Field('vendor', required=True)
    """Network device vendor e.g. cisco"""

    model = base.Field('model', required=True)
    """Network device model e.g. 5300"""

    version = base.Field('version', required=True)
    """Network device model version e.g. 1.2.3"""

    uuid = base.Field('uuid', required=True)
    """Network device unique instance ID"""

    description = base.Field('description')
    """The description of this box"""

    hostname = base.Field('hostname')
    """Network device model e.g. 5300"""

    mgmt_address = base.Field('mgmt_address')
    """Management IP address"""

    @property
    def credentials(self):
        """A reference `CredentialsCollection`."""
        return credentials.CredentialsCollection(
            self._conn, base.get_sub_resource_path_by(
                self, 'credentials'))

    @property
    def routes(self):
        """A reference `RouteCollection`."""
        return route.RouteCollection(
            self._conn, base.get_sub_resource_path_by(self, 'routes'))

    @property
    def ports(self):
        """A reference `PortCollection`."""
        return port.PortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'))


class BoxCollection(base.ResourceCollection):
    """A class representing a BoxCollection

    :param connection: A RestClient instance
    :param path: The canonical path to the Box collection resource
    """

    @property
    def _resource_type(self):
        return Box
