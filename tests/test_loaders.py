import pytest

from tsplib95 import loaders


@pytest.mark.parametrize('filepath', [
    ('data/gr666.tsp'),
])
def test_load_problem_fromstring(read_problem_text, filepath):
    text = read_problem_text(filepath)
    assert loaders.load_problem_fromstring(text)


@pytest.mark.parametrize('filepath', [
    ('data/gr666.tsp'),
])
def test_load_problem(get_problem_filepath, filepath):
    path = get_problem_filepath(filepath)
    assert loaders.load_problem(path)
