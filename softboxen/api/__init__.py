#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import os

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from softboxen.api import config


app = Flask(__name__)

app.url_map.strict_slashes = False

app.config.from_object(config.DefaultConfig)

if 'SOFTBOXEN_CONFIG' in os.environ:
    app.config.from_envvar('SOFTBOXEN_CONFIG')

db = SQLAlchemy(app)
ma = Marshmallow(app)
