from distutils.core import setup

VERSION = '1.0.0'
desc    = """Parse human-readable date/time text.
Python 2.6+ is required for parsedatetime v1.+
The simple example of how to use parsedatetime is:

    import parsedatetime as pdt

    cal = pdt.Calendar()

    cal.parse("tomorrow")

More detailed examples can be found in the examples
directory.
"""

setup(name='parsedatetime',
        version=VERSION, 
        author='Mike Taylor',
        author_email='bear@code-bear.com',
        url='http://code-bear.com/code/parsedatetime/',
        download_url='http://code-bear.com/code/parsedatetime/parsedatetime-%s.tar.gz' % VERSION,
        description='Parse human-readable date/time text.',
        license='http://www.apache.org/licenses/LICENSE-2.0',
        packages=['parsedatetime'],
        platforms=['Any'],
        long_description=desc,
        classifiers=['Development Status :: 5 - Production/Stable',
                     'Environment :: Library',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: Apache Software License',
                     'Operating System :: OS Independent',
                     'Topic :: Text Processing',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Programming Language :: Python :: 2.5',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.0',
                     'Programming Language :: Python :: 3.1',
                     'Programming Language :: Python :: 3.2',
                    ]
        )

