#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import logging

from softboxen.client.resources import base

LOG = logging.getLogger(__name__)


class Vlan(base.Resource):
    """This class represents VLAN resource."""
    number = base.Field('number')
    name = base.Field('name')
    description = base.Field('description')


class VlanCollection(base.ResourceCollection):
    """This class represents the collection of `Vlan` resources."""

    @property
    def _resource_type(self):
        return Vlan
