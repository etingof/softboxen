#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import logging

from softboxen.client.resources import base

LOG = logging.getLogger(__name__)


class Credentials(base.Resource):
    protocol = base.Field('protocol')
    user = base.Field('user')
    password = base.Field('password')


class CredentialsCollection(base.ResourceCollection):
    """This class represents the collection of Storage resources"""

    @property
    def _resource_type(self):
        return Credentials
