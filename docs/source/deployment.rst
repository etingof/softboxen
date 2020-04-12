
.. _deployment:

Deployment
----------

This is a overview of a typical Softboxen deployment just to give you some
inspiration. This is not a step-by-step instructions.

Installation
++++++++++++

For production use, install Softboxen core along with the CLI implementation
packages for the devices you want to emulate:

.. code-block:: bash

   # Older setuptools may not work with versioned dependencies
   pip install setuptools -U

   pip install softboxen  # softboxen core
   pip install softboxen-example-switch  # vendor 'example', model 'switch' 

It's better to run softboxen components under a non-privileged user and group
(e.g. `softboxen`).

.. code-block:: bash

    su softboxen
    mkdir -p /etc/softboxen /var/run/softboxen /var/softboxen

Configuration files
+++++++++++++++++++

Create a configuration file for REST API server:

.. code-block:: bash

    cat > /etc/softboxen/softboxen.conf << EOF
    SQLALCHEMY_DATABASE_URI = 'sqlite:////var/softboxen/softboxen-restapi.db'
    DEBUG = False
    SOFTBOXEN_LISTEN_IP = '127.0.0.1'
    SOFTBOXEN_LISTEN_PORT = 5000
    SOFTBOXEN_SSL_CERT = None
    SOFTBOXEN_SSL_KEY = None
    EOF

Bootstrap underlying database:

.. code-block:: bash

    softboxen-restapi --config /etc/softboxen/softboxen.conf \
        --recreate-db

REST API server
+++++++++++++++

To bring up REST API server, just follow WSGI application setup guidelines.

For example, for `gunicorn <https://gunicorn.org>`_:

.. code-block:: bash

    pip install gunicorn

    gunicorn -b 127.0.0.1:5000 \
       --env "SOFTBOXEN_CONFIG=/etc/softboxen/softboxen.conf" \
      --access-logfile /var/log/softboxen/softboxen-access.log \
      --error-logfile /var/log/softboxen/softboxen-error.log  \
      --daemon \
      softboxen.wsgi:app

Initial models
++++++++++++++

For CLI device emulation to work, a model needs to be created in the database,
and specific CLI implementation package has to be installed on the system.

To create device model, a series of REST API calls have to be performed. The
following call creates a network device model for vendor "example", model
"switch" and version "1".

.. code-block:: bash

    req='{
      "vendor": "example",
      "model": "switch",
      "version": "1",
    }'
    curl -d "$req" \
        -H "Content-Type: application/json" \
        -X POST \
        http://localhost:5000/softboxen/v1/boxen

Box ID and UUID will be automatically assigned to the new model. Then one
or more network ports can be added to the model (assuming box ID is `1`:

.. code-block:: bash

    req='{
      "name": "1/16",
      "speed": "1G",
    }'
    curl -d "$req" \
        -H "Content-Type: application/json" \
        -X POST \
        http://localhost:5000/softboxen/v1/boxen/1/ports

Likewise other resources can be created and associated with models.

.. note::

    It is in the project's TODO list to create a command-line admin tool
    for models management.

CLI implementation packages
+++++++++++++++++++++++++++

Once the UUID of the model is passed to the CLI frontend tool, it
will learn the vendor, model and version identifiers. Based on that, CLI
frontend will try to locate matching CLI implementation among installed
Python packages and use it.

.. code-block:: bash

    $ softboxen-cli --service-root http://127.0.0.1:5000/softboxen/v1 \
        --box-uuid 123e4567-e89b-12d3-a456-426655440000

To see which CLI implementation packages are presently installed, the user can
run `softboxen-cli --list-clis` command:

.. code-block:: bash

    $ softboxen-cli  --list-clis
    Vendor cisco, model 5300, version 12.1
    Vendor Zyxel, model DSL-630, version 1.1
    Vendor Juniper, model EX-4500, version 5.1

Particular CLI implementation package can be pip-installed like any regular
Python package:

.. code-block:: bash

    pip install softboxen-example-switch


