#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#
import argparse
import sys
import os
from urllib.parse import urlparse

from softboxen import __version__
from softboxen.client.resources import root
from softboxen.client import rest_client
from softboxen.cli import factory


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
        '--list-clis', action='store_true',
        help='Discover and print out installed softboxen CLI '
             'implementations')

    parser.add_argument(
        '--list-boxen', action='store_true',
        help='Discover and print out existing box models')

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
        for box in root_resource.boxen:
            print('Vendor %s, model %s, version %s, instance %s' % (
                  box.vendor, box.model, box.version, box.uuid))
        return 0


if __name__ == '__main__':
    sys.exit(main())
