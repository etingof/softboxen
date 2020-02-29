#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import logging

from softboxen.client.resources import base
from softboxen.client.resources.box import box

LOG = logging.getLogger(__name__)


class Root(base.Resource):
    """Softboxen REST API service root.

    :param connector: A RestClient instance
    :param path: sub-URI path to the resource.
    """

    description = base.Field('description')
    """Service description."""

    def __init__(self, connector, path='/softboxen/v1'):

        super(Root, self).__init__(connector, path=path)

    @property
    def boxen(self):
        """Return a `BoxCollection` object."""
        return box.BoxCollection(
            self._conn, base.get_sub_resource_path_by(self, 'boxen'))

    def get_box(self, identity):
        """Return `Box` object by identity.

        :param identity: The identity of the Box resource.
        :raises: `UnknownDefaultError` if default box can't be determined.
        :returns: The Box object
        """
        return box.Box(self._conn, identity)
