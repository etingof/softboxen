#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

from softboxen.cli import base
from softboxen import exceptions


class BaseCommandProcessor(base.CommandProcessor):
    """Create CLI REPR loop for example switch."""
    VENDOR = 'example'
    MODEL = 'switch'
    VERSION = '1'


class PreLoginCommandProcessor(BaseCommandProcessor):
    """"""
    def on_unknown_command(self, command, *args, context=None):
        subprocessor = self._create_subprocessor(
            LoginCommandProcessor, 'login')

        context['username'] = command

        subprocessor.loop(context=context)


class LoginCommandProcessor(BaseCommandProcessor):

    def on_unknown_command(self, command, *args, context=None):
        username = context.pop('username')
        password = command

        for creds in self._model.credentials:
            if creds.user == username and creds.password == password:
                break

        else:
            text = self._render('password', context=context)
            self._write(text)
            raise exceptions.TerminalExitError()

        subprocessor = self._create_subprocessor(
            UserViewCommandProcessor, 'login', 'mainloop')

        subprocessor.loop(context=context)


class UserViewCommandProcessor(BaseCommandProcessor):

    def do_enable(self, command, *args, context=None):

        subprocessor = self._create_subprocessor(
            EnableCommandProcessor, 'login', 'mainloop', 'enable')

        subprocessor.loop(context=context)


class EnableCommandProcessor(BaseCommandProcessor):

    def on_unknown_command(self, command, *args, context=None):
        username = '<enable>'
        password = command

        for creds in self._model.credentials:
            if creds.user == username and creds.password == password:
                break

        else:
            text = self._render('password', context=context)
            self._write(text)
            raise exceptions.TerminalExitError()

        subprocessor = self._create_subprocessor(
            AdminCommandProcessor, 'login', 'mainloop', 'enable', 'admin')

        subprocessor.loop(context=context)


class AdminCommandProcessor(BaseCommandProcessor):
    pass


