#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#
import argparse
import logging
import os
import sys
from urllib.parse import urlparse

from softboxen import __version__
from softboxen.cli import factory
from softboxen.client import rest_client
from softboxen.client.resources import root
from softboxen import exceptions

LOG = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser(
                description='SoftBoxen CLI Simulator')

    parser.add_argument(
        '-v', '--version', action='version',
        version='%(prog)s ' + __version__)

    parser.add_argument(
        '--service-root', metavar='<URL>', type=str,
        help='URL of Softboxen REST API service root. '
             'Example: https://example.com/softboxen/v1/root.json')

    parser.add_argument(
        '--insecure', action='store_true',
        help='Disable TLS X.509 validation.')

    parser.add_argument(
        '--template-root', metavar='<DIR>', type=str,
        help='Top directory of CLI command loop Jinja2 templates')

    parser.add_argument(
        '--list-clis', action='store_true',
        help='Discover and print out installed softboxen CLI '
             'implementations')

    parser.add_argument(
        '--list-boxen', action='store_true',
        help='Discover and print out existing box models')

    parser.add_argument(
        '--box-uuid', metavar='<UUID>', type=str,
        help='Run CLI instance using specified box instance as a '
             'backend model')

    args = parser.parse_args()

    if args.list_clis:
        clis = factory.load_clis()
        for cli in clis:
            print('Vendor %s, model %s, version %s' % (
                cli.VENDOR, cli.MODEL, cli.VERSION))
        return 0

    if not args.service_root:
        parser.error('--service-root is required')
        return

    service_root = urlparse(args.service_root)
    prefix = os.path.dirname(service_root.path)
    filename = os.path.basename(service_root.path)

    conn = rest_client.RestClient(
        '%s://%s%s/' % (service_root.scheme, service_root.netloc, prefix),
        verify=not args.insecure,
    )

    root_resource = root.Root(conn, path=filename)

    if args.list_boxen:
        for model in root_resource.boxen:
            print('Vendor %s, model %s, version %s, instance %s' % (
                  model.vendor, model.model, model.version, model.uuid))
        return 0

    if not args.box_uuid:
        parser.error('--box-uuid is required')
        return

    for model in root_resource.boxen:
        if model.uuid == args.box_uuid:
            LOG.debug('Found requested box with UUID %s', model.uuid)
            break

    else:
        parser.error('Requested box with UUID %s not found' % args.box_uuid)
        return

    try:
        cli = factory.get_box(model.vendor, model.model, model.version)

    except exceptions.ExtensionNotFoundError as exc:
        parser.error(exc)
        return

    stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
    stdout = os.fdopen(sys.stdout.fileno(), 'wb', 0)

    command_processor = cli(
        model, stdin, stdout, template_root=args.template_root)

    command_processor.loop(raise_on_exit=False)


if __name__ == '__main__':
    sys.exit(main())
