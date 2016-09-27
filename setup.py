#!/usr/bin/env python3
from distutils.core import setup


setup(
    name='pydgeot_jinja',
    description='Jinja2 support for Pydgeot.',
    url='https://github.com/broiledmeat/pydgeot_jinja',
    license='Apache License, Version 2.0',
    author='Derrick Staples',
    author_email='broiledmeat@gmail.com',
    version='0.5',
    packages=['pydgeot.plugins.jinja'],
    requires=['pydgeot', 'jinja2'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup'
    ]
)
