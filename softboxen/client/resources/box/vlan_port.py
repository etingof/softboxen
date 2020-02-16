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
    """This class represents VLAN port resource."""
    name = base.Field('name')
    description = base.Field('description')
    mode = base.Field('mode')
    shutdown = base.Field('shutdown')
    vrf = base.Field('vrf')
    speed = base.Field('speed')
    auto_negotiation = base.Field('auto_negotiation')
    mtu = base.Field('mtu')
    lldp_transmit = base.Field('lldp_transmit')
    lldp_receive = base.Field('lldp_receive')
    lldp_med = base.Field('lldp_med')
    lldp_med_transmit_capabilities = base.Field(
        'lldp_med_transmit_capabilities')
    lldp_med_transmit_network_policy = base.Field(
        'lldp_med_transmit_network_policy')
    spanning_tree = base.Field('spanning_tree')
    spanning_tree_portfast = base.Field('spanning_tree_portfast')
    ntp = base.Field('ntp')
    access_group_in = base.Field('access_group_in')
    access_group_out = base.Field('access_group_out')
    vrrp_common_authentication = base.Field('vrrp_common_authentication')
    vrrp_version = base.Field('vrrp_version')
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
        """A reference `VlanPortCollection`."""
        return VlanPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'))


class VlanPortCollection(base.ResourceCollection):
    """This class represents the collection of `VlanPort` resources."""

    @property
    def _resource_type(self):
        return VlanPort
