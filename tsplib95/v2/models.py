import re

from . import fields as F


class FileMeta(type):
    def __new__(cls, name, bases, data):
        data['fields'] = {}
        for name, attr in list(data.items()):
            if isinstance(attr, F.Field):
                data['fields'][attr.name] = attr
                data['fields'][attr.name].name = name  # tricky
        return super().__new__(cls, name, bases, data)

    def parse(cls, text):
        names = '|'.join(cls.fields)
        sep = '''\s*:\s*|\s*\n'''
        pattern = f'({names}|EOF)(?:{sep})'
        regex = re.compile(pattern, re.M)

        __, *results = regex.split(text)
        field_names = results[::2]
        field_values = results[1::2]

        data = {}
        for name, value in zip(field_names, field_values):
            if name != 'EOF':
                field = cls.fields[name]
                value = field.parse(value)
                data[field.name] = value

        return data

    def render(cls, value):
        pass


class Problem(metaclass=FileMeta):
    pass


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


# p = Problem.parse(text)
# print(p.name)
# p.render()
# Problem.render(p)
