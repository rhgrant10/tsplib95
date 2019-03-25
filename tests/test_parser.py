# -*- coding: utf-8 -*-
from unittest import mock

import pytest

from tsplib95 import parser


def create_mock_stream(lines):
    lines = iter(lines)
    m_stream = mock.MagicMock()
    m_stream.line = next(lines)

    def set_next():
        m_stream.line = next(lines)
        return m_stream

    m_stream.__next__.side_effect = set_next
    return m_stream


def test_process_key_value_sets_value_for_key():
    data = {}
    m_stream = mock.MagicMock()
    m_stream.line = 'NAME: foo'

    transition = parser.process_key_value(data, m_stream)

    assert data == {'NAME': 'foo'}
    assert transition is parser.process_line


def test_process_key_value_raises_KeyError_for_invalid_key():
    m_stream = mock.MagicMock()
    m_stream.line = 'bar: foo'

    with pytest.raises(KeyError):
        parser.process_key_value({}, m_stream)


def test_parse_node_coords_with_1_dimensional_coord_raises_Exception():
    lines = [
        '1 2.3 55.4',
        '2 8.1',
        None,
    ]
    m_stream = create_mock_stream(lines)

    with pytest.raises(Exception):
        parser.parse_node_coords({}, m_stream)


def test_parse_node_coords():
    lines = [
        '1 2.3 55.4',
        '2 8.1 10.6',
        None,
    ]

    m_stream = create_mock_stream(lines)
    data = {}
    parser.parse_node_coords(data, m_stream)

    assert data['NODE_COORD_SECTION'] == {1: (2.3, 55.4), 2: (8.1, 10.6)}


def test_parse_depot_with_non_int_depot_raises_Exception():
    lines = [
        '1',
        '2.4',
        '3',
        '-1',
        None,
    ]

    m_stream = create_mock_stream(lines)
    with pytest.raises(Exception):
        parser.parse_depots({}, m_stream)


def test_parse_depot_requires_end_of_negative_1():
    lines = [
        '1',
        '2.4',
        '3',
        None,
    ]

    m_stream = create_mock_stream(lines)
    with pytest.raises(Exception):
        parser.parse_depots({}, m_stream)


def test_parse_depot():
    lines = [
        '1',
        '2',
        '3',
        '-1',
        None,
    ]

    m_stream = create_mock_stream(lines)
    data = {}
    parser.parse_depots(data, m_stream)

    assert data == {'DEPOT_SECTION': [1, 2, 3]}


def test_split_kv():
    k, v = parser.split_kv('foo: bar: baz')
    assert k == 'foo'
    assert v == 'bar: baz'
