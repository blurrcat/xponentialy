#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='xponentialy',
    version='0.1.0',
    description='Fit it!',
    long_description=readme + '\n\n' + history,
    author='Harry Liang',
    author_email='blurrcat@gmail.com',
    url='https://github.com/blurrcat/xponentialy',
    packages=[
        'xponentialy',
    ],
    package_dir={'xponentialy': 'xponentialy'},
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-WTF',
        'Flask-Admin',
        'Flask-SQLAlchemy',
        'Flask-Restless',
        'PyMySQL',
    ],
    license="BSD",
    zip_safe=False,
    keywords='xponentialy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
