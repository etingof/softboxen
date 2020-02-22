#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#


class CommandProcessor:
    VENDOR = '?'
    MODEL = '?'
    VERSION = '?'

    def __init__(self, model, input, output, subprocessor=None):
        """Create CLI REPR loop object.

        :param model: box model
        :param input: terminal input stream
        :param output: terminal output stream
        :param subprocessor: child REPR loop to handle context-specific
            commands
        """
