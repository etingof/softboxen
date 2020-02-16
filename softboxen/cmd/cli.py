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


def main():

    parser = argparse.ArgumentParser(
                description='SoftBoxen CLI Simulator')

    parser.add_argument(
        '-v', '--version', action='version',
        version='%(prog)s ' + __version__)

    parser.add_argument(
        '--service-root', metavar='<URL>', type=str, required=True,
        help='URL of Softboxen REST API service root. '
             'Example: https://example.com/softboxen/v1/root.json')

    parser.add_argument(
        '--insecure', action='store_true',
        help='Disable TLS X.509 validation.')

    args = parser.parse_args()

    service_root = urlparse(args.service_root)
    prefix = os.path.dirname(service_root.path)
    filename = os.path.basename(service_root.path)

    conn = rest_client.RestClient(
        '%s://%s%s/' % (service_root.scheme, service_root.netloc, prefix),
        verify=not args.insecure,
    )

    root_resource = root.Root(conn, path=filename)

    for box in root_resource.boxen:
        print('vendor', box.vendor, 'model', box.model)
        for port in box.ports:
            print('port', port.name)
            print('access vlan', port.access_vlan.name)
            for vlan in port.trunk_vlans:
                print('trunk vlan', vlan.name)


if __name__ == '__main__':
    sys.exit(main())
