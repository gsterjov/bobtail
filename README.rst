========
Overview
========

.. start-badges
.. end-badges

A dialogue system for NLP interpreters.

* Free software: MIT license

Installation
============

::

    pip install bobtail

Documentation
=============

https://bobtail.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
