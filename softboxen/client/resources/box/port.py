#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import logging
import os

from softboxen.client.resources import base
from softboxen.client.resources.box import vlan_port

LOG = logging.getLogger(__name__)


class Port(base.Resource):
    """Represent physical port resource."""

    name = base.Field('name')
    description = base.Field('description')
    mode = base.Field('mode')
    shutdown = base.Field('shutdown')
    speed = base.Field('speed')
    auto_negotiation = base.Field('auto_negotiation')
    mtu = base.Field('mtu')

    @property
    def access_vlan(self):
        """Return `VlanPort` object for access VLAN."""
        return vlan_port.VlanPort(
            self._conn, base.get_sub_resource_path_by(
                self, 'access_vlan'))

    @property
    def trunk_vlans(self):
        """Return `VlanPortCollection` object for trunk VLANs."""
        return vlan_port.VlanPortCollection(
            self._conn, base.get_sub_resource_path_by(
                self, 'trunk_vlans'))

    @property
    def trunk_native_vlan(self):
        """Return `VlanPort` object for trunk native VLAN."""
        return vlan_port.VlanPort(
            self._conn, base.get_sub_resource_path_by(
                self, 'trunk_native_vlan'))

    def add_access_vlan(self, **fields):
        """Add new access VLAN."""
        vlan_port.VlanPort.create(
            self._conn,
            os.path.join(self.path, 'access_vlan'),
            **fields)

    def add_trunk_vlan(self, **fields):
        """Add new trunk VLAN."""
        vlan_port.VlanPort.create(
            self._conn,
            os.path.join(self.path, 'trunk_vlans'),
            **fields)

    def add_trunk_native_vlan(self, **fields):
        """Add new trunk native VLAN."""
        vlan_port.VlanPort.create(
            self._conn,
            os.path.join(self.path, 'trunk_native_vlan'),
            **fields)


class PortCollection(base.ResourceCollection):
    """Represent a collection of ports."""

    @property
    def _resource_type(self):
        return Port
