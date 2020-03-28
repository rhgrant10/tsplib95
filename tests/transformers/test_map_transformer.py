from unittest import mock

import pytest

from tsplib95 import transformers as T
from tsplib95 import exceptions


@pytest.fixture
def map_transformer():
    def make(**kwargs):
        return T.MapT(**kwargs)
    return make


def test_that_it_works(map_transformer):
    text = 'foo:1 bar:2 baz:3'
    map_ = {'foo': '1', 'bar': '2', 'baz': '3'}
    tf = map_transformer(kv_sep=':')
    assert tf.parse(text) == map_
    assert tf.render(map_) == text


@pytest.mark.parametrize('kwargs,correct', [
    ({}, ('a', 'b:c-d:--e')),
    ({'kv_sep': '-'}, ('a b:c', 'd:--e')),
    ({'kv_sep': ':'}, ('a b', 'c-d:--e')),
])
def test_map_transformer_parse_item(map_transformer, kwargs, correct):
    tf = map_transformer(**kwargs)
    assert tf.parse_item('a b:c-d:--e') == correct


def test_map_transformer_parse_item_no_kv(map_transformer):
    tf = map_transformer(kv_sep=' ')
    with pytest.raises(exceptions.ParsingError):
        tf.parse_item('abc')


def test_map_transformer_render_item(map_transformer):
    tf = map_transformer(kv_sep=' ')
    tf.render_key = mock.Mock(return_value='a')
    tf.render_value = mock.Mock(return_value='b')
    result = tf.render_item('12')
    assert tf.render_key.call_args[0] == ('1',)
    assert tf.render_value.call_args[0] == ('2',)
    assert result == 'a b'
