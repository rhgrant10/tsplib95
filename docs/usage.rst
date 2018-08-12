=====
Usage
=====

To use TSPLIB 95 in a project::

    import tsplib95


Loading problems and solutions is easy:

.. code-block:: python

    >>> problem = tsplib95.load_problem('ulysses16.tsp')
    >>> problem
    <tsplib95.models.Problem at 0x105030d30>
    >>> solution = tsplib95.load_solution('ulysses16.opt.tour')
    >>> solution
    <tsplib95.models.Solution at 0x104314d68>


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

Note that it returns a list of tour distances, one for each tour defined in the solution.

.. _TSPLIB: https://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/index.html