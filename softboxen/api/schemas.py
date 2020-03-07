#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

from softboxen.api import ma
from softboxen.api import models


class RootSchema(ma.ModelSchema):
    class Meta:
        fields = ('description', 'boxen', '_links')

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_root')})


class BoxSchema(ma.ModelSchema):
    class Meta:
        model = models.Box
        fields = ('id', 'vendor', 'model', 'version', 'uuid', 'description',
                  'hostname', 'mgmt_address', 'credentials',
                  'ports', 'routes', '_links')

    credentials = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_credentials', box_id='<id>')}})

    ports = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_ports', box_id='<id>')}})

    routes = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_routes', box_id='<id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_box', id='<id>'),
         'collection': ma.URLFor('show_boxen')})


class BoxenSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class BoxSchema(ma.ModelSchema):
        class Meta:
            model = models.Box
            fields = (
                'vendor', 'model', 'version', 'uuid',
                '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_box', id='<id>')})

    members = ma.Nested(BoxSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_boxen')})


class CredentialSchema(ma.ModelSchema):
    class Meta:
        model = models.Credential
        fields = ('id', 'protocol', 'credential', 'user', 'password',
                  'box', '_links')

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_credential', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_credentials', box_id='<box_id>')})


class CredentialsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class CredentialSchema(ma.ModelSchema):
        class Meta:
            model = models.Credential
            fields = ('_links',)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_credential', box_id='<box_id>', id='<id>')})

    members = ma.Nested(CredentialSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_credentials', box_id='<box_id>')})


class PortSchema(ma.ModelSchema):
    class Meta:
        model = models.Port
        fields = ('id', 'name', 'description', 'shutdown', 'speed',
                  'auto_negotiation', 'mtu', 'access_vlan',
                  'trunk_vlans', 'trunk_native_vlan',
                  'box', '_links')

    access_vlan = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor(
                'show_vlan_ports', box_id='<box_id>', port_id='<id>',
                role='access')}})

    trunk_vlans = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor(
                'show_vlan_ports', box_id='<box_id>', port_id='<id>',
                role='trunk')}})

    trunk_native_vlan = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor(
                'show_vlan_ports', box_id='<box_id>', port_id='<id>',
                role='native')}})

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_port', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_ports', box_id='<box_id>')})


class PortsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class PortSchema(ma.ModelSchema):
        class Meta:
            model = models.Port
            fields = ('_links',)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_port', box_id='<box_id>', id='<id>')})

    members = ma.Nested(PortSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_ports', box_id='<box_id>')})


class VlanPortSchema(ma.ModelSchema):
    class Meta:
        model = models.VlanPort
        fields = ('id', 'vlan_num', 'name', 'description', 'shutdown', 'mtu',
                  'access_group_in', 'access_group_out', 'ip_redirect',
                  'ip_proxy_arp', 'unicast_reverse_path_forwarding',
                  'load_interval', 'mpls_ip', 'access_on_port',
                  'trunk_on_port', 'trunk_native_on_port', 'box',
                  '_links')

    class PortSchema(ma.ModelSchema):
        class Meta:
            model = models.Port
            fields = ('_links',)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_port', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_ports', box_id='<box_id>')})

    class BoxSchema(ma.ModelSchema):
        class Meta:
            model = models.Box
            fields = ('_links',)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_box', id='<id>'),
             'collection': ma.URLFor('show_boxen')})

    _links = ma.Hyperlinks({
        'self': ma.URLFor(
            'show_vlan_port', box_id='<box_id>', port_id='<port_id>',
            role='<role>', id='<id>'),
        'collection': ma.URLFor(
            'show_vlan_ports', box_id='<box_id>', port_id='<port_id>',
            role='<role>')})

    access_on_port = ma.Nested(PortSchema)
    trunk_on_port = ma.Nested(PortSchema)
    trunk_native_on_port = ma.Nested(PortSchema)
    box = ma.Nested(BoxSchema)


class VlanPortsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class VlanPortSchema(ma.ModelSchema):
        class Meta:
            model = models.VlanPort
            fields = ('_links',)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_vlan_port', box_id='<box_id>', port_id='<port_id>',
                role='<role>', id='<id>')})

    members = ma.Nested(VlanPortSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor(
            'show_vlan_ports', box_id='<box_id>', port_id='<port_id>',
            role='<role>')})


class RouteSchema(ma.ModelSchema):
    class Meta:
        model = models.Credential
        fields = ('id', 'dst', 'gw', 'metric', 'box', '_links')

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_route', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_routes', box_id='<box_id>')})


class RoutesSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class RouteSchema(ma.ModelSchema):
        class Meta:
            model = models.Route
            fields = ('_links',)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_route', box_id='<box_id>', id='<id>')})

    members = ma.Nested(RouteSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_routes', box_id='<box_id>')})


