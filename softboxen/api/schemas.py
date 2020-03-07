#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

from softboxen.api import ma
from softboxen.api import models


class BoxSchema(ma.ModelSchema):
    class Meta:
        model = models.Box
        fields = ('vendor', 'model', 'version', 'uuid', 'description',
                  'hostname', 'mgmt_address', 'credentials',
                  'ports', 'routes', '_links')

    class CredentialSchema(ma.ModelSchema):
        class Meta:
            model = models.Credential
            fields = ('_links',)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_credential', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_credentials', box_id='<box_id>')})

    class PortSchema(ma.ModelSchema):
        class Meta:
            model = models.Port
            fields = ('_links',)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_port', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_ports', box_id='<box_id>')})

    class RouteSchema(ma.ModelSchema):
        class Meta:
            model = models.Route
            fields = ('_links',)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_route', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_routes', box_id='<box_id>')})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_box', id='<id>'),
         'collection': ma.URLFor('show_boxen')})

    credentials = ma.Nested(CredentialSchema, many=True)
    ports = ma.Nested(PortSchema, many=True)
    routes = ma.Nested(RouteSchema, many=True)


class CredentialSchema(ma.ModelSchema):
    class Meta:
        model = models.Credential
        fields = ('protocol', 'credential', 'user', 'password',
                  'box', '_links')

    class BoxSchema(ma.ModelSchema):
        class Meta:
            model = models.Box
            fields = ('_links',)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_box', id='<id>'),
             'collection': ma.URLFor('show_boxen')})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_credential', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_credentials', box_id='<box_id>')})

    box = ma.Nested(BoxSchema)


class PortSchema(ma.ModelSchema):
    class Meta:
        model = models.Port
        fields = ('name', 'description', 'shutdown', 'speed',
                  'auto_negotiation', 'mtu', 'access_vlan',
                  'trunk_vlans', 'trunk_native_vlan',
                  'box', '_links')

    class VlanSchema(ma.ModelSchema):
        class Meta:
            model = models.VlanPort
            fields = ('_links',)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_vlan_port', box_id='<box_id>', port_id='<port_id>',
                id='<id>'),
             'collection': ma.URLFor(
                'show_vlan_ports', box_id='<box_id>', port_id='<port_id>')})

    class BoxSchema(ma.ModelSchema):
        class Meta:
            model = models.Box
            fields = ('_links',)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_box', id='<id>'),
             'collection': ma.URLFor('show_boxen')})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_port', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_ports', box_id='<box_id>')})

    access_vlan = ma.Nested(VlanSchema, many=True)
    trunk_vlans = ma.Nested(VlanSchema, many=True)
    trunk_native_vlan = ma.Nested(VlanSchema, many=True)
    box = ma.Nested(BoxSchema)


class VlanPortSchema(ma.ModelSchema):
    class Meta:
        model = models.VlanPort
        fields = ('vlan_num', 'name', 'description', 'shutdown', 'mtu',
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
            id='<id>'),
        'collection': ma.URLFor(
            'show_vlan_ports', box_id='<box_id>', port_id='<port_id>')})

    access_on_port = ma.Nested(PortSchema)
    trunk_on_port = ma.Nested(PortSchema)
    trunk_native_on_port = ma.Nested(PortSchema)
    box = ma.Nested(BoxSchema)


class RouteSchema(ma.ModelSchema):
    class Meta:
        model = models.Credential
        fields = ('dst', 'gw', 'metric', 'box', '_links')

    class BoxSchema(ma.ModelSchema):
        class Meta:
            model = models.Box
            fields = ('_links',)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_box', id='<id>'),
             'collection': ma.URLFor('show_boxen')})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_route', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_routes', box_id='<box_id>')})

    box = ma.Nested(BoxSchema)
