# -*- coding: utf-8 -*-
import collections


VALUE_TYPES = {
    'NAME': str,
    'TYPE': str,
    'COMMENT': str,
    'DIMENSION': int,
    'CAPACITY': int,
    'EDGE_WEIGHT_TYPE': str,
    'EDGE_WEIGHT_FORMAT': str,
    'EDGE_DATA_FORMAT': str,
    'NODE_COORD_TYPE': str,
    'DISPLAY_DATA_TYPE': str,
}


class Stream:
    def __init__(self, lines):
        self.lines = iter(lines)
        self.line = self._get_next()

    def __next__(self):
        self.line = self._get_next()
        return self.line

    def _get_next(self):
        try:
            line = ''
            while not line:
                line = next(self.lines).strip()
        except StopIteration:
            return None
        return line


def get_next_tour(sequence):
    tour = []
    while sequence:
        index = sequence.pop(0)

        if index == -1:
            if sequence == [-1]:
                sequence.pop(0)
            return tour

        tour.append(index)

    raise Exception('all tours must end with -1')


def read_integer_sequence(stream):
    while True:
        try:
            yield from map(int, stream.line.split())
            next(stream)
        except (ValueError, AttributeError):
            break


def partition(values, lengths):
    edge_weights = []
    for n in lengths:
        if n > len(values):
            raise Exception('too few values')
        row, values = values[:n], values[n:]
        edge_weights.append(row)

    if values:
        raise Exception('too many values')

    return edge_weights


def read_input_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


def split_kv(line):
    k, v = line.split(':', 1)
    return k.strip(), v.strip()


def parse(filename):
    lines = read_input_file(filename)
    stream = Stream(lines)
    data = {}

    transition = start
    while transition:
        transition = transition(data, stream)

    return data


def start(data, stream):
    next(stream)
    return process_line


def finish(data, stream):
    return None


def process_line(data, stream):
    if stream.line is None or stream.line == 'EOF':
        return finish

    if ':' in stream.line:
        return process_key_value
    else:
        return process_key


def process_key_value(data, stream):
    key, value = split_kv(stream.line)
    data[key] = VALUE_TYPES[key](value)
    next(stream)
    return process_line


def process_key(data, stream):
    key = stream.line
    next(stream)
    return {
        'NODE_COORD_SECTION': parse_node_coords,
        'DEPOT_SECTION': parse_depots,
        'DEMAND_SECTION': parse_demands,
        'EDGE_DATA_SECTION': parse_edge_data,
        'FIXED_EDGES_SECTION': parse_fixed_edges,
        'DISPLAY_DATA_SECTION': parse_display_data,
        'TOUR_SECTION': parse_tours,
        'EDGE_WEIGHT_SECTION': parse_edge_weights,
    }[key]


def parse_node_coords(data, stream):
    section = data['NODE_COORD_SECTION'] = collections.OrderedDict()

    while True:
        if stream.line is None:
            break

        index, *reals = stream.line.split()
        try:
            index = int(index)
        except ValueError:
            break

        if len(reals) not in (2, 3):
            raise Exception('invalid node coord')

        coord = tuple(map(float, reals))
        section[index] = coord
        next(stream)

    return process_line


def parse_depots(data, stream):
    section = data['DEPOT_SECTION'] = []

    while True:
        if stream.line is None:
            raise Exception('depot section must end with -1')

        try:
            depot = int(stream.line)
        except ValueError:
            raise Exception('invalid depot')

        if depot == -1:
            break

        section.append(depot)
        next(stream)

    next(stream)
    return process_line


def parse_demands(data, stream):
    section = data['DEMAND_SECTION'] = {}

    while True:
        if stream.line is None:
            break

        try:
            index, demand = stream.line.split()
        except ValueError:
            break

        try:
            index, demand = int(index), int(demand)
        except ValueError:
            break

        section[index] = demand
        next(stream)

    return process_line


def parse_edge_data(data, stream):
    edge_format = data['EDGE_DATA_FORMAT']
    return {
        'EDGE_LIST': parse_edge_list,
        'ADJ_LIST': parse_adj_list,
    }[edge_format]


def parse_edge_list(data, stream):
    section = data['EDGE_DATA_SECTION'] = []

    while True:
        if stream.line is None:
            raise Exception('edge list must end with a -1')

        try:
            u, v = stream.line.split()
        except ValueError:
            break

        try:
            edge = int(u), int(v)
        except ValueError:
            raise Exception('bad edge')

        section.append(edge)
        next(stream)

    if stream.line != '-1':
        raise Exception('edge list must end with a -1')

    next(stream)
    return process_line


def parse_adj_list(data, stream):
    section = data['EDGE_DATA_SECTION'] = collections.OrderedDict()

    while True:
        if stream.line is None:
            raise Exception('entire adjacency list must end with a -1')

        *values, end = stream.line.split()
        if end != '-1':
            raise Exception('adjacency list must end with a -1')
        if not values:
            break

        node, *neighbors = map(int, values)
        section[node] = neighbors
        next(stream)

    next(stream)
    return process_line


def parse_fixed_edges(data, stream):
    section = data['FIXED_EDGES_SECTION'] = []

    while True:
        if stream.line is None:
            raise Exception('fixed edges must end with a -1')

        try:
            u, v = stream.line.split()
        except ValueError:
            break

        try:
            edge = int(u), int(v)
        except ValueError:
            raise Exception('bad fixed edge')

        section.append(edge)
        next(stream)

    if stream.line != '-1':
        raise Exception('fixed edges must end with a -1')

    next(stream)
    return process_line


def parse_display_data(data, stream):
    section = data['DISPLAY_DATA_SECTION'] = collections.OrderedDict()

    while True:
        if stream.line is None:
            break

        index, *reals = stream.line.split()
        try:
            index = int(index)
        except ValueError:
            break

        if len(reals) not in (2, 3):
            raise Exception('invalid display data')

        coord = tuple(map(float, reals))
        section[index] = coord
        next(stream)

    return process_line


def parse_tours(data, stream):
    section = data['TOUR_SECTION'] = []

    sequence = list(read_integer_sequence(stream))
    while sequence:
        tour = get_next_tour(sequence)
        section.append(tour)

    return process_line


def parse_edge_weights(data, stream):
    data['EDGE_WEIGHT_SECTION'] = list(read_integer_sequence(stream))
    return process_line
