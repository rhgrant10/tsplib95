=====
Usage
=====

To use TSPLIB 95 in a project::

    import tsplib95


1. Problems
    A. Loading
        i. From file
        ii. From string
        iii. Using special
    B. Writing
        i. To file
        ii. To string
    C. Using
        i. Basic attributes
        ii. Nodes and edges
        iii. About wfunc
        iv. Extra attributes
        v. Tracing tours
    D. Converting
        i. Basics
        ii. Metadata
        iii. Symmetry
        iv. Normalization
2. Solutions
    A. Loading
        i. From file
        ii. From string
    B. Writing
        i. To file
        ii. To string
    C. Using
        i. Basic attributes
3. Miscellaneous
    A. Unknown files

Problems
========

.. note::

    **tsplib95** does not officially ship with any problem files itself. The problems
    and solutions are standalone files. ``load_problem`` and ``load_solution`` take a
    filesystem path as an argument, not the name of a problem. Feel free to download
    and use any of the original `TSPLIB problem files`_ commonly used and referenced
    by the community, find others, or write your own. Any file that adheres to the
    `TSPLIB95 file format standards`_ should load without error.

Loading
-------

Problems can be loaded either by specifying a filepath or providing raw text.

From file
~~~~~~~~~

For the simple case of a file on disk, pass the filepath to
:func:`tsplib95.utils.load_problem`:

.. code-block:: python

    >>> import os
    >>> import tsplib95
    >>> filepath = os.path.expanduser('~/tsp/bays29.tsp')
    >>> problem = tsplib95.utils.load_problem(filepath)

From string
~~~~~~~~~~~

For cases where the problem isn't stored as a file on disk, just pass the text
directly to :func:`tsplib95.utils.load_problem_fromstring`:

.. code-block:: python

    >>> from myapp import db
    >>> import tsplib95
    >>> text = db.load(name='bays29')
    >>> problem = tsplib95.load_problem_fromstring(text)

Using ``special``
~~~~~~~~~~~~~~~~~

Some problems involve using a custom function for calcating edge weights. Because
such a function is defined outside of the TSPLIB standard it is termed a "special"
weight function. Problems that use a special function have the following
characteristics:

* EDGE_WEIGHT_FORMAT is "FUNCTION"
* EDGE_WEIGHT_TYPE is "SPECIAL"

A special function can be provided during load time or it can be set on an existing
problem instance. The function must accept two node coordinates and return the
weight, distance, or cost of the edge between them. As a simple example, we could
create a special function that requests driving distance using Google Maps:

.. code-block:: python

    >>> from myapp import clients
    >>> import tsplib95
    >>> gmaps = clients.GMapClient()
    >>> def driving_distance(start, end):
    ...     start = dict(zip(['lat', 'lng'], start))
    ...     end = dict(zip(['lat', 'lng'], end))
    ...     kilometers = gmaps.get_driving_distance(start, end)
    ...     return kilometers
    ...
    >>> problem = tsplib95.utils.load_problem('my-hometown.tsp',
    ...                                       special=driving_distance)

.. note::

    The example above demonstrates the flexibility of the special function, but it's pretty
    rough around the edges depending on what happens inside ``gmaps.get_driving_distance``.
    There is no exception handling around the use of the special function so it is advisable
    to handle any exceptions. Depending on the use case, it may also be wise to decorate it
    with cache or debounce functions to avoid excessive API calls, for example.

Writing
-------

Currently, it is not possible to write a TSPLIB95 problem file back to disk nor to a string.

Using
-----

In general, familiarity with the original file format standard will translate well. Please
refer to it for additional details.


Specification attributes
^^^^^^^^^^^^^^^^^^^^^^^^

Just like the file format standard, problem instances have both specification and data attributes.
Put succinctly, the attributes of a problem instance are the lowercase versions of the file format
standard's keywords.

.. code-block:: python

    >>> import tsplib95
    >>> problem = tsplib95.utils.load_problem('hk48.tsp')
    >>> problem.name
    'hk48'
    >>> problem.type
    'TSP'
    >>> problem.dimension
    48
    >>> problem.comment
    '48-city problem (Held/Karp)'

Beyond the basic attributes, the file format provides a variety of ways to specify problems.
Several attributes describe the data format.

.. code-block:: python

    >>> import tsplib95
    >>> problem = tsplib95.utils.load_problem('hk48.tsp')
    >>> problem.edge_weight_type
    'EXPLICIT'
    >>> problem.edge_weight_format
    'LOWER_DIAG_ROW'
    >>> problem.edge_data_format
    >>> problem.node_coord_type
    >>> problem.display_data_type
    'NO_DISPLAY'

.. code-block:: python

    >>> problem = tsplib95.utils.load_problem('archives/problems/tsp/burma14.tsp')
    >>> problem.edge_weight_type
    'GEO'
    >>> problem.edge_weight_format
    'FUNCTION'
    >>> problem.edge_data_format
    >>> problem.node_coord_type
    >>> problem.display_data_type
    'COORD_DISPLAY'
 
Data attributes
^^^^^^^^^^^^^^^

The remaining attributes specify the actual data. Node coordinates and demands
are :class:`OrderedDict`s. The keys are the node names (integers, not necessarily
sequential nor starting at 0).

.. code-block:: python

    >>> import tsplib95
    >>> problem = tsplib95.utils.load_problem('eil22.vrp')
    >>> problem.node_coords
    OrderedDict([(1, (145.0, 215.0)),
                (2, (151.0, 264.0)),
                (3, (159.0, 261.0)),
                ...
                (20, (129.0, 189.0)),
                (21, (155.0, 185.0)),
                (22, (139.0, 182.0))])
    >>> problem.demands
    {1: 0,
     2: 1100,
     3: 700,
     ...
     20: 2500,
     21: 1800,
     22: 700}


Edge data is either an :class:`OrderedDict` or a :class:`list`, depending
on the edge data format.

.. code-block:: python

    >>> import tsplib95
    >>> problem = tsplib95.utils.load_problem('alb1000.hcp')
    >>> problem.edge_data
    [(1000, 593),
     (1000, 456),
     (1000, 217),
     ...
     (12, 9),
     (9, 1),
     (7, 2)]go


'node_coords': {},
'edge_weights': [10,
20,
25,
25,
20,
10,
12,
20,
25,
30,
20,
10,
11,
22,
30,
2,
11,
25,
10,
20,
12],
'display_data': {},
'edge_data': None,
'fixed_edges': set(),
}

Certain types of problems involve additional information, such as capacity, depots, demands,
and fixed edges.

.. code-block:: python

    >>> import tsplib95
    >>> problem = tsplib95.utils.load_problem('eil7.vrp')
    >>> problem.capacity
    3
    >>> problem.depots
    [1]
    >>> problem.demands
    {1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}
    >>> problem.fixed_edges
    set()

The problem above specifies capacity, depots, and demands, but it does not stipulate any fixed
edges. Here is a problem that specifies a single fixed edge:

.. code-block:: python

    >>> import tsplib95
    >>> problem = tsplib95.utils.load_problem('linhp318.tsp')
    >>> problem.capacity
    >>> problem.depots
    set()
    >>> problem.demands
    {}
    >>> problem.fixed_edges
    [(1, 214)]
        



Nodes and edges
~~~~~~~~~~~~~~~

About wfunc
~~~~~~~~~~~

Extra attributes
~~~~~~~~~~~~~~~~

Tracing tours
~~~~~~~~~~~~~


Converting
----------

Basics
~~~~~~

Metadata
~~~~~~~~

Symmetry
~~~~~~~~

Normalization
~~~~~~~~~~~~

Solutions
=========

Loading
-------

From file
~~~~~~~~~

From string
~~~~~~~~~~~

Writing
-------

It is currently not possible to write a TSPLIB95 Solution back to disk nor to string.

Using
-----

Basic attributes
~~~~~~~~~~~~~~~~

Miscellaneous
=============

Working with unknown files
--------------------------



Attributes
==========

Problems and solutions have various attributes. Both contain a common set
of basic metadata attributes:

.. code-block:: python

    >>> problem.name  # not specified
    >>> problem.comment
    'Odyssey of Ulysses (Groetschel/Padberg)'
    >>> problem.type
    'TSP'
    >>> problem.dimension
    16


Problems
--------

Specification
~~~~~~~~~~~~~

Problems can be specified in several ways according to the TSPLIB_ format.
Here's how this particular problem is specified:

.. code-block:: python

    >>> problem.display_data_type
    'COORD_DISPLAY'
    >>> problem.edge_data_format    # not specified
    >>> problem.edge_weight_format  # not specified
    >>> problem.edge_weight_type
    'GEO'
    >>> problem.node_coord_type     # not specified

Nodes and Edges
~~~~~~~~~~~~~~~

Regardless of how the problem is specified, nodes and edges are accessible
in the same way. Nodes and edges are returned as generators since there could
be a significant number of them:

.. code-block:: python

    >>> list(problem.get_nodes())
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    >>> list(problem.get_edges())[:5]
    [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]

Distances
~~~~~~~~~

We can find the weight of the edge between nodes 1 and, say, 11,
using ``wfunc``:

.. code-block:: python

    >>> problem.wfunc
    <function tsplib95.models.Problem._create_distance_function.<locals>.adapter>
    >>> problem.wfunc(1, 11)
    26

If the distance function for the problem is "SPECIAL" you must provide a
custom distance function. The function must accept two node coordinates
and return the distance between them. Let's create one:

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

You can either provide that function at load time or you can also set it on
an existing ``Problem`` instance:

.. code-block:: python

    >>> problem = tsplib95.load_problem('example.tsp', special=euclidean_2d_jitter)
    >>> problem.special = euclidean_jitter

Note that setting the special function on a problem that has explicit edge
weights has no effect.

You can get a ``networkx.Graph`` instance from the problem:

.. code-block:: python

    >>> G = problem.get_graph()
    >>> G.nodes
    NodeView((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16))

Solutions
---------

You can trace the tours found in a ``Solution``:

.. code-block:: python

    >>> solution = tsplib95.load_solution('ulysses16.opt.tour')
    >>> problem.trace_tours(solution)
    [73]

Note that it returns a list of tour distances, one for each tour defined in
the solution.

.. _TSPLIB: https://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/index.html
.. _TSPLIB problem files: https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/
.. _TSPLIB95 file format standards: https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf
