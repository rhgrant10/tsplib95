=========
TSPLIB 95
=========


.. image:: https://img.shields.io/pypi/v/tsplib95.svg
        :target: https://pypi.python.org/pypi/tsplib95
        :alt: Available on PyPI

.. image:: https://img.shields.io/travis/rhgrant10/tsplib95.svg
        :target: https://travis-ci.org/rhgrant10/tsplib95
        :alt: Continuous Integration

.. image:: https://codecov.io/gh/rhgrant10/tsplib95/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/rhgrant10/tsplib95
        :alt: Code Coverage

.. image:: https://readthedocs.org/projects/tsplib95/badge/?version=latest
        :target: https://tsplib95.readthedocs.io/?badge=latest
        :alt: Documentation Status



TSPLIB 95 is a library for working with TSPLIB 95 files.

* Free software: Apache Software License 2.0
* Documentation: https://tsplib95.readthedocs.io.

Features
--------

- **read** and **write** TSPLIB95 file format like a boss
- easily **convert** problems into ``networkx.Graph`` instances
- supports **all** fields in the original standard
- allows completely **custom** field and problem declarations

It also has a CLI program to print a tabular summary of one or more TSPLIB95
files... no idea why anyone would want that, but there you have it nonetheless.


Credits
-------

See TSPLIB_ for original details, including file format specification, C++ code, and sample problems.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

.. _TSPLIB: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/

