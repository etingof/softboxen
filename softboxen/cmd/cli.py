#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#
import argparse
import sys

from softboxen import __version__


def main():

    parser = argparse.ArgumentParser(
                description='SoftBoxen CLI Simulator')

    parser.add_argument(
        '-v', '--version', action='version', version='%(prog)s ' + __version__
    )

    args = parser.parse_args()


if __name__ == '__main__':
    sys.exit(main())
