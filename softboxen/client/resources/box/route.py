#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import logging

from softboxen.client.resources import base

LOG = logging.getLogger(__name__)


class Route(base.Resource):
    """This class represents network routing entry resource."""
    dst = base.Field('dst')
    gw = base.Field('gw')
    metric = base.Field('metric')


class RouteCollection(base.ResourceCollection):
    """This class represents the collection of Route resources."""

    @property
    def _resource_type(self):
        return Route
