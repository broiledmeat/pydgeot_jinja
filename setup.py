#!/usr/bin/env python3
from distutils.core import setup

setup(
    name='pydgeot_jinja',
    version='0.1',
    packages=['pydgeot.plugins.jinja'],
    requires=['pydgeot', 'jinja2'],
    url='https://github.com/broiledmeat/pydgeot_jinja',
    license='Apache License, Version 2.0',
    author='Derrick Staples',
    author_email='broiledmeat@gmail.com',
    description='Jinja2 support for Pydgeot.'
)
