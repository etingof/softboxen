
# Network equipment simulator

[![PyPI](https://img.shields.io/pypi/v/softboxen.svg?maxAge=1800)](https://pypi.org/project/softboxen)
[![Python Versions](https://img.shields.io/pypi/pyversions/softboxen.svg)](https://pypi.org/project/softboxen/)
[![Build status](https://travis-ci.org/etingof/softboxen.svg?branch=master)](https://secure.travis-ci.org/etingof/softboxen)
[![Coverage Status](https://img.shields.io/codecov/c/github/etingof/softboxen.svg)](https://codecov.io/github/etingof/softboxen)
[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/etingof/softboxen/master/LICENSE.rst)

*This project is being in active development. Not ready for use yet!*

The goal of `softboxen` project is to simulate the presence of a large number
of network devices (such as switches, routers, modems etc) from a system
administrator perspective.

These devices should expose their management interfaces and support
command-line dialogues in a reasonably convincing way. The main use-case
for `softboxen` is to create a testing environment for network management
and automation harness.

The system architecture being considered at the moment is this:

![system architecture](docs/arch.png)

## How to get softboxen

The softboxen package is distributed under terms and conditions of 2-clause
BSD [license](https://github.com/etingof/softboxen/LICENSE.rst). Source code is freely
available as a GitHub [repo](https://github.com/etingof/softboxen).

You could `pip install softboxen` or download it from [PyPI](https://pypi.org/project/softboxen).

If something does not work as expected, 
[open an issue](https://github.com/etingof/softboxen/issues) at GitHub.

Copyright (c) 2020, [Ilya Etingof](mailto:etingof@gmail.com). All rights reserved.
