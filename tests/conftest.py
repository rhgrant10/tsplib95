import os

import pytest


@pytest.fixture(scope='module')
def read_problem_text():
    def read(relpath):
        directory = os.path.dirname(__file__)
        with open(os.path.join(directory, relpath)) as f:
            return f.read()
    return read


@pytest.fixture(scope='module')
def get_problem_filepath():
    def make_path(relpath):
        directory = os.path.dirname(__file__)
        return os.path.join(directory, relpath)
    return make_path
