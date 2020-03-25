import re

from . import fields as F


class FileMeta(type):
    def __new__(cls, name, bases, data):
        fields = {}
        for name, attr in list(data.items()):
            if isinstance(attr, F.Field):
                # swap the keyword and the name
                fields[attr.keyword] = attr
                fields[attr.keyword].keyword = name  # tricky
        data['fields'] = fields
        return super().__new__(cls, name, bases, data)


class Problem(metaclass=FileMeta):

    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)

    @classmethod
    def parse(cls, text):
        # prepare the regex for all known keys
        keywords = '|'.join(cls.fields)
        sep = '''\s*:\s*|\s*\n'''
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
                field = cls.fields[keyword]
                value = field.parse(value.strip())
                data[field.keyword] = value

        # return as a model
        return cls(**data)

    def render(self):
        keywords = {f.keyword: kw for kw, f in self.__class__.fields.items()}

        rendered = {}
        for name, value in vars(self).items():
            keyword = keywords[name]
            field = self.__class__.fields[keyword]
            rendered[keyword] = field.render(value)

        kvpairs = []
        for keyword, value in rendered.items():
            sep = ':\n' if '\n' in value else ': '
            kvpairs.append(f'{keyword}{sep}{value}')
        kvpairs.append('EOF')

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
