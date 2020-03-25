"""

Problems load fine. Unknown fields are available in a 

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

    class JsonField(tsplib95.Field):
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

"""
