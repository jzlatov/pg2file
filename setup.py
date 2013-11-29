#!/usr/bin/env python
# -*- coding: utf8 -*-

import os

import multiprocessing

try:
    from setuptools import setup, Extension, Command
except ImportError:
    from distutils.core import setup, Extension, Command

dependencies = ['sqlalchemy', 'psycopg2']

setup(
    name='pg2file',
    version='0.1.0',
    description="pg2file save PostgreSQL database objects to separate files.",
    long_description=open('README.rst').read(),
    author='Jiří Zlatov',
    author_email='jiri.zlatov@gmail.com',
    url='https://plus.google.com/+Ji%C5%99%C3%ADZlatov/',
    packages=['pg2file'],
    scripts=['scripts/runpg2file'],
    license='MIT',
    install_requires=dependencies,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Utilities'
    ]
)