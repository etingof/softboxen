#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#
import logging
import os

from softboxen import exceptions

import jinja2

LOG = logging.getLogger(__name__)


class Context:
    """Turn a dict into an object.

    The intension is to simplify context access in the templates.
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class CommandProcessor:
    """Create CLI REPR loop.

    :param model: box model
    :param input: terminal input stream
    :param output: terminal output stream
    :param template_root: location of Jinja2 templates for rendering
        command output by this command processor
    :param scopes: a sequence of names of nesting command processors
        followed by the name of this command processor
    """

    # Identify backend models to load and use
    VENDOR = '?'
    MODEL = '?'
    VERSION = '?'

    def __init__(self, model, input_stream, output_stream,
                 template_root=None, scopes=()):
        self._model = model
        self._input = input_stream
        self._output = output_stream
        self._scopes = scopes
        self._template_root = template_root
        self._template_dir = os.path.join(
            template_root, self.VENDOR, self.MODEL, self.VERSION,
            *scopes)

        self._jenv = jinja2.Environment(
            loader=(jinja2.FileSystemLoader(self._template_dir)
                    if template_root else None),
            trim_blocks=True, lstrip_blocks=True)

    def _render(self, command, *args, context=None):
        template_name = '%s.j2' % command

        try:
            tmpl = self._jenv.get_template(template_name)

            return tmpl.render(
                scopes=self._scopes,
                command=command,
                args=args,
                model=self._model,
                context=Context(**context))

        except jinja2.exceptions.TemplateError as exc:
            raise exceptions.TemplateError(
                command=command, processor=self.__class__.__name__,
                template_root=self._template_dir, error=exc)

    def _default_command_handler(self, command, *args, context=None):
        try:
            text = self._render(command, *args, context=context)

        except exceptions.TemplateError:
            raise exceptions.CommandSyntaxError(command=command)

        self._write(text)

    def _read(self):
        text = self._input.readline()
        return text.decode('utf-8')

    def _write(self, text):
        self._output.write(text.encode('utf-8'))

    def _get_command_func(self, line):
        if line.startswith(self.comment):
            return (lambda: None), '', []

        args = line.strip().split()
        command = args[0]
        args = args[1:]

        if command == self.negation:
            command += "_" + args.pop(0)

        command = command.replace('-', '_')

        matching = sorted(
            [c for c in dir(self) if c.startswith('do_' + command)])

        if len(matching) >= 1:
            return getattr(self, matching[0]), command, args

        if hasattr(self, 'on_unknown_command'):
            LOG.debug('Using unknown command handler for command '
                      '%s %s', command, args)

            return self.on_unknown_command, command, args

        LOG.debug('Using default command handler for command '
                  '%s %s', command, args)

        return self._default_command_handler, command, args

    def _parse_and_execute_command(self, line, context):
        if line.strip():
            func, command, args = self._get_command_func(line)
            if not func:
                LOG.debug("%s can't process : %s, falling back to "
                          "parent" % (self.__class__.__name__, line))
                return False

            else:
                func(command, *args, context=context)

        return True

    def _create_subprocessor(self, subprocessor, *scopes):
        return subprocessor(
            self._model, self._input, self._output,
            template_root=self._template_root,
            scopes=scopes)

    def process_command(self, line, context):
        self._parse_and_execute_command(line, context)

    def loop(self, context=None, raise_on_exit=True):
        if context is None:
            context = {}

        self.on_enter(context)
        self.on_cycle(context)

        while True:
            line = self._read()
            if not line:
                break

            try:
                self.process_command(line, context)

            except exceptions.CommandSyntaxError as exc:
                self.on_error(dict(context, command=exc.command))

            except exceptions.TerminalExitError:
                if raise_on_exit:
                    raise
                break

            self.on_cycle(context)

        self.on_exit(context)

    def _render_from_template(self, tmpl, context, ignore_errors=True):
        try:
            text = self._render(tmpl, context=context)

        except exceptions.TemplateError as exc:
            if not ignore_errors:
                raise

            LOG.debug('ignoring rendering template %s error: %s', tmpl, exc)
            return

        self._write(text)

    def on_cycle(self, context):
        self._render_from_template('on_cycle', context)

    def on_enter(self, context):
        self._render_from_template('on_enter', context)

    def on_exit(self, context):
        self._render_from_template('on_exit', context)

    def on_error(self, context):
        self._render_from_template('on_error', context)

    @property
    def comment(self):
        return '!'

    @property
    def negation(self):
        return 'no'

    def _dissect(self, args, *tokens):
        values = []

        for idx, token in enumerate(tokens):
            try:
                arg = args[idx]

            except IndexError:
                raise exceptions.CommandSyntaxError(command=' '.join(args))

            if type(token) == type:
                values.append(arg)

            elif not token.startswith(arg):
                raise exceptions.CommandSyntaxError(command=' '.join(args))

        return values
