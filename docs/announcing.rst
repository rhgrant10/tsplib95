I'm pleased to announce the release of tsplib95 v0.4.0!

What's New?
-----------

You can define your own problems!


What is tsplib95?
-----------------

tsplib95 is a library for reading TSPLIB95 problems and solutions.
It supports the entire file format specification and automatically
converts problems into ``networkx.Graph`` instances.

License: Apache Software License 2.0

* Read the **docs**: https://tsplib95.readthedocs.io/
* Install from **PyPI**: https://pypi.org/project/tsplib95/0.4.0/
* Contribute **source**: https://github.com/rhgrant10/tsplib95

Example
-------

.. code-block:: python

    >>> import tsplib95
    >>> import networkx as nx

    >>> # read problem files
    >>> problem = tsplib95.load_problem('path/to/att48.tsp')
    >>> problem.name
    >>> problem.comment
    '48 capitals of the US (Padberg/Rinaldi)'
    >>> problem.dimension
    48
    >>> problem.type
    'TSP'
    
    >>> # auto-generated weight function for any two nodes
    >>> problem.get_weight(2, 6)
    6977

    >>> # convert to networkx
    >>> G = problem.get_graph()
    >>> if problem.is_symmteric():
    ...     assert issubclass(G, nx.Graph)
    ... else:
    ...     assert issubclass(G, nx.DiGraph)
    >>> if problem.is_depictable():
    ...     nx.draw(G)
    ... 


Enjoy!

Robert Grant
