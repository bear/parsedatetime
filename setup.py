import os

from setuptools import setup, find_packages
from parsedatetime import __version__

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(name='parsedatetime',
        version=__version__,
        author='Mike Taylor',
        author_email='bear@bear.im',
        url='http://github.com/bear/parsedatetime/',
        download_url='https://pypi.python.org/pypi/parsedatetime/',
        description='Parse human-readable date/time text.',
        license='Apache License 2.0',
        packages=find_packages(exclude=['tests*']),
        platforms=['Any'],
        long_description=(read('README.rst') + '\n\n' +
                          read('AUTHORS.txt') + '\n\n' +
                          read('CHANGES.txt')),
        classifiers=['Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: Apache Software License',
                     'Operating System :: OS Independent',
                     'Topic :: Text Processing',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.0',
                     'Programming Language :: Python :: 3.1',
                     'Programming Language :: Python :: 3.2',
                     'Programming Language :: Python :: 3.3',
                     'Programming Language :: Python :: 3.4',
                    ]
    )
