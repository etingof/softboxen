#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#


class CommandProcessor:
    """Create CLI REPR loop.

    :param model: box model
    :param input: terminal input stream
    :param output: terminal output stream
    :param subprocessor: child REPR loop to handle context-specific
        commands
    """
    VENDOR = '?'
    MODEL = '?'
    VERSION = '?'

    def __init__(self, model, input, output, subprocessor=None):
        return

    def loop(self):
        """Run CLI REPR loop."""
