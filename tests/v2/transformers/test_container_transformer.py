from unittest import mock

import pytest

from tsplib95.v2 import transformers as T
from tsplib95.v2 import exceptions


@pytest.fixture
def container_tf():
    def make(**kwargs):
        tf = T.ContainerT(**kwargs)
        tf.pack = list
        tf.unpack = list
        return tf
    return make


@pytest.mark.parametrize('kwargs,correct', [
    ({'sep': ':'}, ['a b', 'c-d', '--e']),
    ({'sep': '-'}, ['a b:c', 'd:', 'e']),
    ({'sep': '-', 'filter_empty': False}, ['a b:c', 'd:', '', 'e']),
    ({'sep': ':', 'terminal': '--e'}, ['a b', 'c-d']),
    ({'sep': ':', 'size': 3}, ['a b', 'c-d', '--e']),
    ({'sep': ':', 'terminal': 'e'}, ['a b', 'c-d', '--']),
])
def test_container_tf_parse(container_tf, kwargs, correct):
    tf = container_tf(**kwargs)
    result = tf.parse('a b:c-d:--e')
    assert result == correct


@pytest.mark.parametrize('text', [
    'a b',
    'a b c d',
])
def test_container_tf_parse_wrong_size(container_tf, text):
    tf = container_tf(size=3)
    with pytest.raises(exceptions.ParsingError):
        tf.parse(text)


def test_container_tf_parse_no_terminal(container_tf):
    tf = container_tf(terminal='-1')
    with pytest.raises(exceptions.ParsingError):
        tf.parse('a b')


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
