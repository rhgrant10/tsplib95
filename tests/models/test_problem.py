import pytest


from tsplib95 import models as M
from tsplib95 import fields as F
from tsplib95 import exceptions as E


@pytest.fixture
def TestProblem():
    class TestProblem(M.Problem):
        foo = F.IntegerField('FOO')
        bar = F.StringField('BAR')
    return TestProblem


@pytest.mark.parametrize('text,value,exc', [
    ('FOO: 42\nBAR: answer', {'foo': 42, 'bar': 'answer'}, None),
    ('FOO: 4.2\nBAR: answer', None, E.ParsingError),
])
def test_model_parse(TestProblem, text, value, exc):
    if exc:
        with pytest.raises(exc):
            TestProblem.parse(text)
    else:
        problem = TestProblem.parse(text)
        attrs = {k: v for k, v in vars(problem).items() if not k.startswith('_')}  # noqa: E501
        assert attrs == value


@pytest.mark.parametrize('value,text,exc', [
    ({'foo': 42, 'bar': 'answer'}, 'FOO: 42\nBAR: answer\nEOF', None),
    ({'foo': 42, 'bar': 'answer', 'baz': 'wat'}, 'FOO: 42\nBAR: answer\nEOF', None),  # noqa: E501
])
def test_model_render(TestProblem, value, text, exc):
    problem = TestProblem(**value)
    if exc:
        with pytest.raises(exc):
            print(problem.render())
    else:
        assert problem.render() == text
