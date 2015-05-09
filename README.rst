parsedatetime

Parse human-readable date/time strings.

Python 2.7 or greater is required for parsedatetime version 1.0 or greater.

.. image:: https://pypip.in/wheel/parsedatetime/badge.png
    :target: https://pypi.python.org/pypi/parsedatetime/
    :alt: Wheel Status

.. image:: https://travis-ci.org/bear/parsedatetime.svg?branch=master
    :target: https://travis-ci.org/bear/parsedatetime
    :alt: Travis CI

==========
Installing
==========

You can install parsedatetime using::

    pip install parsedatetime

=============
Running Tests
=============

From the source directory::

    python run_tests.py parsedatetime

To run tests on several python versions, type ``tox``::

  $ tox
  [... tox creates a virtualenv for every python version and runs tests inside of each]
  py27: commands succeeded
  py33: commands succeeded
  py34: commands succeeded

This assumes that you have ``python2.7``, ``python3.4``, etc in ``PATH``.

===================
Using parsedatetime
===================

An example of how to use parsedatetime::

    import parsedatetime

    cal = parsedatetime.Calendar()

    cal.parse("tomorrow")

More detailed examples can be found in the examples directory.

=============
Documentation
=============

The generated documentation is included by default in the docs directory and can also be viewed online at https://bear.im/code/parsedatetime/docs/index.html

The docs can be generated using either of the two commands::

    python setup.py doc
    epydoc --html --config epydoc.conf

=====
Notes
=====

The ``Calendar`` class has a member property named ``ptc`` which is created during the class init method to be an instance
of ``parsedatetime_consts.CalendarConstants()``.

=======
History
=======

The code in parsedatetime has been implemented over the years in many different languages (C, Clipper, Delphi) as part of different custom/proprietary systems I've worked on.  Sadly the previous code is not "open" in any sense of that word.

When I went to work for Open Source Applications Foundation and realized that the Chandler project could benefit from my experience with parsing of date/time text I decided to start from scratch and implement the code using Python and make it truly open.

After working on the initial concept and creating something that could be shown to the Chandler folks the code has now evolved to it's current state with the help the Chandler folks, most especially Darshana.
