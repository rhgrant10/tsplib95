import pytest

from tsplib95 import models as M
from tsplib95 import fields as F


FOO_FIELD = F.Field('FOO')
BAZ_FIELD = F.Field('BAZ')
QUUX_FIELD = F.Field('QUUX')
CORGE_FIELD = F.Field('CORGE')


class BaseProblem(metaclass=M.FileMeta):
    foo = FOO_FIELD
    bar = 42
    corge = CORGE_FIELD


class CustomProblem(BaseProblem):
    baz = BAZ_FIELD
    qux = 3.14
    quux = QUUX_FIELD
    corge = None  # test attribute hiding


@pytest.mark.parametrize('Problem,correct', [
    (BaseProblem, {'foo': FOO_FIELD, 'corge': CORGE_FIELD}),
    (CustomProblem, {'foo': FOO_FIELD, 'baz': BAZ_FIELD, 'quux': QUUX_FIELD}),
])
def test_fields_by_name(Problem, correct):
    assert Problem.fields_by_name == correct


@pytest.mark.parametrize('Problem,correct', [
    (BaseProblem, {'FOO': FOO_FIELD, 'CORGE': CORGE_FIELD}),
    (CustomProblem, {'FOO': FOO_FIELD, 'BAZ': BAZ_FIELD, 'QUUX': QUUX_FIELD, 'CORGE': CORGE_FIELD}),  # noqa: E501
])
def test_fields_by_keyword(Problem, correct):
    assert Problem.fields_by_keyword == correct


@pytest.mark.parametrize('Problem,correct', [
    (BaseProblem, {'FOO': 'foo', 'CORGE': 'corge'}),
    (CustomProblem, {'FOO': 'foo', 'BAZ': 'baz', 'QUUX': 'quux', 'CORGE': 'corge'}),  # noqa: E501
])
def test_names_by_keyword(Problem, correct):
    assert Problem.names_by_keyword == correct


@pytest.mark.parametrize('Problem,correct', [
    (BaseProblem, {'foo': 'FOO', 'corge': 'CORGE'}),
    (CustomProblem, {'foo': 'FOO', 'baz': 'BAZ', 'quux': 'QUUX'}),
])
def test_keywords_by_name(Problem, correct):
    assert Problem.keywords_by_name == correct


@pytest.mark.parametrize('Problem,correct', [
    (BaseProblem, {'bar': 42}),
    (CustomProblem, {'bar': 42, 'qux': 3.14}),
])
def test_non_fields_are_class_attributes(Problem, correct):
    assert all(getattr(Problem, k) == v for k, v in correct.items())


@pytest.mark.parametrize('Problem', [
    BaseProblem,
    CustomProblem,
])
def test_fields_are_not_class_attributes(Problem):
    with pytest.raises(AttributeError):
        Problem.foo
