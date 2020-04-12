
# Network equipment CLI emulator

[![PyPI](https://img.shields.io/pypi/v/softboxen.svg?maxAge=1800)](https://pypi.org/project/softboxen)
[![Python Versions](https://img.shields.io/pypi/pyversions/softboxen.svg)](https://pypi.org/project/softboxen/)
[![Build status](https://travis-ci.org/etingof/softboxen.svg?branch=master)](https://secure.travis-ci.org/etingof/softboxen)
[![Coverage Status](https://img.shields.io/codecov/c/github/etingof/softboxen.svg)](https://codecov.io/github/etingof/softboxen)
[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/etingof/softboxen/master/LICENSE.rst)


The goal of `softboxen` project is to emulate the presence of a large number
of network devices (such as switches, routers, modems etc) on the network.

These emulated devices expose their management interfaces and support
command-line dialogues in a reasonably convincing way. The main use-case
for `softboxen`is to create a testing environment for network management
and automation harness.

For more information on `softboxen` please refer to
[user documentation](http://snmplabs.com/softboxen).

## How to run example CLI

The easiest way to play with the example CLI (shipped along with main distribution
as the `softboxen-example-switch`) is to run two tox jobs on the softboxen
repo - one that starts up REST API server and populates the example model in
the DB, and the other that installs example CLI implementation package and
runs CLI frontend against REST API server.

In one terminal:

    $ tox -e example-restapi -- --keep-running

In the other terminal:

    $ tox -e example-restcli
    
     / ____|      / _| | | |
    | (___   ___ | |_| |_| |__   _____  _____ _ __
     \___ \ / _ \|  _| __| '_ \ / _ \ \/ / _ \ '_ \
     ____) | (_) | | | |_| |_) | (_) >  <  __/ | | |
    |_____/ \___/|_|  \__|_.__/ \___/_/\_\___|_| |_|
    
    
    Hint: login credentials: admin/secret
    
    login:admin
    Password:secret
    Last login on 01.03.2020

Interactive menus will guide you through the implemented commands.

## How to add new emulated CLI

For more information on this matter, please refer to the
[developer's documentation](http://snmplabs.com/softboxen/development.html).

## How to get softboxen

The softboxen package is distributed under terms and conditions of 2-clause
BSD [license](https://github.com/etingof/softboxen/LICENSE.rst). Source code is freely
available as a GitHub [repo](https://github.com/etingof/softboxen).

You could `pip install softboxen` or download it from [PyPI](https://pypi.org/project/softboxen).

If something does not work as expected, 
[open an issue](https://github.com/etingof/softboxen/issues) at GitHub.

Copyright (c) 2020, [Ilya Etingof](mailto:etingof@gmail.com). All rights reserved.
