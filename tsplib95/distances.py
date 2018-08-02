# -*- coding: utf-8 -*-
import collections
import functools
import math


LatLng = collections.namedtuple('LatLng', 'lat lng')


def nint(x):
    return int(x + 0.5)


def _deltas(start, end):
    return (e - s for e, s in zip(end, start))


def _parse_degrees(coord):
    degrees = nint(coord)
    minutes = coord - degrees
    return degrees + minutes * 5 / 3


def to_radian_coord(coord):
    x, y = coord
    lat = math.radians(_parse_degrees(x))
    lng = math.radians(_parse_degrees(y))
    return LatLng(lat, lng)


def euclidean(start, end, round=nint):
    square_distance = sum(d * d for d in _deltas(start, end))
    return round(math.sqrt(square_distance))


def manhattan(start, end, round=nint):
    total_distance = sum(abs(d) for d in _deltas(start, end))
    return round(total_distance)


def maximum(start, end, round=nint):
    return max(round(abs(d)) for d in _deltas(start, end))


def geographical(start, end, round=nint, diameter=6378.388):
    start = to_radian_coord(start)
    end = to_radian_coord(end)

    q1 = math.cos(start.lng - end.lng)
    q2 = math.cos(start.lat - end.lat)
    q3 = math.cos(start.lat + end.lat)
    distance = diameter * math.acos(0.5 * ((1 + q1) * q2 - (1 - q1) * q3)) + 1

    return round(distance)


def pseudo_euclidean(start, end, round=nint):
    square_sum = sum(d * d for d in _deltas(start, end))
    value = math.sqrt(square_sum / 10)
    distance = round(value)
    if distance < value:
        value = distance + 1
    return distance


TYPES = {
    'EUC_2D': euclidean,
    'EUC_3D': euclidean,
    'MAX_2D': maximum,
    'MAX_3D': maximum,
    'MAN_2D': manhattan,
    'MAN_3D': manhattan,
    'CEIL_2D': functools.partial(euclidean, round=math.ceil),
    'GEO': euclidean,
    'ATT': euclidean,
}
