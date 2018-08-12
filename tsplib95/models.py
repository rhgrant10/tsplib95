# -*- coding: utf-8 -*-
import itertools

import networkx

from . import matrix
from . import distances


def pairwise(indexes):
    starts = list(indexes)
    ends = list(indexes)
    ends += [ends.pop(0)]
    return zip(starts, ends)


class File:
    def __init__(self, **kwargs):
        self.name = kwargs.get('NAME')
        self.comment = kwargs.get('COMMENT')
        self.type = kwargs.get('TYPE')
        self.dimension = kwargs.get('DIMENSION')

    def __len__(self):
        return self.dimension

    def get_nodes(self):
        raise NotImplementedError()


class Solution(File):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tours = kwargs.get('TOUR_SECTION')

    def get_nodes(self):
        return list(self.tours[0])


class Problem(File):
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
        self.fixed_edges = kwargs.get('FIXED_EDGES_SECTION')

        self.wfunc = self._create_wfunc(special=special)

    def is_explicit(self):
        return self.edge_weight_type == 'EXPLICIT'

    def is_full_matrix(self):
        return self.edge_weight_format == 'FULL_MATRIX'

    def is_special(self):
        return self.edge_weight_type == 'SPECIAL'

    def is_complete(self):
        return 'EDGE_DATA_FORMAT' not in self

    def is_symmetric(self):
        return not self.is_full_matrix() and not self.is_special()

    def is_depictable(self):
        if 'DISPLAY_DATA_SECTION' in self:
            return True

        if self.display_data_type == 'NO_DISPLAY':
            return False

        return 'NODE_COORD_SECTION' in self

    def trace_tours(self, solution):
        solutions = []
        for tour in solution.tours:
            weight = sum(self.get_weight(i, j) for i, j in pairwise(tour))
            solutions.append(weight)
        return solutions

    def _create_wfunc(self, special=None):
        if self.is_explicit():
            matrix = self._create_explicit_matrix()
            return lambda i, j: matrix[i, j]
        else:
            return self._create_distance_function(special=special)

    def _create_distance_function(self, special=None):
        if special is None:
            if self.is_special():
                raise Exception('missing needed special weight function')
            wfunc = distances.TYPES[self.edge_weight_type]
        else:
            wfunc = special

        def adapter(i, j):
            return wfunc(self.node_coords[i], self.node_coords[j])

        return adapter

    def _create_explicit_matrix(self):
        m = min(self.get_nodes())
        Matrix = matrix.TYPES[self.edge_weight_format]
        return Matrix(self.edge_weights, self.dimension, min_index=m)

    def get_nodes(self):
        if 'NODE_COORD_SECTION' in self:
            return list(self.node_coords)
        elif 'DISPLAY_DATA_SECTION' in self:
            return list(self.display_data)
        else:
            return list(range(self.dimension))

    def get_edges(self):
        if self.edge_data_format == 'EDGE_LIST':
            yield from self.edge_data
        elif self.edge_data_format == 'ADJ_LIST':
            for i, adj in self.edge_data.items():
                yield from ((i, j) for j in adj)
        else:
            indexes = self.get_nodes()
            yield from itertools.product(iter(indexes), iter(indexes))

    def get_display(self, i):
        if self.is_depictable():
            try:
                return self.display_data[i]
            except TypeError:
                return self.node_coord[i]
        else:
            return None

    def get_graph(self):
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
