# -*- coding: utf-8 -*-
import itertools

import networkx

from . import matrix
from . import distances
from . import utils


class File:
    """Base file format type.

    This class isn't meant to be used directly. It contains the common keyword
    values common among all formats. Note that all information is optional. In
    that case the value will be None. See the official TSPLIB_ documentation
    for more details.

    .. _TSPLIB: https://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/index.html
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get('NAME')
        self.comment = kwargs.get('COMMENT')
        self.type = kwargs.get('TYPE')
        self.dimension = kwargs.get('DIMENSION')


class Solution(File):
    """A TSPLIB solution file containing one or more tours to a problem.

    The length of a solution is the number of tours it contains.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tours = kwargs.get('TOUR_SECTION')

    def __len__(self):
        return len(self.tours)


class Problem(File):
    """A TSPLIB problem file.

    For problems that require a special distance function, you must set the
    special function in one of two ways:

    .. code-block:: python

        >>> problem = Problem(special=func, ...)  # at creation time
        >>> problem.special = func                # on existing problem

    Special distance functions are ignored for explicit problems but are
    required for some.

    Regardless of problem type or specification, the weight of the edge between
    two nodes given by index can always be found using ``wfunc``. For example,
    to get the weight of the edge between nodes 13 and 6:

    .. code-block:: python

        >>> problem.wfunc(13, 6)
        87

    The length of a problem is the number of nodes it contains.
    """

    def __init__(self, special=None, **kwargs):
        super().__init__(**kwargs)
        self.capacity = kwargs.get('CAPACITY')

        # specification
        self.edge_weight_type = kwargs.get('EDGE_WEIGHT_TYPE')
        self.edge_weight_format = kwargs.get('EDGE_WEIGHT_FORMAT')
        self.edge_data_format = kwargs.get('EDGE_DATA_FORMAT')
        self.node_coord_type = kwargs.get('NODE_COORD_TYPE')
        self.display_data_type = kwargs.get('DISPLAY_DATA_TYPE')

        # data
        self.depots = kwargs.get('DEPOT_SECTION')
        self.demands = kwargs.get('DEMAND_SECTION')
        self.node_coords = kwargs.get('NODE_COORD_SECTION')
        self.edge_weights = kwargs.get('EDGE_WEIGHT_SECTION')
        self.display_data = kwargs.get('DISPLAY_DATA_SECTION')
        self.edge_data = kwargs.get('EDGE_DATA_SECTION')
        self.fixed_edges = kwargs.get('FIXED_EDGES_SECTION', set())

        self.wfunc = None
        self.special = special

    def __len__(self):
        return self.dimension

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

    def _create_wfunc(self, special=None):
        # smooth out the differences between explicit and calculated problems
        if self.is_explicit():
            matrix = self._create_explicit_matrix()
            return lambda i, j: matrix[i, j]
        else:
            return self._create_distance_function(special=special)

    def _create_distance_function(self, special=None):
        # wrap a distance function so that it takes node indexes, not coords
        if self.is_special():
            if special is None:
                raise Exception('missing needed special weight function')
            wfunc = special
        elif self.is_weighted():
            wfunc = distances.TYPES[self.edge_weight_type]
        else:
            return lambda i, j: 1

        def adapter(i, j):
            return wfunc(self.node_coords[i], self.node_coords[j])

        return adapter

    def _create_explicit_matrix(self):
        # instantiate the right matrix class for the problem
        m = min(self.get_nodes())
        Matrix = matrix.TYPES[self.edge_weight_format]
        return Matrix(self.edge_weights, self.dimension, min_index=m)

    def get_nodes(self):
        """Return an iterator over the nodes.

        :return: nodes
        :rtype: iter
        """
        if self.node_coords:
            return iter(self.node_coords)
        elif self.display_data:
            return iter(self.display_data)
        else:
            return iter(range(self.dimension))

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
            except TypeError:
                return self.node_coords[i]
        else:
            return None

    def get_graph(self):
        """Return the corresponding networkx.Graph instance.

        If the graph is not symmetric then a DiGraph is returned. If present,
        the coordinates of each node are set to the ``coord`` key, and each
        edge has an ``is_fixed`` key that is True if the edge is in the list
        of fixed edges.

        :return: graph
        """
        G = networkx.Graph() if self.is_symmetric() else networkx.DiGraph()
        G.graph['name'] = self.name
        G.graph['comment'] = self.comment
        G.graph['type'] = self.type
        G.graph['dimension'] = self.dimension
        G.graph['capacity'] = self.capacity
        G.graph['depots'] = self.depots
        G.graph['demands'] = self.demands
        G.graph['fixed_edges'] = self.fixed_edges

        if not self.is_explicit():
            for i, coord in self.node_coords.items():
                G.add_node(i, coord=coord)

        for i, j in self.get_edges():
            weight = self.wfunc(i, j)
            is_fixed = (i, j) in self.fixed_edges
            G.add_edge(i, j, weight=weight, is_fixed=is_fixed)

        return G
