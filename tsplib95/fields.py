# -*- coding: utf-8 -*-
from . import transformers as T
from . import exceptions


class Field:
    default = None

    def __init__(self, keyword, *, transformer=None, default=None):
        self.keyword = keyword
        self.default = default or self.__class__.default
        self.tf = transformer

    @property
    def tf(self):
        if self._tf is None:
            self._tf = self.build_transformer()
        return self._tf

    @tf.setter
    def tf(self, value):
        self._tf = value

    def get_default_value(self):
        if callable(self.default):
            return self.default()
        return self.default

    @classmethod
    def build_transformer(cls):
        return T.Transformer()

    def parse(self, text):
        return self.tf.parse(text)

    def render(self, value):
        return self.tf.render(value)

    def validate(self, value):
        return self.tf.validate(value)


class StringField(Field):
    @classmethod
    def build_transformer(cls):
        return T.FuncT(func=str)


class IntegerField(Field):
    default = 0

    @classmethod
    def build_transformer(cls):
        return T.FuncT(func=int)


class FloatField(Field):
    default = 0.0

    @classmethod
    def build_transformer(cls):
        return T.FuncT(func=float)


class NumberField(Field):
    default = 0

    @classmethod
    def build_transformer(cls):
        return T.NumberT()


class IndexedCoordinatesField(Field):
    default = dict

    def __init__(self, *args, dimensions=None, **kwargs):
        """Coordinates listed by integer index.

        Dimensions can be a single value, a tuple of possible values, or none.
        Every coordinate must be the same dimensionality, and if present, this
        value dictates the valid dimensionalities. The check is enforced
        during validation.
        """
        super().__init__(*args, **kwargs)
        try:
            self.dimensions = tuple(iter(dimensions))
        except Exception:
            self.dimensions = (dimensions,) if dimensions else None

    @classmethod
    def build_transformer(cls):
        key = T.FuncT(func=int)
        value = T.ListT(value=T.NumberT())
        return T.MapT(key=key, value=value, sep='\n')

    def validate(self, value):
        super().validate(value)
        cards = set(len(coord) for coord in value.values())
        if self.dimensions and cards not in ({dim} for dim in self.dimensions):
            raise exceptions.ValidationError('all coordinates must have the same '  # noqa: E501
                                             f'dimensionality {self.dimensions}')   # noqa: E501


class AdjacencyListField(Field):
    default = dict

    @classmethod
    def build_transformer(cls):
        return T.MapT(key=T.FuncT(func=int),
                      value=T.ListT(value=T.FuncT(func=int)),
                      sep=('-1', ' -1\n'),
                      terminal='-1')


class EdgeListField(Field):
    default = list

    @classmethod
    def build_transformer(cls):
        edge = T.ListT(value=T.FuncT(func=int), size=2)
        return T.ListT(value=edge, terminal='-1', sep='\n')


class MatrixField(Field):
    default = list

    @classmethod
    def build_transformer(cls):
        row = T.ListT(value=T.NumberT())
        return T.ListT(value=row, terminal='-1', sep='\n')


class EdgeDataField(Field):
    default = dict

    @classmethod
    def build_transformer(cls):
        adj_list = AdjacencyListField.build_transformer()
        edge_list = EdgeListField.build_transformer()
        return T.UnionT(adj_list, edge_list)


class DepotsField(Field):
    default = list

    @classmethod
    def build_transformer(cls):
        depot = T.FuncT(func=int)
        return T.ListT(value=depot, terminal='-1')


class DemandsField(Field):
    default = dict

    @classmethod
    def build_transformer(cls):
        node = T.FuncT(func=int)
        demand = T.FuncT(func=int)
        return T.MapT(key=node, value=demand, terminal='-1', sep='\n')


class ToursField(Field):
    default = list

    @classmethod
    def build_transformer(cls):
        tour = T.ListT(value=T.FuncT(func=int), terminal='-1')
        return T.ListT(value=tour, terminal='-1')


"""
import tsplib95
with open('archives/problems/tsp/att48.tsp') as f:
    problem_text = f.read()

problem = tsplib95.parse(problem_text)
G = problem.get_graph()
"""