import os

from setuptools import setup, find_packages

__author__ = 'Mike Taylor (bear@bear.im)'
__copyright__ = 'Copyright (c) 2004 Mike Taylor'
__license__ = 'Apache v2.0'
__version__ = '2.0'
__contributors__ = ['Darshana Chhajed',
                    'Michael Lim (lim.ck.michael@gmail.com)',
                    'Bernd Zeimetz (bzed@debian.org)']


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


def read_lines(path):
    with open(path, 'r') as fio:
        return fio.readlines()


setup(
    name='parsedatetime',
    version=__version__,
    author='Mike Taylor',
    author_email='bear@bear.im',
    url='http://github.com/bear/parsedatetime/',
    download_url='https://pypi.python.org/pypi/parsedatetime/',
    description='Parse human-readable date/time text.',
    license='Apache License 2.0',
    packages=find_packages(exclude=['tests*']),
    platforms=['Any'],
    install_requires=read_lines('requirements.txt'),
    long_description=(read('README.rst')),
    test_suite='nose.collector',
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
