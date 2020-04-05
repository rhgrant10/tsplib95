# -*- coding: utf-8 -*-
import re

from . import transformers as T
from . import exceptions


class Field:
    default = None

    def __init__(self, keyword, *, default=None):
        self.keyword = keyword
        self.default = default or self.__class__.default

    def __repr__(self):
        return f'<{self.__class__.__qualname__}({repr(self.keyword)})>'

    def get_default_value(self):
        if callable(self.default):
            return self.default()
        return self.default

    def parse(self, text):
        raise NotImplementedError()

    def render(self, value):
        raise NotImplementedError()

    def validate(self, value):
        pass


class TransformerField(Field):

    def __init__(self, keyword, *, transformer=None, **kwargs):
        super().__init__(keyword, **kwargs)
        self.tf = transformer

    @classmethod
    def build_transformer(cls):
        return T.Transformer()

    @property
    def tf(self):
        if self._tf is None:
            self._tf = self.build_transformer()
        return self._tf

    @tf.setter
    def tf(self, value):
        self._tf = value

    def parse(self, text):
        try:
            return self.tf.parse(text)
        except exceptions.ParsingError as e:
            context = f'{self.__class__.__qualname__}({self.keyword})'
            raise exceptions.ParsingError.wrap(e, context)

    def render(self, value):
        try:
            return self.tf.render(value)
        except exceptions.RenderingError as e:
            context = f'{self.__class__.__qualname__}({self.keyword})'
            raise exceptions.RenderingError.wrap(e, context)

    def validate(self, value):
        return self.tf.validate(value)


class StringField(TransformerField):
    @classmethod
    def build_transformer(cls):
        return T.FuncT(func=str)


class IntegerField(TransformerField):
    default = 0

    @classmethod
    def build_transformer(cls):
        return T.FuncT(func=int)


class FloatField(TransformerField):
    default = 0.0

    @classmethod
    def build_transformer(cls):
        return T.FuncT(func=float)


class NumberField(TransformerField):
    default = 0

    @classmethod
    def build_transformer(cls):
        return T.NumberT()


class IndexedCoordinatesField(TransformerField):
    default = dict

    def __init__(self, *args, dimensions=None, **kwargs):
        """Coordinates listed by integer index.

        Dimensions can be a single value, a tuple of possible values, or none.
        Every coordinate must be the same dimensionality, and if present, this
        value dictates the valid dimensionalities. The check is enforced
        during validation.
        """
        super().__init__(*args, **kwargs)
        self.dimensions = self.tuplize(dimensions)

    @staticmethod
    def tuplize(dimensions):
        try:
            return tuple(iter(dimensions))
        except Exception:
            return (dimensions,) if dimensions else None

    @classmethod
    def build_transformer(cls):
        key = T.FuncT(func=int)
        value = T.ListT(value=T.NumberT())
        return T.MapT(key=key, value=value, sep='\n')

    def validate(self, value):
        super().validate(value)
        cards = set(len(coord) for coord in value.values())
        if self.dimensions and cards not in ({dim} for dim in self.dimensions):
            error = ('all coordinates must have the same dimensionality '
                     f'and it must be one of {self.dimensions}')
            raise exceptions.ValidationError(error)


class AdjacencyListField(TransformerField):
    default = dict

    @classmethod
    def build_transformer(cls):
        return T.MapT(key=T.FuncT(func=int),
                      value=T.ListT(value=T.FuncT(func=int)),
                      sep=('-1', ' -1\n'),
                      terminal='-1')


class EdgeListField(TransformerField):
    default = list

    @classmethod
    def build_transformer(cls):
        edge = T.ListT(value=T.FuncT(func=int), size=2)
        return T.ListT(value=edge, terminal='-1', sep='\n')


class MatrixField(TransformerField):
    default = list

    @classmethod
    def build_transformer(cls):
        row = T.ListT(value=T.NumberT())
        return T.ListT(value=row, sep='\n')


class EdgeDataField(TransformerField):
    default = dict

    @classmethod
    def build_transformer(cls):
        adj_list = AdjacencyListField.build_transformer()
        edge_list = EdgeListField.build_transformer()
        return T.UnionT(adj_list, edge_list)


class DepotsField(TransformerField):
    default = list

    @classmethod
    def build_transformer(cls):
        depot = T.FuncT(func=int)
        return T.ListT(value=depot, terminal='-1')


class DemandsField(TransformerField):
    default = dict

    @classmethod
    def build_transformer(cls):
        node = T.FuncT(func=int)
        demand = T.FuncT(func=int)
        return T.MapT(key=node, value=demand, sep='\n')


class ToursField(Field):
    default = list

    def __init__(self, *args, require_terminal=True):
        super().__init__(*args)
        self.terminal = '-1'
        self.require_terminal = require_terminal
        self._end_terminals = re.compile(rf'(?:(?:\s+|\b|^){self.terminal})+$')
        self._any_terminal = re.compile(rf'(?:\s+|\b){self.terminal}(?:\b|\s+)')  # noqa: E501

    def parse(self, text):
        text = text.strip()
        if not text:
            return []

        match = self._end_terminals.search(text)
        # terminal must terminate, if required
        if not match and self.require_terminal:
            terminal = text.split()[-1]
            error = (f'must terminate in "{self.terminal}", '
                     f'not {repr(terminal)}')
            raise exceptions.ParsingError(error)

        # trim the terminal if present
        if match:
            text = text[:match.start()]

        # split the texts and filter out the empties
        texts = self._any_terminal.split(text)
        texts = list(filter(None, texts))
        if not texts:
            return []

        # convert the tours from texts to integer lists
        tours = []
        for text in texts:
            try:
                tour = [int(n) for n in text.strip().split()]
            except ValueError as e:
                error = f'could not convert text to node index: {repr(e)}'
                raise exceptions.ParsingError(error)
            else:
                tours.append(tour)

        return tours

    def render(self, tours):
        if not tours:
            return ''

        tour_strings = []
        for tour in tours:
            if tour:
                tour_string = ' '.join(str(i) for i in tour)
                tour_strings.append(f'{tour_string} -1')

        if tour_strings:
            tour_strings += ['-1']

        return '\n'.join(tour_strings)
