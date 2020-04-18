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

    def do_exit(self, command, *args, context=None):
        raise exceptions.TerminalExitError()


class ReadInputCommandProcessor(base.CommandProcessor):
    """Create CLI REPR loop for example switch."""

    VENDOR = 'example'
    MODEL = 'switch'
    VERSION = '1'


class PreLoginCommandProcessor(ReadInputCommandProcessor):

    def on_unknown_command(self, command, *args, context=None):
        subprocessor = self._create_subprocessor(
            LoginCommandProcessor, 'login')

        context['username'] = command

        subprocessor.loop(context=context)


class LoginCommandProcessor(ReadInputCommandProcessor):

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

        subprocessor.loop(context=context, raise_on_exit=False)


class EnableCommandProcessor(ReadInputCommandProcessor):

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

    def do_show(self, command, *args, context=None):
        port_name, = self._dissect(
            args, 'interface', 'status', 'ethernet', str)

        try:
            port = self._model.ports.find_by_field_value(
                'name', port_name)

        except exceptions.SoftboxenError:
            raise exceptions.CommandSyntaxError(command=command)

        text = self._render(
            'show_interfaces_status_ethernet',
            context=dict(context, port=port))

        self._write(text)

    def do_configure(self, command, *args, context=None):
        subprocessor = self._create_subprocessor(
            ConfigureCommandProcessor, 'login', 'mainloop',
            'enable', 'admin', 'configure')

        subprocessor.loop(context=context, raise_on_exit=False)


class ConfigureInterfaceMixIn:

    def do_interface(self, command, *args, context=None):
        port_name, = self._dissect(args, 'ethernet', str)

        port = self._model.ports.find_by_field_value('name', port_name)

        subprocessor = self._create_subprocessor(
            ConfigureIfEthCommandProcessor, 'login', 'mainloop',
            'enable', 'admin', 'configure', 'interface_ethernet')

        subprocessor.loop(
            context=dict(context, port=port), raise_on_exit=False,
            return_to=ConfigureCommandProcessor)


class ConfigureRouteMixIn:

    def do_route(self, command, *args, context=None):
        subprocessor = self._create_subprocessor(
            ConfigureRouteCommandProcessor, 'login', 'mainloop',
            'enable', 'admin', 'configure', 'route')

        subprocessor.loop(
            context=context, raise_on_exit=False,
            return_to=ConfigureCommandProcessor)


class ConfigureCommandProcessor(
        BaseCommandProcessor, ConfigureInterfaceMixIn, ConfigureRouteMixIn):
    """Dual command CommandProcessor.

    This CommandProcessor supports two sub-menus at the same menu level.

        configure -> interface ...
                  -> route

    Both sub-menus exit back to this CommandProcessor.
    """


class ConfigureIfEthCommandProcessor(
        BaseCommandProcessor, ConfigureRouteMixIn):
    """Dual command CommandProcessor.

    This CommandProcessor supports one command and one-submenu at the
    same menu level.

        interface -> switchport ...
                  -> route

    Sub-menu exits back to `ConfigureCommandProcessor`, not to this one.
    """

    def do_switchport(self, command, *args, context=None):
        vlan_name, = self._dissect(
            args, 'allowed', 'vlan', 'add', str, 'tagged')

        port = context.pop('port')

        port.add_access_vlan(name=vlan_name)


class ConfigureRouteCommandProcessor(
        BaseCommandProcessor, ConfigureInterfaceMixIn):
    """Dual command CommandProcessor.

    This CommandProcessor supports one command and one-submenu at the
    same menu level.

        interface -> table show
                  -> interface ...

    Sub-menu exits back to `ConfigureCommandProcessor`, not to this one.
    """

    def do_table_show(self, command, *args, context=None):
        text = self._render(
            'show_routes',
            context=dict(context, routes=self._model.routes))

        self._write(text)
