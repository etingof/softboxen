
New device emulation
--------------------

The only thing that's required to add new device type emulation is to create
and install the CLI implementation package for the new device.

A reference CLI implementation package is
`included <https://github.com/etingof/softboxen/tree/master/examples/softboxen-example-switch>`_
in the `softboxen` package.

It is advisable to create `softboxen` implementation packages for every distinct
vendor and/or model and/or version (depending on code reuse possibilities), and
release these packages on PyPI for public consumption.

.. note::

    It is in project's TODO list to create a `quickstart` tool for creating
    a wireframe of CLI implementation package.

CLI entry points
++++++++++++++++

The CLI implementation package can be a regular pip-installable Python
package exposing specific
`entry point(s) <https://packaging.python.org/guides/creating-and-discovering-plugins/#using-package-metadata>`_,
as package metadata, that `softboxen` core will be looking up. Softboxen relies
on `setuptools <https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins>`_
plugin registration for plugin discovery.

Practically, CLI implementation package should have something like this in its
`setup.py`:

.. code-block:: python

    'entry_points': {
        'softboxen.cli': 'example.switch.1 = softboxen_example_switch'
                         '.main:PreLoginCommandProcessor'
    }


Where:

* `softboxen.cli` is softboxen plugin namespace
* `example.switch.1` string should be a unique, plugin-specific string. This
  information is not used for model matching
* `softboxen_example_switch.main:PreLoginCommandProcessor` is a path to the
  top-level softboxen `command processor` class that implements initial CLI
  dialogue

Command processor class
+++++++++++++++++++++++

Softboxen `command processor <https://github.com/etingof/softboxen/blob/master/softboxen/cli/base.py#L27>`_
is a base class that implements CLI `REPR <https://en.wikipedia.org/wiki/Read–eval–print_loop>`_
loop. As a REPR loop, `command processor` operates along these guidelines:

* Read CLI user input on `stdin` up to <CR>
* Parse user input and try to match it against any known commands, otherwise
  default handler will be picked
* Apply user command to the emulated device model (fetched from REST API server
  by `softboxen` core)
* Locate appropriate Jinja2 template and render it in the context emulated
  device model

... or

* If this command results in moving down the CLI menu tree, create another
  `command processor` object for the submenu and invoke its own `REPR` loop

Typical CLI implementation package will have one or more daisy-chained
`command processor` objects. The first, top-level, object will handle the
initial user interaction. In the example CLI implementation, the first
`PreLoginCommandProcessor <https://github.com/etingof/softboxen/blob/master/examples/softboxen-example-switch/softboxen_example_switch/main.py#L31>`_
is responsible for "login:" prompt rendering and user name string collection.

The top-level `command processor` class should define `VENDOR`, `MODEL` and
`VERSION` attributes. They are used by Softboxen core for matching CLI against
the model at hand.

.. code-block:: python

    class BaseCommandProcessor(base.CommandProcessor):
        """Create CLI REPR loop for example switch."""

        VENDOR = 'example'
        MODEL = 'switch'
        VERSION = '1'

Chaining command processors
+++++++++++++++++++++++++++

When a command processor needs to go down one menu level, the way to represent
it programmatically is to create a sub-processor. The `_create_subprocessor`
helper function is advised to use.

The new `command processor` will
`inherit <https://github.com/etingof/softboxen/blob/master/softboxen/cli/base.py#L137>`_
model and I/O streams from its parent, the user should only supply the new
"scope" for the template tree:

.. code-block:: python

    subprocessor = self._create_subprocessor(
        UserViewCommandProcessor, 'login', 'mainloop')

Template tree
+++++++++++++

It is advisable to arrange Jinja2 templates, that command processors use for
CLI dialog rendering, in a tree on the file system. The main reason for that
is that `softboxen` core treats some templates in special ways.

To date, the following template file names receive special treatment (if
exist):

* `on_enter.j2` - render this template on command processor entering into
  this directory
* `on_exit.j2` - render this template before command processor leaves this
  directory
* `on_cycle.j2` - render this template upon every <CR> received in the REPR
  loop
* `on_error.j2` - render this template on any error that occurs in the
  command processor while handling the command

Please, refer to
`example switch CLI <https://github.com/etingof/softboxen/tree/master/examples/softboxen-example-switch/softboxen_example_switch/templates/example/switch/1>`_
for further inspiration.

Command handling
++++++++++++++++

In response to user input, the REPR loop in every `command processor` will
try to locate a method name starting with the `on_` prefix followed by the
longest substring of the user input.

If found, this method will be called and all further command processing should
happen there. If no matching method is found, the magic `on_unknown_command`
method will be invoked instead (if defined).

.. code-block:: python

    def do_enable(self, command, *args, context=None):

        subprocessor = self._create_subprocessor(
            EnableCommandProcessor, 'login', 'mainloop', 'enable')

        subprocessor.loop(context=context, raise_on_exit=False)


Parsing user input
~~~~~~~~~~~~~~~~~~

CLI commands are frequently composed of a series of instructions interlaced
with references to device properties. For example:

.. code-block:: bash

    $ show interface status ethernet 1/16

Where `1/16` is NIC ID, while the rest are command instructions.

To simplify command parsing, the
`_dissect <https://github.com/etingof/softboxen/blob/master/softboxen/cli/base.py#L206>`_
method can be used:

.. code-block:: python

    port_name, = self._dissect(
        args, 'interface', 'status', 'ethernet', str)

This method expects the instructions in the literal form and Python types
(e.g. `str`) in place of the options.

Operating on model properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every `command processor` object is passed a model of the emulated device as
received from the REST API server (or local JSON files). Command handler in
the `command processor` can create/read/update/delete model properties what
will eventually be reflected on the models maintained by the REST API server.

Generally, reading model attribute can be done just like `port.name`, however
attribute creation/update/deletion typically requires a method call on the
model.

For example, to handle CLI command like:

.. code-block:: bash

    $ switchport allowed vlan add 1 tagged

The `port.add_access_vlan` method would be called:

.. code-block:: python

    def do_switchport(self, command, *args, context=None):
        vlan_name, = self._dissect(
            args, 'allowed', 'vlan', 'add', str, 'tagged')

        port = context.pop('port')

        port.add_access_vlan(name=vlan_name)


.. note::

    To date, no update and delete operations are implemented.
