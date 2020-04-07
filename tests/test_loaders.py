import pytest

from tsplib95 import loaders


@pytest.mark.parametrize('filepath', [
    ('data/gr666.tsp'),
])
def test_parse(read_problem_text, filepath):
    text = read_problem_text(filepath)
    assert loaders.parse(text)


@pytest.mark.parametrize('filepath', [
    ('data/gr666.tsp'),
])
def test_load(get_problem_filepath, filepath):
    path = get_problem_filepath(filepath)
    assert loaders.load(path)
