#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#


class DefaultConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'
    SQLALCHEMY_ECHO = False

    DEBUG = False

    SOFTBOXEN_MGMT_LISTEN_IP = '127.0.0.1'
    SOFTBOXEN_MGMT_LISTEN_PORT = 5000
    SOFTBOXEN_MGMT_SSL_CERT = None
    SOFTBOXEN_MGMT_SSL_KEY = None
