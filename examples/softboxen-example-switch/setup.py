#!/usr/bin/env python
#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#
import os
import unittest

import setuptools

CLASSIFIERS = """\
Development Status :: 3 - Alpha
Environment :: Console
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Information Technology
Intended Audience :: System Administrators
Intended Audience :: Telecommunications Industry
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Communications
Topic :: Software Development :: Libraries :: Python Modules
"""


class PyTest(setuptools.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        suite = unittest.TestLoader().loadTestsFromNames(
            ['tests.__main__.suite']
        )

        unittest.TextTestRunner(verbosity=2).run(suite)


with open('requirements.txt') as fl:
    requires = fl.read()

params = {
    'install_requires': requires,
    'name': 'softboxen-example-switch',
    'version': open(
        os.path.join(
            'softboxen_example_switch', '__init__.py')).read().split('\'')[1],
    'description': 'Example network switch for softboxen network equipment '
                   'simulator',
    'long_description': 'Example network switch extension module for Softboxen '
                        'network equipment simulation suite.',
    'maintainer': 'Ilya Etingof <etingof@gmail.com>',
    'author': 'Ilya Etingof',
    'author_email': 'etingof@gmail.com',
    'url': 'https://github.com/etingof/softboxen',
    'platforms': ['any'],
    'classifiers': [x for x in CLASSIFIERS.split('\n') if x],
    'license': 'BSD',
    'packages': setuptools.find_packages(),
    'entry_points': {
        'softboxen.cli': 'example.switch.1 = softboxen_example_switch.main:PreLoginCommandProcessor'
    },
    'cmdclass': {
        'test': PyTest,
        'tests': PyTest
    },
    'zip_safe': True
}

setuptools.setup(**params)
