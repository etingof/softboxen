#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

from softboxen.cli import base


class CommandProcessor(base.CommandProcessor):
    """Create CLI REPR loop for example switch."""
    VENDOR = 'example'
    MODEL = 'switch'
    VERSION = '1'
