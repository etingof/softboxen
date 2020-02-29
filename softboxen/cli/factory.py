#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import logging

import pkg_resources

from softboxen.cli import base
from softboxen import exceptions

LOG = logging.getLogger(__name__)


def load_clis(namespace='softboxen.cli'):
    """Return discovered softboxen CLI extension classes.

    :param namespace: entry point prefix to search
    :return: a sequence of discovered CLI implementation classes
    """
    LOG.debug('searching namespace %s', namespace)

    extensions = {
        entry_point.name: entry_point.load()
        for entry_point
        in pkg_resources.iter_entry_points(namespace)
    }

    discovered_clis = []

    for identity, impl in extensions.items():
        if not issubclass(impl, base.CommandProcessor):
            LOG.warning('ignoring non-compliant implementation %s', identity)
            continue

        LOG.debug('found extension module %s for vendor %s, model %s, '
                  'version %s', impl, impl.VENDOR, impl.MODEL, impl.VERSION)

        discovered_clis.append(impl)

    return discovered_clis


def get_box(vendor, model, version):
    """Get concrete box CLI implementation.

    Given box vendor, model and version searches Python package namespace
    for suitable implementation.

    For example, `get_box('cisco', '5300', '1.11)` will return CLI
    implementation for requested router type.
    """
    clis = load_clis()

    for cli in clis:
        if cli.VENDOR != vendor:
            continue

        if cli.MODEL != model:
            continue

        if cli.VERSION != version:
            continue

        return cli

    raise exceptions.ExtensionNotFoundError(
        vendor=vendor, model=model, version=version)
