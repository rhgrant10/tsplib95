# -*- coding: utf-8 -*-
import collections
import itertools
import re

import networkx

from . import fields as F
from . import matrix
from . import distances
from . import utils


class FileMeta(type):
    def __new__(mcs, name, bases, attrs):
        # we need to map the fields by keyword and by field name
        # data is a dictionary of class attributes, some of which are fields
        # we need to pop the fields out and use them to create two maps
        # one by keyword and one by field name

        # first, we build the data for the current class
        current = {
            'fields_by_name': {},
            'fields_by_keyword': {},
            'names_by_keyword': {},
            'keywords_by_name': {},
        }
        for name, value in list(attrs.items()):
            if isinstance(value, F.Field):
                current['fields_by_name'][name] = value
                current['fields_by_keyword'][value.keyword] = value
                current['names_by_keyword'][value.keyword] = name
                current['keywords_by_name'][name] = value.keyword
                attrs.pop(name)

        # use the data to build a new class
        attrs.update(current)
        new_class = super().__new__(mcs, name, bases, attrs)

        for key in current:
            # merge together the data from all classes in the class
            # hierarchy by traversing them in reverse MRO order.
            data = {}
            for base in reversed(new_class.__mro__):
                if hasattr(base, key):
                    data.update(getattr(base, key))

                # be sure to take care of attribute hiding
                for name, value in base.__dict__.items():
                    if value is None and name in data:
                        data.pop(name)

            # set the final value on the new class
            setattr(new_class, key, data)

        return new_class


class Problem(metaclass=FileMeta):

    def __init__(self, special=None, **data):
        super().__init__()
        # every keyword argument becomes an attribute
        for name, value in data.items():
            setattr(self, name, value)
        self._special = special

    @classmethod
    def parse(cls, text, special=None):
        # prepare the regex for all known keys
        keywords = '|'.join(cls.fields_by_keyword)
        sep = r'''\s*:\s*|\s*\n'''
        pattern = f'({keywords}|EOF)(?:{sep})'

        # split the whole text by known keys
        regex = re.compile(pattern, re.M)
        __, *results = regex.split(text)

        # pair keys and values
        field_keywords = results[::2]
        field_values = results[1::2]

        # parse into a dictionary
        data = {}
        for keyword, value in zip(field_keywords, field_values):
            if keyword != 'EOF':
                field = cls.fields_by_keyword[keyword]
                name = cls.names_by_keyword[keyword]
                data[name] = field.parse(value.strip())

        # return as a model
        return cls(special=special, **data)

    def __str__(self):
        return self.render()

    def __getattribute__(self, name):
        # check for a value like normal
        try:
            attrs = object.__getattribute__(self, '__dict__')
            return attrs[name]
        except KeyError:
            pass

        # value missing, so try to return the default
        # for the correpsonding field
        try:
            cls = object.__getattribute__(self, '__class__')
            field = cls.fields_by_name[name]
            return field.get_default_value()
        except KeyError:
            pass

        # not a field, so punt to the super implementation
        return super().__getattribute__(name)

    def render(self):
        # render each value by keyword
        rendered = {}
        for name, field in self.__class__.fields_by_name.items():
            if name in self.__dict__:  # has had a value set
                rendered[field.keyword] = field.render(getattr(self, name))

        # build keyword-value pairs with the separator
        kvpairs = []
        for keyword, value in rendered.items():
            sep = ':\n' if '\n' in value else ': '
            kvpairs.append(f'{keyword}{sep}{value}')
        kvpairs.append('EOF')

        # join and return the result
        return '\n'.join(kvpairs)


class StandardProblem(Problem):
    name = F.StringField('NAME')
    comment = F.StringField('COMMENT')
    type = F.StringField('TYPE')
    dimension = F.IntegerField('DIMENSION')

    capacity = F.IntegerField('CAPACITY')
    node_coord_type = F.StringField('NODE_COORD_TYPE')
    edge_weight_type = F.StringField('EDGE_WEIGHT_TYPE')
    display_data_type = F.StringField('DISPLAY_DATA_TYPE')
    edge_weight_format = F.StringField('EDGE_WEIGHT_FORMAT')
    edge_data_format = F.StringField('EDGE_DATA_FORMAT')

    node_coords = F.IndexedCoordinatesField('NODE_COORD_SECTION', dimensions=(2, 3))  # noqa: E501
    edge_data = F.EdgeDataField('EDGE_DATA_SECTION')
    edge_weights = F.MatrixField('EDGE_WEIGHT_SECTION')
    display_data = F.IndexedCoordinatesField('DISPLAY_DATA_SECTION', dimensions=2)  # noqa: E501
    fixed_edges = F.EdgeListField('FIXED_EDGES_SECTION')
    depots = F.DepotsField('DEPOT_SECTION')
    demands = F.DemandsField('DEMAND_SECTION')

    tours = F.ToursField('TOUR_SECTION')

    def __init__(self, special=None, **kwargs):
        super().__init__(**kwargs)
        self.wfunc = None
        self.special = special

    @property
    def special(self):
        """Special distance function"""
        return self._special

    @special.setter
    def special(self, func):
        """Set the special distance function.

        Special/custom distance functions must accept two coordinates of
        appropriate dimension and return the distance between them.

        Note that this has no effect if the problem defines weights explicitly.

        :param callable func: custom distance function
        """
        self._special = func
        self.wfunc = self._create_wfunc(special=func)

    def is_explicit(self):
        """Return True if the problem specifies explicit edge weights.

        :rtype: bool
        """
        return self.edge_weight_type == 'EXPLICIT'

    def is_full_matrix(self):
        """Return True if the problem is specified as a full matrix.

        :rtype: bool
        """
        return self.edge_weight_format == 'FULL_MATRIX'

    def is_weighted(self):
        """Return True if the problem has weighted edges.

        :rtype: bool
        """
        return bool(self.edge_weight_format) or bool(self.edge_weight_type)

    def is_special(self):
        """Return True if the problem requires a special distance function.

        :rtype: bool
        """
        return self.edge_weight_type == 'SPECIAL'

    def is_complete(self):
        """Return True if the problem specifies a complete graph.

        :rtype: bool
        """
        return not bool(self.edge_data_format)

    def is_symmetric(self):
        """Return True if the problem is not asymmetrical.

        Note that even if this method returns False there is no guarantee that
        there are any two nodes with an asymmetrical distance between them.

        :rtype: bool
        """
        return not self.is_full_matrix() and not self.is_special()

    def is_depictable(self):
        """Return True if the problem is designed to be depicted.

        :rtype: bool
        """
        if bool(self.display_data):
            return True

        if self.display_data_type == 'NO_DISPLAY':
            return False

        return bool(self.node_coords)

    def trace_tours(self, solution):
        """Calculate the total weights of the tours in the given solution.

        :param solution: solution with tours to trace
        :type solution: :class:`~Solution`
        :return: one or more tour weights
        :rtype: list
        """
        solutions = []
        for tour in solution.tours:
            weight = sum(self.wfunc(i, j) for i, j in utils.pairwise(tour))
            solutions.append(weight)
        return solutions

    def get_nodes(self):
        """Return an iterator over the nodes.

        :return: nodes
        :rtype: iter
        """
        if self.node_coords:
            return iter(self.node_coords)

        if self.display_data:
            return iter(self.display_data)

        if self.edge_data_format == 'EDGE_LIST':
            nodes = set()
            for a, b in self.edge_data:
                nodes.update({a, b})
            return iter(nodes)

        if self.edge_data_format == 'ADJ_LIST':
            nodes = set()
            for a, ends in self.edge_data.items():
                nodes.update({a, *ends})
            return iter(nodes)

        try:
            return iter(range(self.dimension))
        except Exception:
            raise ValueError('undefined nodes')

    def get_edges(self):
        """Return an iterator over the edges.

        :return: edges
        :rtype: iter
        """
        if self.edge_data_format == 'EDGE_LIST':
            yield from self.edge_data
        elif self.edge_data_format == 'ADJ_LIST':
            for i, adj in self.edge_data.items():
                yield from ((i, j) for j in adj)
        else:
            yield from itertools.product(self.get_nodes(), self.get_nodes())

    def get_display(self, i):
        """Return the display data for node at index *i*, if available.

        :param int i: node index
        :return: display data for node i
        """
        if self.is_depictable():
            try:
                return self.display_data[i]
            except (KeyError, TypeError):
                return self.node_coords[i]
        else:
            return None

    def get_graph(self, normalize=False):
        """Return a networkx graph instance representing the problem.

        The metadata of the problem is associated with the graph itself.
        Additional problem information is associated with the nodes and edges.
        For example:

        .. code-block:: python

            >>> G.graph
            {'name': None,
             'comment': '14-Staedte in Burma (Zaw Win)',
             'type': 'TSP',
             'dimension': 14,
             'capacity': None}
            >>> G.nodes[1]
            {'coord': (16.47, 96.1),
             'display': None,
             'demand': None,
             'is_depot': False}
            >>> G.edges[1, 2]
            {'weight': 2, 'is_fixed': False}

        If the graph is not symmetric then a :class:`networkx.DiGraph` is
        returned. Optionally, the nodes can be renamed to be sequential and
        zero-indexed.

        :param bool normalize: rename nodes to be zero-indexed
        :return: graph
        :rtype: :class:`networkx.Graph`
        """
        # directed graphs are fundamentally different
        G = networkx.Graph() if self.is_symmetric() else networkx.DiGraph()

        # add basic graph metadata
        G.graph['name'] = self.name
        G.graph['comment'] = self.comment
        G.graph['type'] = self.type
        G.graph['dimension'] = self.dimension
        G.graph['capacity'] = self.capacity

        # set up a map from original node name to new node name
        nodes = list(self.get_nodes())
        if normalize:
            names = {n: i for i, n in enumerate(nodes)}
        else:
            names = {n: n for n in nodes}

        # add every node with some associated metadata
        for n in nodes:
            is_depot = n in self.depots
            G.add_node(names[n], coord=self.node_coords.get(n),
                       display=self.display_data.get(n),
                       demand=self.demands.get(n),
                       is_depot=is_depot)

        # add every edge with some associated metadata
        for a, b in self.get_edges():
            weight = self.wfunc(a, b)
            is_fixed = (a, b) in self.fixed_edges
            G.add_edge(names[a], names[b], weight=weight, is_fixed=is_fixed)

        # return the graph object
        return G

    def _create_wfunc(self, special=None):
        # handle the differences between explicit and calculated problems
        if self.is_explicit():
            matrix = self._create_explicit_matrix()
            return lambda i, j: matrix[i, j]
        if self.is_special():
            if special is None:
                raise Exception('missing needed special weight function')
            wfunc = special
        elif self.is_weighted():
            wfunc = distances.TYPES[self.edge_weight_type]
        else:
            return lambda i, j: 1  # unweighted graphs

        # wrap the distance function so that it takes node indexes, not coords
        def adapter(i, j):
            return wfunc(self.node_coords[i], self.node_coords[j])

        return adapter

    def _create_explicit_matrix(self):
        # instantiate the right matrix class for the problem
        m = min(self.get_nodes())
        Matrix = matrix.TYPES[self.edge_weight_format]
        return Matrix(self.edge_weights, self.dimension, min_index=m)
