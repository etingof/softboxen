#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import argparse
import os
import sys

from softboxen.api import app
from softboxen.api import db
from softboxen.api import views  # noqa

DESCRIPTION = """\
Softboxen CLI simulator REST API.

Maintains network devices models in a persistent DB. Models
can be created, removed or changed by REST API.

Can be run as a WSGI application.
"""


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument(
        '--recreate-db',
        action='store_true',
        help='DANGER! Running with this flag wipes up REST API server DB! '
             'This switch makes sense only when running this tool for the '
             'first time.')

    parser.add_argument(
        '--config', type=str,
        help='Config file path. Can also be set via environment variable '
             'SOFTBOXEN_CONFIG.')

    parser.add_argument(
        '--interface', type=str,
        help='IP address of the local interface for REST API'
             'server to listen on. Can also be set via config variable '
             'SOFTBOXEN_LISTEN_IP. Default is all local interfaces.')

    parser.add_argument(
        '--port', type=int,
        help='TCP port to bind REST API server to.  Can also be '
             'set via config variable SOFTBOXEN_LISTEN_PORT. '
             'Default is 5000.')

    return parser.parse_args()


def main():

    args = parse_args()

    if args.config:
        os.environ['SOFTBOXEN_CONFIG'] = args.config

    config_file = os.environ.get('SOFTBOXEN_CONFIG')
    if config_file:
        app.config.from_pyfile(config_file)

    if args.interface:
        app.config['SOFTBOXEN_LISTEN_IP'] = args.interface

    if args.port:
        app.config['SOFTBOXEN_LISTEN_PORT'] = args.port

    if args.recreate_db:
        db.drop_all()
        db.create_all()
        return 0

    app.run(host=app.config.get('SOFTBOXEN_LISTEN_IP'),
            port=app.config.get('SOFTBOXEN_LISTEN_PORT'))

    return 0


if __name__ == '__main__':
    sys.exit(main())
