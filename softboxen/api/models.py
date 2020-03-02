#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#
import uuid

from softboxen.api import db


class Box(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    vendor = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(64), nullable=False)
    version = db.Column(db.String(64), nullable=False)
    uuid = db.Column(
        db.String(36), nullable=False, unique=True,
        default=lambda: str(uuid.uuid1()))
    description = db.Column(db.String())
    hostname = db.Column(db.String(64))
    mgmt_address = db.Column(db.String(32))
    credentials = db.relationship('Credential', backref='box', lazy='dynamic')
    ports = db.relationship('Port', backref='box', lazy='dynamic')
    vlan_ports = db.relationship('VlanPort', backref='box', lazy='dynamic')
    routes = db.relationship('Route', backref='box', lazy='dynamic')


class Credential(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    protocol = db.Column(
        db.Enum('password'), nullable=False, default='password')
    user = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(32), nullable=True)
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))


class Port(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String())
    shutdown = db.Column(db.Boolean(), default=False)
    speed = db.Column(db.Enum('10M', '1G', '10G'), default='1G')
    auto_negotiation = db.Column(db.Boolean(), default=True)
    mtu = db.Column(db.Integer(), default=1500)
    access_vlan = db.relationship(
        'VlanPort', backref='access_on_port', lazy='dynamic')
    trunk_vlans = db.relationship(
        'VlanPort', backref='trunk_on_port', lazy='dynamic')
    trunk_native_vlan = db.relationship(
        'VlanPort', backref='trunk_native_on_port', lazy='dynamic')
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))


class VlanPort(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    vlan_num = db.Column(db.Integer(), nullable=False)
    name = db.Column(db.String(64))
    description = db.Column(db.String())
    shutdown = db.Column(db.Boolean(), default=False)
    mtu = db.Column(db.Integer(), default=1500)
    access_group_in = db.Column(db.String(64))
    access_group_out = db.Column(db.String(64))
    ip_redirect = db.Column(db.Boolean(), default=False)
    ip_proxy_arp = db.Column(db.Boolean(), default=False)
    unicast_reverse_path_forwarding = db.Column(db.Boolean(), default=False)
    load_interval = db.Column(db.Integer())
    mpls_ip = db.Column(db.String(32))
    port_id = db.Column(db.Integer, db.ForeignKey('port.id'))
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))


class Route(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    dst = db.Column(db.String(23))
    gw = db.Column(db.String(23))
    metric = db.Column(db.Integer(), default=1)
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
