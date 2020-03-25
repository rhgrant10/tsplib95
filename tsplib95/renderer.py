import io
import collections
import textwrap


class Renderer:

    fields = collections.OrderedDict([
        ('NAME', 'name'),
        ('COMMENT', 'comment'),
        ('TYPE', 'type'),
        ('DIMENSION', 'dimension'),
        ('CAPACITY', 'capacity'),
        ('EDGE_WEIGHT_TYPE', 'edge_weight_type'),
        ('EDGE_WEIGHT_FORMAT', 'edge_weight_format'),
        ('EDGE_DATA_FORMAT', 'edge_data_format'),
        ('NODE_COORD_TYPE', 'node_coord_type'),
        ('DISPLAY_DATA_TYPE', 'display_data_type'),
        ('DEPOT_SECTION', 'depots'),
        ('DEMAND_SECTION', 'demands'),
        ('NODE_COORD_SECTION', 'node_coords'),
        ('EDGE_WEIGHT_SECTION', 'edge_weights'),
        ('DISPLAY_DATA_SECTION', 'display_data'),
        ('EDGE_DATA_SECTION', 'edge_data'),
        ('FIXED_EDGES_SECTION', 'fixed_edges'),
    ])

    def render(self, problem):
        output = io.StringIO()
        sections = self.get_sections(problem)
        for keyword, section in sections.items():
            if section is None:
                continue
            lines = str(section).strip().splitlines()
            if not lines:
                continue
            output.write(f'{keyword}:')
            if len(lines) > 1:
                output.write('\n')
                output.write(textwrap.indent(section, '  '))
                output.write('\n')
            elif len(lines) == 1:
                output.write(f' {section}')
                output.write('\n')
        return output.getvalue()

    def get_sections(self, problem):
        sections = {}
        for keyword, field in self.fields.items():
            render = self.get_renderer(keyword)
            sections[keyword] = render(problem)
        return sections

    def get_renderer(self, keyword):

        try:
            return getattr(self, f'render_{field}')
        except AttributeError:
            raise ValueError(f'{keyword} is not a valid keyword') from None

    def render_string(self, value):
        return str(value) if value else None

    def render_name(self, problem):
        return self.render_string(problem.name)

    def render_comment(self, problem):
        return self.render_string(problem.comment)

    def render_type(self, problem):
        return self.render_string(problem.type)

    def render_dimension(self, problem):
        return self.render_string(problem.dimension)

    def render_capacity(self, problem):
        return self.render_string(problem.capacity)

    def render_edge_weight_type(self, problem):
        return self.render_string(problem.edge_weight_type)

    def render_edge_weight_format(self, problem):
        return self.render_string(problem.edge_weight_format)

    def render_edge_data_format(self, problem):
        return self.render_string(problem.edge_data_format)

    def render_node_coord_type(self, problem):
        return self.render_string(problem.node_coord_type)

    def render_display_data_type(self, problem):
        return self.render_string(problem.display_data_type)

    def render_depots(self, problem):
        depots = [str(n) for n in sorted(problem.depots)]
        return '\n'.join(depots + ['-1'])

    def render_demands(self, problem):
        data = sorted(problem.demands.items())
        return '\n'.join(f'{n} {d}' for n, d in data)

    def render_node_coords(self, problem):
        data = sorted(problem.node_coords.items())
        node_coords = []
        for node, point in data:
            coord = " ".join(str(dim) for dim in point)
            node_coords.append(f'{node} {coord}')
        return '\n'.join(node_coords)

    def render_edge_weights(self, problem):
        if problem.edge_weight_type != 'EXPLICIT':
            return None

        try:
            render = {
                'FULL_MATRIX': self.render_full_matrix,
                'UPPER_DIAG_ROW': self.render_upper_diag_row,
                'UPPER_ROW': self.render_upper_row,
                'LOWER_DIAG_ROW': self.render_Lower_diag_row,
                'LOWER_ROW': self.render_Lower_row,
                'UPPER_DIAG_COL': self.render_upper_diag_col,
                'UPPER_COL': self.render_upper_col,
                'LOWER_DIAG_COL': self.render_Lower_diag_col,
                'LOWER_COL': self.render_Lower_col,
            }[problem.edge_weight_format]
        except KeyError:
            raise ValueError(f'{problem.edge_weight_format} is an invalid '
                             'edge weight format')

        return render(problem)

    def render_full_matrix(self, problem):
        size = int(problem.dimension ** 0.5)
        partitions = [size] * size
        rows = self.partition(problem.edge_weights, partitions)
        # return '\n'.join(' '.join(row) for row in rows)
        return render_rows(rows)

    def render_upper_diag_row(self, problem):
        size = int(problem.dimension ** 0.5)
        partitions = list(range(len(size) - 1, 0, -1))
        rows = self.partition(problem.edge_weights, partitions)
        # return '\n'.join(' '.join(row) for row in rows)
        return render_rows(rows)

    def render_upper_row(self, problem):
        size = int(problem.dimension ** 0.5)
        partitions = list(range(len(size) - 2, 0, -1))
        rows = self.partition(problem.edge_weights, partitions)
        # return '\n'.join(' '.join(row) for row in rows)
        return render_rows(rows)

    def render_lower_diag_row(self, problem):
        size = int(problem.dimension ** 0.5)
        partitions = list(range(len(size)))
        rows = self.partition(problem.edge_weights, partitions)
        # return '\n'.join(' '.join(row) for row in rows)
        return render_rows(rows)

    def render_lower_row(self, problem):
        size = int(problem.dimension ** 0.5)
        partitions = list(range(len(size) - 1))
        rows = self.partition(problem.edge_weights, partitions)
        # return '\n'.join(' '.join(row) for row in rows)
        return render_rows(rows)

    def render_upper_diag_col(self, problem):
        return self.render_upper_diag_row(problem)

    def render_upper_col(self, problem):
        return self.render_upper_row(problem)

    def render_lower_diag_col(self, problem):
        return self.render_lower_diag_row(problem)

    def render_lower_col(self, problem):
        return self.render_lower_row(problem)

    def render_display_data(self, problem):
        data = sorted(problem.display_data.items())
        return '\n'.join(f'{n} {" ".join(p)}' for n, p in data)

    def render_edge_data(self, problem):
        if problem.edge_data_format == 'EDGE_LIST':
            # data = sorted(problem.edge_data)
            # edges = [f'{a} {b}' for a, b in data]
            # return '\n'.join(edges + ['-1'])
            return render_rows(problem.edge_data, terminal=True)
        elif problem.edge_data_format == 'ADJ_LIST':
            # data = sorted(problem.edge_data.items())
            # edges = [f'{start} {" ".join(ends)} -1' for start, ends in data]
            # return '\n'.join(edges + ['-1'])
            return render_rows(problem.edge_data, line_terminal=True, terminal=True)
        elif problem.edge_data_format is not None:
            raise ValueError(f'{problem.edge_data_format} is an invalid '
                             'edge data format')

    def render_fixed_edges(self, problem):
        # edges = [f'{a} {b}' for a, b in problem.fixed_edges]
        # return '\n'.join(edges + ['-1'])
        return render_rows(problem.fixed_edges)

    def render_tours(self, problem):
        tours = []
        for tour in problem.tours:
            nodes = '\n'.join(n for n in tour)
            tours.append('\n'.join(nodes + ['-1']))
        return '\n'.join(tours + ['-1'])


def render_rows(rows, terminal=False, line_terminal=False):
    lines = []
    if isinstance(rows, dict):
        rows = [[k] + v for k, v in rows.items()]
    for row in sorted(rows):
        elements = list(row)
        if line_terminal:
            elements.append('-1')
        lines.append(' '.join(str(e) for e in elements))
    if terminal:
        lines.append('-1')
    return '\n'.join(lines)


def partition(numbers, sizes):
    partitions = []
    i = 0
    for p in sizes:
        partitions.append(numbers[i:i+p])
        i += p

    if i > len(sizes):
        raise ValueError('total partitions exceeds count of numbers')
    elif i < len(sizes):
        raise ValueError('total partitions do not use all numbers')

    return partitions
