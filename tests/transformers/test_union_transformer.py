from unittest import mock

import pytest

from tsplib95 import transformers as T
from tsplib95 import exceptions as E


FOO = object()
BAR = object()


@pytest.mark.parametrize('kw1,kw2,value,exc', [
    (dict(return_value=FOO), dict(return_value=BAR), FOO, None),
    (dict(side_effect=Exception()), dict(return_value=BAR), BAR, None),
    (dict(return_value=FOO), dict(side_effect=Exception()), FOO, None),
    (dict(side_effect=Exception()), dict(side_effect=Exception()), None, E.ParsingError),  # noqa: E501
])
def test_parse(kw1, kw2, value, exc):
    tf = T.UnionT(mock.Mock(parse=mock.Mock(**kw1)),
                  mock.Mock(parse=mock.Mock(**kw2)))
    if exc:
        with pytest.raises(exc):
            tf.parse('text')
    else:
        assert tf.parse('text') == value


@pytest.mark.parametrize('kw1,kw2,text,exc', [
    (dict(return_value='foo'), dict(return_value='bar'), 'foo', None),
    (dict(side_effect=Exception()), dict(return_value='bar'), 'bar', None),
    (dict(return_value='foo'), dict(side_effect=Exception()), 'foo', None),
    (dict(side_effect=Exception()), dict(side_effect=Exception()), None, E.RenderingError),  # noqa: E501
])
def test_render(kw1, kw2, text, exc):
    tf = T.UnionT(mock.Mock(render=mock.Mock(**kw1)),
                  mock.Mock(render=mock.Mock(**kw2)))
    if exc:
        with pytest.raises(exc):
            tf.render(FOO)
    else:
        assert tf.render(FOO) == text
