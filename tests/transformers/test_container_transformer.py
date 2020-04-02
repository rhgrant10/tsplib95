from unittest import mock

import pytest

from tsplib95 import transformers as T
from tsplib95 import exceptions as E


@pytest.fixture
def container_tf():
    def make(**kwargs):
        tf = T.ContainerT(**kwargs)
        tf.pack = list
        tf.unpack = list
        return tf
    return make


@pytest.mark.parametrize('kwargs,correct', [
    ({'sep': ':'}, ['a b', 'c-d', '--', 'e']),
    ({'sep': '-'}, ['a b:c', 'd:', ':e']),
    ({'sep': '-', 'filter_empty': False}, ['a b:c', 'd:', '', ':e']),
    ({'sep': ':', 'terminal': 'e'}, ['a b', 'c-d', '--']),
    ({'sep': ':', 'size': 3, 'terminal': 'e'}, ['a b', 'c-d', '--']),
    ({'sep': ':', 'size': 4}, ['a b', 'c-d', '--', 'e']),
])
def test_container_tf_parse(container_tf, kwargs, correct):
    tf = container_tf(**kwargs)
    result = tf.parse('a b:c-d:--:e')
    assert result == correct


@pytest.mark.parametrize('text', [
    'a b',
    'a b c d',
])
def test_container_tf_parse_wrong_size(container_tf, text):
    tf = container_tf(size=3)
    with pytest.raises(E.ParsingError):
        tf.parse(text)


def test_container_tf_parse_no_terminal(container_tf):
    tf = container_tf(terminal='-1')
    with pytest.raises(E.ParsingError):
        tf.parse('a b')


def test_container_tf_parse_middle_terminal(container_tf):
    tf = container_tf(terminal='-1')
    with pytest.raises(E.ParsingError):
        tf.parse('a -1 b -1')


def test_container_tf_parse_near_middle_terminal(container_tf):
    tf = container_tf(terminal='-1')
    assert tf.parse('a -1b -1') == ['a', '-1b']


@pytest.mark.parametrize('kwargs,text', [
    ({}, 'a b c'),
    ({'terminal': '-1'}, 'a b c -1'),
])
def test_container_tf_render(container_tf, kwargs, text):
    tf = container_tf(**kwargs)
    assert tf.render(['a', 'b', 'c']) == text


def test_container_tf_parse_item(container_tf):
    tf = container_tf()
    tf.child_tf.parse = mock.Mock()
    assert tf.parse_item('foo') == tf.child_tf.parse.return_value


def test_container_tf_render_item(container_tf):
    tf = container_tf()
    tf.child_tf.render = mock.Mock()
    assert tf.render_item('foo') == tf.child_tf.render.return_value


def test_container_tf_split_items(container_tf):
    tf = container_tf()
    tf.sep.split = mock.Mock()
    assert tf.split_items('foo') == tf.sep.split.return_value


def test_container_tf_join_items(container_tf):
    tf = container_tf()
    tf.sep.join = mock.Mock()
    assert tf.join_items('foo') == tf.sep.join.return_value


def test_container_tf_split_items_error(container_tf):
    tf = container_tf()
    tf.split_items = mock.Mock(side_effect=Exception())
    with pytest.raises(E.ParsingError):
        tf.parse('foo')


def test_container_tf_parse_item_error(container_tf):
    tf = container_tf()
    tf.parse_item = mock.Mock(side_effect=Exception())
    with pytest.raises(E.ParsingError):
        tf.parse('foo')


@pytest.mark.parametrize('attr', ['pack', 'unpack'])
def test_container_tf_needs_implementation(attr):
    tf = T.ContainerT()
    with pytest.raises(NotImplementedError):
        getattr(tf, attr)(object())
