
# Network equipment CLI simulator

[![PyPI](https://img.shields.io/pypi/v/softboxen.svg?maxAge=1800)](https://pypi.org/project/softboxen)
[![Python Versions](https://img.shields.io/pypi/pyversions/softboxen.svg)](https://pypi.org/project/softboxen/)
[![Build status](https://travis-ci.org/etingof/softboxen.svg?branch=master)](https://secure.travis-ci.org/etingof/softboxen)
[![Coverage Status](https://img.shields.io/codecov/c/github/etingof/softboxen.svg)](https://codecov.io/github/etingof/softboxen)
[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/etingof/softboxen/master/LICENSE.rst)

*This project is being in active development. Not quite usable yet, but worth evaluating!*

The goal of `softboxen` project is to simulate the presence of a large number
of network devices (such as switches, routers, modems etc) on the network.

These simulated devices expose their management interfaces and support
command-line dialogues in a reasonably convincing way. The main use-case
for `softboxen` is to create a testing environment for network management
and automation harness.

The system architecture being considered at the moment is this:

![system architecture](docs/arch.png)

## What's done

The project is being gradually developed. As of this time, the efforts have
been mostly focused on CLI pieces. This is what is more or less done:

* REST API client library that can also work against locally hosted JSON
  files.
* A CLI simulation framework (including models of simulated hardware) and
  simulation tool
* An example switch simulation extension package (`softboxen-example-switch`)
  that can be pip-installed and hooked up by the CLI simulation tool
* A tree of JSON files implementing an example network device

## What's not done yet:

* A more realistic CLI implementation to see what's missing in the framework
* Network transport endpoints (telnet, ssh etc.)to access simulated CLIs

On top of that, existing simulation data model will need to be extended
and refined as further development might prove.

## How to evaluate simulated example CLI

The easiest way to play with the example CLI (shipped along with main) distribution
as the `softboxen-example-switch`) is to run `example` tox job:

    $ tox -e example-cli
    
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

Alternatively, one could fire up `softboxen-restapi` server (that hosts
simulated network device models) and point `softboxen-cli` CLI frontend
to it.

## How to simulate a new box

Adding new network device involves creating one or more `CommandProcessor`
classes and Jinja2 templates.

### Command processor

Each command processor implements handling of the CLI commands at a single
nesting level. If you need to implement nesting (e.g. enable->configure), more
daisy chained `CommandProcessors` will be needed.

Individual commands take shape of `do_` or `do_not_` prefixed methods. Methods
are invoked in response to user-entered commands. When called, each method is
passed the entire backend model as a Python object. The method can inspect
and/or modify the model as desired.

See  softboxen-network-switch [CommandProcessor classes](https://github.com/etingof/softboxen/blob/master/examples/softboxen-example-switch/softboxen_example_switch/main.py#L12)
for inspiration.

### Command output

Jinja2 templates can be used to model CLI command responses. Some parts of the
response can be pasted as-is into the template file, while some pieces can be
substituted at runtime from device model properties or `CommandProcessor`
context.

By default, Jinja2 templates are organized in a directory tree reflecting
the nesting of the CLI commands. Individual templates residing in each
directory are used for rendering command output, some pre-defined templates
are invoked automatically:

* `on_enter.j2` - when entering this nesting level
* `on_exit.j2` - when leaving this nesting level
* `on_cycle.j2` - on each REPR cycle
* `on_error.j2` - on command execution failure

See softboxen-example-switch [templates](https://github.com/etingof/softboxen/tree/master/examples/softboxen-example-switch/softboxen_example_switch/templates/example/switch/1)
for more information.

### Simulation data

All simulation data should be ultimately hosted and managed by the REST API
server. While not implemented, and also to simplify development setup,
simulation data can be placed into a tree of JSON files.

A single, universal network device model is used for backing all flavors of
simulated devices. When instantiated, each model is tied to a specific CLI
frontend flavor (by means of `vendor`, `model` and `version` model attributes)
and represents a single specific network device identified by `uuid` attribute.

When CLI simulation tool is started, it should be given `uuid` to point to a
specific instance of a model. Once a model is found, CLI tool will try
to discover and load required CLI implementation by searching installed
extension modules by `vendor`, `model` and `version` model attributes.

Instantiating models and tying them up to a specific network device type
CLI simulation is thought to be done via admin interface of REST API.

See softboxen-example-switch [models](https://github.com/etingof/softboxen/tree/master/examples/models)
for more information.

## How to get softboxen

The softboxen package is distributed under terms and conditions of 2-clause
BSD [license](https://github.com/etingof/softboxen/LICENSE.rst). Source code is freely
available as a GitHub [repo](https://github.com/etingof/softboxen).

You could `pip install softboxen` or download it from [PyPI](https://pypi.org/project/softboxen).

If something does not work as expected, 
[open an issue](https://github.com/etingof/softboxen/issues) at GitHub.

Copyright (c) 2020, [Ilya Etingof](mailto:etingof@gmail.com). All rights reserved.
