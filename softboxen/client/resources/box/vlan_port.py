#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import logging

from softboxen.client.resources import base
from softboxen.client.resources.box import port

LOG = logging.getLogger(__name__)


class VlanPort(base.Resource):
    """Represent VLAN port resource."""

    vlan_id = base.Field('vlan_id')
    name = base.Field('name')
    description = base.Field('description')
    shutdown = base.Field('shutdown')
    mtu = base.Field('mtu')
    access_group_in = base.Field('access_group_in')
    access_group_out = base.Field('access_group_out')
    ip_redirect = base.Field('ip_redirect')
    ip_proxy_arp = base.Field('ip_proxy_arp')
    unicast_reverse_path_forwarding = base.Field(
        'unicast_reverse_path_forwarding')
    load_interval = base.Field('load_interval')
    mpls_ip = base.Field('mpls_ip')

    @property
    def port(self):
        return port.Port(
            self._conn, base.get_sub_resource_path_by(self, 'port'))

    @property
    def ports(self):
        """Return `VlanPortCollection` object."""
        return VlanPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'))


class VlanPortCollection(base.ResourceCollection):
    """Represent a collection of VLAN ports."""

    @property
    def _resource_type(self):
        return VlanPort
