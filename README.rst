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

For now, documentation is light and there are some things missing.

Features
--------

* read TSPLIB95 files
* supports all explicit edge weight formats
* supports all distance functions (except x-ray crystallography for now)
* convert problems into ``networkx.Graph`` instances
* CLI program to print a tabular summary of one or more TSPLIB95 files


Usage
-----

Loading problems and solutions is easy.

.. code-block:: python

    >>> import tsplib95
    >>>
    >>> problem = tsplib95.load_problem('ulysses16.tsp')

Both have the base attributes, but let's focus on a problem first:

.. code-block:: python

    >>> problem.name  # not specified
    >>> problem.comment
    'Odyssey of Ulysses (Groetschel/Padberg)'
    >>> problem.type
    'TSP'
    >>> problem.dimension
    16


Problems can be specified in several ways according to the TSPLIB_ format. Here's how this particular problem is specified:

.. code-block:: python

    >>> problem.display_data_type
    'COORD_DISPLAY'
    >>> problem.edge_data_format    # not specified
    >>> problem.edge_weight_format  # not specified
    >>> problem.edge_weight_type
    'GEO'
    >>> problem.node_coord_type     # not specified

Regardless of how the problem is specified, nodes and edges are accessible in the same way. Nodes and edges are returned as generators since there could be a significant number of them:

.. code-block:: python

    >>> list(problem.get_nodes())
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    >>> list(problem.get_edges())[:5]
    [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]

We can find the weight of the edge between nodes 1 and, say, 11, using ``wfunc``:

.. code-block:: python

    >>> problem.wfunc
    <function tsplib95.models.Problem._create_distance_function.<locals>.adapter>
    >>> problem.wfunc(1, 11)
    26

If the distance function for the problem is "SPECIAL" you must provide a custom distance function. The function must accept two node coordinates and return the distance between them. Let's create one:

.. code-block:: python

    >>> import random
    >>> import math
    >>>
    >>> def euclidean_2d_jitter(a, b):
    ...     x1, y1 = a
    ...     x2, y2 = b
    ...     dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    ...     return dist * random.random() * 2
    ...

Of course, you may want to leverage the existing distance functions:

.. code-block:: python

    >>> from tsplib95 import distances
    >>>
    >>> def euclidean_jitter(a, b):
    ...    dist = distances.euclidean(a, b)  # works for n-dimensions
    ...    return dist * random.random() * 2
    ...

You can either provide that function at load time or you can also set it on an existing ``Problem`` instance:

.. code-block:: python

    >>> problem = tsplib95.load_problem('example.tsp', special=euclidean_2d_jitter)
    >>> problem.special = euclidean_jitter

Note that setting the special function on a problem that has explicit edge weights has no effect.

You can get a ``networkx.Graph`` instance from the problem:

.. code-block:: python

    >>> G = problem.get_graph()
    >>> G.nodes
    NodeView((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16))

And you can trace the tours found in a ``Solution``:

.. code-block:: python

    >>> solution = tsplib95.load_solution('ulysses16.opt.tour')
    >>> problem.trace_tours(solution)
    [73]


Credits
-------

See TSPLIB_ for original details, including file format specification, C++ code, and sample problems.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _TSPLIB: https://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/index.html
