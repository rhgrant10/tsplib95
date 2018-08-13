# -*- coding: utf-8 -*-
import functools
import math

from . import utils


def euclidean(start, end, round=utils.nint):
    """Return the Euclidean distance between start and end.

    :param tuple start: *n*-dimensional coordinate
    :param tuple end: *n*-dimensional coordinate
    :param callable round: function to use to round the result
    :return: rounded distance
    """
    if len(start) != len(end):
        raise ValueError('dimension mismatch between start and end')

    square_distance = sum(d * d for d in utils.deltas(start, end))
    distance = math.sqrt(square_distance)

    return round(distance)


def manhattan(start, end, round=utils.nint):
    """Return the Manhattan distance between start and end.

    :param tuple start: *n*-dimensional coordinate
    :param tuple end: *n*-dimensional coordinate
    :param callable round: function to use to round the result
    :return: rounded distance
    """
    if len(start) != len(end):
        raise ValueError('dimension mismatch between start and end')

    distance = sum(abs(d) for d in utils.deltas(start, end))

    return round(distance)


def maximum(start, end, round=utils.nint):
    """Return the Maximum distance between start and end.

    :param tuple start: *n*-dimensional coordinate
    :param tuple end: *n*-dimensional coordinate
    :param callable round: function to use to round the result
    :return: rounded distance
    """
    if len(start) != len(end):
        raise ValueError('dimension mismatch between start and end')

    distance = max(abs(d) for d in utils.deltas(start, end))

    return round(distance)


def geographical(start, end, round=utils.nint, diameter=6378.388):
    """Return the geographical distance between start and end.

    :param tuple start: *n*-dimensional coordinate
    :param tuple end: *n*-dimensional coordinate
    :param callable round: function to use to round the result
    :param float diameter: the diameter of the Earth
    :return: rounded distance
    """
    if len(start) != len(end):
        raise ValueError('dimension mismatch between start and end')

    start = utils.RadianGeo(start)
    end = utils.RadianGeo(end)

    q1 = math.cos(start.lng - end.lng)
    q2 = math.cos(start.lat - end.lat)
    q3 = math.cos(start.lat + end.lat)
    distance = diameter * math.acos(0.5 * ((1 + q1) * q2 - (1 - q1) * q3)) + 1

    return round(distance)


def pseudo_euclidean(start, end, round=utils.nint):
    """Return the pseudo-Euclidean distance between start and end.

    :param tuple start: *n*-dimensional coordinate
    :param tuple end: *n*-dimensional coordinate
    :param callable round: function to use to round the result
    :return: rounded distance
    """
    if len(start) != len(end):
        raise ValueError('dimension mismatch between start and end')

    square_sum = sum(d * d for d in utils.deltas(start, end))
    value = math.sqrt(square_sum / 10)

    # with nint does this not equate to ceil? and what about other cases?
    distance = round(value)
    if distance < value:
        distance += 1
    return distance


def xray(start, end, sx=1, sy=1, sz=1, round=utils.icost):
    """Return x-ray crystallography distance.

    :param tuple start: 3-dimensional coordinate
    :param tuple end: 3-dimensional coordinate
    :param float sx: x motor speed
    :param float sy: y motor speed
    :param float sz: z motor speed
    :return: distance
    """
    if len(start) != len(end) or len(start) != 3:
        raise ValueError('start and end but be 3-dimensional')

    dx = min(abs(start[0] - end[0]), abs(abs(start[0] - end[0])) - 360)
    dy = abs(start[1] - end[1])
    dz = abs(start[2] - end[2])
    distance = max(dx / sx, dy / sy, dz / sz)

    return round(distance)


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
    'XRAY1': xray,
    'XRAY2': functools.partial(xray, sx=1.25, sy=1.5, sz=1.15),
}
