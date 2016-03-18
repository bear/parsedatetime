#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import codecs

from setuptools import setup, find_packages

cwd = os.path.abspath(os.path.dirname(__file__))

def read(filename):
    with codecs.open(os.path.join(cwd, filename), 'rb', 'utf-8') as h:
        return h.read()

metadata = read(os.path.join(cwd, 'parsedatetime', '__init__.py'))

def extract_metaitem(meta):
    # swiped from https://hynek.me 's attr package
    meta_match = re.search(r"""^__{meta}__\s+=\s+['\"]([^'\"]*)['\"]""".format(meta=meta),
                           metadata, re.MULTILINE)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError('Unable to find __{meta}__ string.'.format(meta=meta))

setup(
    name='parsedatetime',
    version=extract_metaitem('version'),
    author=extract_metaitem('author'),
    author_email=extract_metaitem('email'),
    url=extract_metaitem('url'),
    download_url=extract_metaitem('download_url'),
    description=extract_metaitem('description'),
    license=extract_metaitem('license'),
    packages=find_packages(exclude=['tests', 'docs']),
    platforms=['Any'],
    long_description=read('README.rst'),
    install_requires=['future'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Text Processing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
