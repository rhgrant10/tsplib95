from . import transformers as T
from . import exceptions


class Field:
    def __init__(self, keyword, *, transformer=None):
        self.keyword = keyword
        self.tf = transformer or self.build_transformer()

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
    @classmethod
    def build_transformer(cls):
        return T.FuncT(func=int)


class FloatField(Field):
    @classmethod
    def build_transformer(cls):
        return T.FuncT(func=float)


class NumberField(Field):
    @classmethod
    def build_transformer(cls):
        return T.NumberT()


class IndexedCoordinatesField(Field):
    def __init__(self, *args, dimensions=None):
        """Coordinates listed by integer index.

        Dimensions can be a single value, a tuple of possible values, or none.
        Every coordinate must be the same dimensionality, and if present, this
        value dictates the valid dimensionalities. The check is enforced
        during validation.
        """
        super().__init__(*args)
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
    @classmethod
    def build_transformer(cls):
        return T.MapT(key=T.FuncT(func=int),
                      value=T.ListT(value=T.FuncT(func=int)),
                      sep=('-1', ' -1\n'),
                      terminal='-1')


class EdgeListField(Field):
    @classmethod
    def build_transformer(cls):
        edge = T.ListT(value=T.FuncT(func=int), size=2)
        return T.ListT(value=edge, terminal='-1', sep='\n')


class MatrixField(Field):
    @classmethod
    def build_transformer(cls):
        row = T.ListT(value=T.NumberT())
        return T.ListT(value=row, terminal='-1', sep='\n')


class EdgeDataField(Field):
    @classmethod
    def build_transformer(cls):
        adj_list = AdjacencyListField.build_transformer()
        edge_list = EdgeListField.build_transformer()
        return T.UnionT(adj_list, edge_list)


class DepotsField(Field):
    @classmethod
    def build_transformer(cls):
        depot = T.FuncT(func=int)
        return T.ListT(value=depot, terminal='-1')


class DemandsField(Field):
    @classmethod
    def build_transformer(cls):
        demand = T.ListT(value=T.FuncT(func=int), size=2)
        return T.ListT(value=demand, terminal='-1', sep='\n')


class ToursField(Field):
    @classmethod
    def build_transformer(cls):
        tour = T.ListT(value=T.FuncT(func=int), terminal='-1')
        return T.ListT(value=tour, terminal='-1')
