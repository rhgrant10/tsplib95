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




TSPLIB 95 works with TSPLIB 95 files. See TSPLIB_ for original details, including file format specification, CPP code, and sample problems.


* Free software: Apache Software License 2.0
* Documentation: https://tsplib95.readthedocs.io.


Features
--------

* read TSPLIB95 file format into a dictionary
* supports all explicit edge weight formats
* supports all distance functions (except x-ray crystallography for now)
* convert problems into ``networkx.Graph`` instances
* CLI program to print a tabular summary of one or more TSPLIB95 files

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _TSPLIB: https://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/index.html
