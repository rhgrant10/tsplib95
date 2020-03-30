I'm pleased to announce the release of tsplib95 v0.4.0!

What's New?
-----------

You can define your own problems!

.. code-block:: python

    import tsplib95

    loader = tsplib95.loaders.PathLoader()
    problem = loader.load('some/path.tsp')

    assert problem.extra
    print(f'Unexpected data: {problem.extra.items()})
    print('Please provide the missing field classes.')


.. code-block:: python

import json
import tsplib95

class JsonField(tsplib95.fields.Field):
    def __init__(self, keyword, **options):
        super().__init__(keyword)
        self.options = options

    def parse(self, text):
        '''Convert the given text into some python data structure.'''
        return json.loads(text)

    def render(self, value):
        '''Convert the python data structure into text.'''
        return json.dumps(value, self.options)

    def validate(self, value):
        '''Raise an exception if the value fails validation.'''
        # we expect it to be a dict
        if not isinstance(value, dict):
            raise tsplib95.ValidationError('must be a dict')
        required = 'email phone website'.split()
        missing = set(required) - set(value)
        if missing:
            raise tsplib95.ValidationError(f'missing fields: {missing}')

class CustomProblem(tsplib95.Problem):
    json_data = JsonField('JSON_DATA', indent=2)

loader = tsplib95.loaders.PathLoader(class=CustomProblem)
problem = loader.load('some/path.tsp')

if not problem.extra:
    print(problem.json_data)


* parser now raises ``ParserError`` instead of ``Exception``
* problem fields are now documented
* added explicit support for python 3.7
* corrected a parameter name in ``distances.geographical``

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
    >>> problem.wfunc(2, 6)
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
