=====
Usage
=====

To use TSPLIB 95 in a project::

    >>> import tsplib95

.. note::

    **tsplib95** does not officially ship with any problem files itself. The
    problems and solutions are standalone files. Feel free to download and use
    any of the original `TSPLIB problem files`_ commonly used and referenced by
    the community, find others, or write your own. Any file that adheres to the
    `TSPLIB95 file format standards`_ should load without error.


Loading problems
================

Problems can be loaded from files, read from file pointers, or parsed from strings.

- :func:`tsplib95.load() <tsplib95.loaders.load>`: loads from a filepath
- :func:`tsplib95.parse() <tsplib95.loaders.parse>`: parses directly from a string
- :func:`tsplib95.read() <tsplib95.loaders.read>`: reads from a file-like object


From a filepath
---------------

For the simple case of a file on disk, pass the filepath to
:func:`tsplib95.load`:

.. code-block:: python

    >>> import tsplib95
    >>> problem = tsplib95.load('archives/problems/tsp/bay29.tsp')


From a string
-------------

For cases where the problem isn't stored as a file on disk, just pass the text
directly to :func:`tsplib95.parse`:

.. code-block:: python

    >>> import tsplib95
    >>> with open('archives/problems/tsp/gr17.tsp') as f:
    ...     text = f.read()
    ...
    >>> problem = tsplib95.parse(text)


From a file-like object
-----------------------

If you already have an open file-like object, just pass it to :func:`tsplib95.read`:

.. code-block:: python

    >>> import tsplib95
    >>> with open('archives/problems/tsp/gr17.tsp') as f:
    ...     problem = tsplib95.read(f)
    ...


.. _special-functions-label:

SPECIAL functions
-----------------

What's a SPECIAL function?
~~~~~~~~~~~~~~~~~~~~~~~~~~

Some problems involve using a custom function for calcating edge weights. Such custom
weight functions are called "special" functions because their details are not defined
by TSPLIB95 standard.

Problems that use a special function have the following characteristics:

* EDGE_WEIGHT_FORMAT is "FUNCTION"
* EDGE_WEIGHT_TYPE is "SPECIAL"

In `tsplib95`, a special function must accept two node coordinates and return the
weight, distance, or cost of the edge between them::

    from typing import Union, Sequence

    def special(start: Sequence, end: Sequence) -> Union[float,int]:
        pass

How to use
~~~~~~~~~~

All loaders (:func:`~tsplib95.loaders.load`, :func:`~tsplib95.loaders.read`, and
:func:`~tsplib95.loaders.parse`) accept a custom weight function via the keyword
parameter `special`.

.. code-block:: python

    >>> import tsplib95
    >>> from myapp import get_distance
    >>> problem = tsplib95.load('assets/tsp/routes-150.tsp',
    ...                         special=get_distance)

Special functions can also be set on an existing problem instance:

.. code-block:: python

    >>> import tsplib95
    >>> from myapp import get_distance
    >>> problem = tsplib95.load('assets/tsp/routes-150.tsp')
    >>> problem.special = get_distance

Note that setting the special function on a problem that has explicit edge
weights has no effect.


An example
~~~~~~~~~~

Let's assume our app has a helper function capable of using the Google Maps API to
fetch the driving distance between two geocoordinates. We can use that to create a
special function and use it as the distance function in a TSPLIB95 problem.

Let's also assume our hypothetical helper function accepts a list of waypoints as
dictionaries with "lat" and "lng" keys, but our problem specifies geocoordinates as
a simple tuple of latitude and longitude values.

Our special function will need to convert the tuples into the expected dictionaries
and use the helper to calculate the driving distance.

.. code-block:: python

    >>> from myapp import helpers

    >>> def waypoint(coordinates):
    ...     return {'lat': coordinates[0], 'lng': coordinates[1]}

    >>> def driving_distance(start, end):
    ...     """Special distance function for driving distance."""
    ...     waypoints = [waypoint(start), waypoint(end)]
    ...     kilometers = helpers.total_distance(waypoints, method='driving')
    ...     return kilometers
    ...

Now we can simply supply the
:func:`tsplib95.load <tsplib95.loaders.load_problem>` method with our special
function:

.. code-block:: python

    >>> import tsplib95
    >>> problem = tsplib95.load('my-hometown.tsp', special=driving_distance)

As with any problem, we can find the weight of any edge using the
:func:`~tsplib95.models.StandardProblem.get_weight` method. See the
:ref:`distances-label` section for more details.

.. note::

    The example above demonstrates the flexibility of the special function, but
    depending on the specific implementation details of the helper function, it
    could be too fragile.

    There is no exception handling around the use of the special function so it
    is advisable to handle any exceptions. Depending on the use case, it may also
    be wise to limit calls to it by wrapping it in a debounce function or backing
    it with a cache.


Saving problems
===============

The :class:`Problem` class also two convenience methods for output to files:

- :func:`Problem.save <tsplib95.models.Problem.save>`: saves to a filepath
- :func:`Problem.write <tsplib95.models.Problem.write>`: writes to a file-like object

.. code-block:: python

    >>> problem.save('path/to/file.name')

    >>> with open('path/to/other.name', 'w') as f:
    ...     problem.write(f)
    ... 


Rendering problems
==================

Problems can be rendered back into text using the
:func:`Problem.render <tsplib95.models.Problem.render>` method:

.. code-block:: python

    >>> print(problem.render())
    NAME: gr17
    COMMENT: 17-city problem (Groetschel)
    TYPE: TSP
    DIMENSION: 17
    EDGE_WEIGHT_TYPE: EXPLICIT
    EDGE_WEIGHT_FORMAT: LOWER_DIAG_ROW
    EDGE_WEIGHT_SECTION:
    0 633 0 257 390 0 91 661 228 0 412 227
    169 383 0 150 488 112 120 267 0 80 572 196
    77 351 63 0 134 530 154 105 309 34 29 0
    259 555 372 175 338 264 232 249 0 505 289 262
    476 196 360 444 402 495 0 353 282 110 324 61
    208 292 250 352 154 0 324 638 437 240 421 329
    297 314 95 578 435 0 70 567 191 27 346 83
    47 68 189 439 287 254 0 211 466 74 182 243
    105 150 108 326 336 184 391 145 0 268 420 53
    239 199 123 207 165 383 240 140 448 202 57 0
    246 745 472 237 528 364 332 349 202 685 542 157
    289 426 483 0 121 518 142 84 297 35 29 36
    236 390 238 301 55 96 153 336 0
    EOF

Note this is equivalent to casting the problem to a string:

.. code-block:: python

    >>> assert str(problem) == problem.render()


Working with problems
=====================

.. note::

    In general, familiarity with the original file format standard will translate
    well. Please refer to it for an better understanding of the underlying TSPLIB95
    file format.

Accessing Values
----------------

In general, the name of a field is its keyword converted to lowercase. For example,
"NAME" is ``name`` and "EDGE_WEIGHT_FORMAT" is ``edge_weight_format``, *etc.*:

.. code-block:: python

    >>> problem.name  # NAME
    'gr17'
    >>> problem.edge_weight_format  # EDGE_WEIGHT_FORMAT
    'LOWER_DIAG_ROW'

However, field names do *not* have the "_SECTION" suffix of some keywords:

    >>> problem.edge_weights  # not EDGE_WEIGHT_SECTION
    [[0, 633, 0, 257, 390, 0, 91, 661, 228, 0, 412, 227],
     [169, 383, 0, 150, 488, 112, 120, 267, 0, 80, 572, 196],
     [77, 351, 63, 0, 134, 530, 154, 105, 309, 34, 29, 0],
     [259, 555, 372, 175, 338, 264, 232, 249, 0, 505, 289, 262],
     [476, 196, 360, 444, 402, 495, 0, 353, 282, 110, 324, 61],
     [208, 292, 250, 352, 154, 0, 324, 638, 437, 240, 421, 329],
     [297, 314, 95, 578, 435, 0, 70, 567, 191, 27, 346, 83],
     [47, 68, 189, 439, 287, 254, 0, 211, 466, 74, 182, 243],
     [105, 150, 108, 326, 336, 184, 391, 145, 0, 268, 420, 53],
     [239, 199, 123, 207, 165, 383, 240, 140, 448, 202, 57, 0],
     [246, 745, 472, 237, 528, 364, 332, 349, 202, 685, 542, 157],
     [289, 426, 483, 0, 121, 518, 142, 84, 297, 35, 29, 36],
     [236, 390, 238, 301, 55, 96, 153, 336, 0]]

All values are available mapped either by keyword or name:

.. code-block:: python

    >>> problem.as_name_dict()
    {'name': 'gr17',
     'comment': '17-city problem (Groetschel)',
     'type': 'TSP',
     'dimension': 17,
     'capacity': 0,
     'node_coord_type': None,
     'edge_weight_type': 'EXPLICIT',
     'display_data_type': None,
     'edge_weight_format': 'LOWER_DIAG_ROW',
     'edge_data_format': None,
     'node_coords': {},
     'edge_data': {},
     'edge_weights': [[0, 633, 0, 257, 390, 0, 91, 661, 228, 0, 412, 227],
      [169, 383, 0, 150, 488, 112, 120, 267, 0, 80, 572, 196],
      [77, 351, 63, 0, 134, 530, 154, 105, 309, 34, 29, 0],
      [259, 555, 372, 175, 338, 264, 232, 249, 0, 505, 289, 262],
      [476, 196, 360, 444, 402, 495, 0, 353, 282, 110, 324, 61],
      [208, 292, 250, 352, 154, 0, 324, 638, 437, 240, 421, 329],
      [297, 314, 95, 578, 435, 0, 70, 567, 191, 27, 346, 83],
      [47, 68, 189, 439, 287, 254, 0, 211, 466, 74, 182, 243],
      [105, 150, 108, 326, 336, 184, 391, 145, 0, 268, 420, 53],
      [239, 199, 123, 207, 165, 383, 240, 140, 448, 202, 57, 0],
      [246, 745, 472, 237, 528, 364, 332, 349, 202, 685, 542, 157],
      [289, 426, 483, 0, 121, 518, 142, 84, 297, 35, 29, 36],
      [236, 390, 238, 301, 55, 96, 153, 336, 0]],
     'display_data': {},
     'fixed_edges': [],
     'depots': [],
     'demands': {},
     'tours': []}

    >>> problem.as_keyword_dict()
    {'NAME': 'gr17',
     'COMMENT': '17-city problem (Groetschel)',
     'TYPE': 'TSP',
     'DIMENSION': 17,
     'CAPACITY': 0,
     'NODE_COORD_TYPE': None,
     'EDGE_WEIGHT_TYPE': 'EXPLICIT',
     'DISPLAY_DATA_TYPE': None,
     'EDGE_WEIGHT_FORMAT': 'LOWER_DIAG_ROW',
     'EDGE_DATA_FORMAT': None,
     'NODE_COORD_SECTION': {},
     'EDGE_DATA_SECTION': {},
     'EDGE_WEIGHT_SECTION': [[0, 633, 0, 257, 390, 0, 91, 661, 228, 0, 412, 227],
      [169, 383, 0, 150, 488, 112, 120, 267, 0, 80, 572, 196],
      [77, 351, 63, 0, 134, 530, 154, 105, 309, 34, 29, 0],
      [259, 555, 372, 175, 338, 264, 232, 249, 0, 505, 289, 262],
      [476, 196, 360, 444, 402, 495, 0, 353, 282, 110, 324, 61],
      [208, 292, 250, 352, 154, 0, 324, 638, 437, 240, 421, 329],
      [297, 314, 95, 578, 435, 0, 70, 567, 191, 27, 346, 83],
      [47, 68, 189, 439, 287, 254, 0, 211, 466, 74, 182, 243],
      [105, 150, 108, 326, 336, 184, 391, 145, 0, 268, 420, 53],
      [239, 199, 123, 207, 165, 383, 240, 140, 448, 202, 57, 0],
      [246, 745, 472, 237, 528, 364, 332, 349, 202, 685, 542, 157],
      [289, 426, 483, 0, 121, 518, 142, 84, 297, 35, 29, 36],
      [236, 390, 238, 301, 55, 96, 153, 336, 0]],
     'DISPLAY_DATA_SECTION': {},
     'FIXED_EDGES_SECTION': [],
     'DEPOT_SECTION': [],
     'DEMAND_SECTION': {},
     'TOUR_SECTION': []}


Nodes and edges
---------------

To help users avoid the complexity in listing the nodes and edges reliably in all
cases, there exists the :func:`~tsplib95.models.StandardProblem.get_nodes` and 
:func:`~tsplib95.models.StandardProblem.get_edges` methods.

.. code-block:: python

    >>> list(problem.get_nodes())
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

    >>> len(list(problem.get_edges()))  # I'll spare you the full listing :P
    289

    >>> list(problem.get_edges())[0]
    (0, 0)

.. _distances-label:

Distances
---------

Regardless of whether the problem is explicit or function, the distance between
two nodes can always be found by passing their indicies to
:func:`~tsplib95.models.Problem.get_weight`.

.. code-block:: python

    >>> problem = tsplib95.load('archives/problems/vrp/eil22.vrp')
    >>> list(problem.get_nodes())
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    >>> problem.node_coords[3]
    [159, 261]
    >>> problem.node_coords[8]
    [161, 242]
    >>> problem.edge_weight_type
    'EUC_2D'
    >>> edge = 3, 8
    >>> weight = problem.get_weight(*edge)
    >>> print(f'The driving distance from node {edge[0]} to node {edge[1]} is {weight}.')
    The distance between node 3 and node 8 is 19.

``tsplib95`` has built-in support for all function types, including special functions.
See :ref:`special-functions-label` for more information.

Boolean methods
---------------

Problems contain a set of functions that report "emergent" boolean information
about the problem given its data.

* :func:`~tsplib95.models.StandardProblem.is_explicit`
* :func:`~tsplib95.models.StandardProblem.is_full_matrix`
* :func:`~tsplib95.models.StandardProblem.is_weighted`
* :func:`~tsplib95.models.StandardProblem.is_special`
* :func:`~tsplib95.models.StandardProblem.is_complete`
* :func:`~tsplib95.models.StandardProblem.is_symmetric`
* :func:`~tsplib95.models.StandardProblem.is_depictable`


Extra attributes
----------------

There can be no extra or unknown keywords in a problem. Typically, this results
in a failure to parse the field preceding it, but not necessarily (for example,
if the presence of the keyword in the value of the preceding field is valid then
there will be no error).

However, not all fields defined on a :class:`Problem` must be present in a problem.
In such a case, requesting the value on the problem instance returns the default
value for the field. Fields are not rendered or written to file unless their value
has been set.

Tracing tours
-------------

Some TSPLIB95 files have a TOURS field that lists one or more tours. Often, the
tour(s) are in a separate ``.opt.tour`` file.
:class:`~tsplib95.models.StandardProblem` has a TOURS field, which means it can
parse these ``.opt.tour`` files as well::

    >>> opt = tsplib95.load('archives/solutions/tour/gr666.opt.tour')
    >>> opt.type
    'TOUR'
    >>> len(opt.tours)
    1
    >>> len(opt.tours[0])
    666

We have 1 tour to trace. We can simply pass the list of tours to
:func:`~tsplib95.models.StandardProblem.trace_tours`::

    >>> problem = tsplib95.load('archives/problems/tsp/gr666.tsp')
    >>> >>> problem.trace_tours(opt.tours)
    [294358]

.. note::

    Note that it returned a list of tour weights, one for each tour given.

For testing purposes, there is also
:func:`~tsplib95.models.StandardProblem.trace_canonical_tour`, which uses the
nodes in definition order as a tour and returns the total weight::

    >>> weight = problem.trace_canonical_tour()


Converting problems
===================

:func:`~tsplib95.models.StandardProblem.get_graph` creates a ``networkx.Graph``
instance from the problem data::

    >>> G = problem.get_graph()
    >>> G.nodes
    NodeView((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16))

The graph, nodes, and edges of the object contain as much accessory information
as is present in the problem instance::

    >>> G.graph
    {'name': 'gr17',
    'comment': '17-city problem (Groetschel)',
    'type': 'TSP',
    'dimension': 17,
    'capacity': 0}
    >>> G.nodes[0]
    {'coord': None, 'display': None, 'demand': None, 'is_depot': False}
    >>> G.edges[0, 1]
    {'weight': 633, 'is_fixed': False}



.. _TSPLIB: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
.. _TSPLIB problem files: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/ALL_tsp.tar.gz
.. _TSPLIB95 file format standards: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf
