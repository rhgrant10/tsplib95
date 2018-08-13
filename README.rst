=========
TSPLIB 95
=========


.. image:: https://img.shields.io/pypi/v/tsplib95.svg
        :target: https://pypi.python.org/pypi/tsplib95

.. image:: https://img.shields.io/travis/rhgrant10/tsplib95.svg
        :target: https://travis-ci.org/rhgrant10/tsplib95

.. image:: https://readthedocs.org/projects/tsplib95/badge/?version=latest
        :target: https://tsplib95.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


TSPLIB 95 is a library for working with TSPLIB 95 files.

* Free software: Apache Software License 2.0
* Documentation: https://tsplib95.readthedocs.io.

For now...

* documentation is not complete
* only 3.6 is supported (I am willing to remove f-strings if there is support; I might also spontaneously decide to do that)
* there are some things missing (being able to write out a TSPLIB file chief among them)

Features
--------

- read and use TSPLIB95 files like a boss
- easily convert problems into ``networkx.Graph`` instances
- supports and implements the following ``EDGE_WEIGHT_TYPE`` s

  - ``EXPLICIT``
  - ``EUC_2D``
  - ``EUC_3D``
  - ``MAX_2D``
  - ``MAX_3D``
  - ``MAN_2D``
  - ``MAN_3D``
  - ``CEIL_2D``
  - ``GEO``
  - ``ATT``
  - ``XRAY1``
  - ``XRAY2``

- supports the following ``EDGE_WEIGHT_FORMAT`` s

  - ``FULL_MATRIX``
  - ``UPPER_ROW``
  - ``LOWER_ROW``
  - ``UPPER_DIAG_ROW``
  - ``LOWER_DIAG_ROW``
  - ``UPPER_COL``
  - ``LOWER_COL``
  - ``UPPER_DIAG_COL``
  - ``LOWER_DIAG_COL``

- supports ``SPECIAL`` ``FUNCTION`` edge weights too

It also has a CLI program to print a tabular summary of one or more TSPLIB95 files. No idea why anyone would want that, but there you have it.


Credits
-------

See TSPLIB_ for original details, including file format specification, C++ code, and sample problems.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

.. _TSPLIB: https://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/index.html
