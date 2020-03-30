# -*- coding: utf-8 -*-
import pytest

from tsplib95 import matrix


def test_base_matrix_requires_get_index_implmentation():
    m = matrix.Matrix(range(1, 10), 3)
    with pytest.raises(NotImplementedError):
        m.get_index(0, 0)


@pytest.mark.parametrize('i,j', [
    (99, 1),
    (99, 99),
    (1, 99),
    (-99, 1),
    (-99, -99),
    (1, -99),
])
def test_matrix_value_at_out_of_bounds(i, j):
    m = matrix.FullMatrix(range(1, 10), 3)
    with pytest.raises(IndexError):
        assert m.value_at(i, j)


# 1 2 3
# 4 5 6
# 7 8 9
@pytest.mark.parametrize('i,j,v', [
    (0, 0, 1),
    (0, 2, 3),
    (1, 1, 5),
    (1, 2, 6),
    (2, 0, 7),
    (2, 2, 9),
])
def test_full_matrix(i, j, v):
    m = matrix.FullMatrix(range(1, 10), 3)
    assert m[i, j] == v


# 1 2 3
#   4 5
#     6
@pytest.mark.parametrize('i,j,v', [
    (0, 0, 1),
    (0, 2, 3),
    (1, 1, 4),
    (1, 2, 5),
    (2, 0, 3),
    (2, 2, 6),
])
def test_upper_diag_row(i, j, v):
    m = matrix.UpperDiagRow(range(1, 7), 3)
    assert m[i, j] == v


# 1
# 2 3
# 4 5 6
@pytest.mark.parametrize('i,j,v', [
    (0, 0, 1),
    (0, 2, 4),
    (1, 1, 3),
    (1, 2, 5),
    (2, 0, 4),
    (2, 2, 6),
])
def test_lower_diag_row(i, j, v):
    m = matrix.LowerDiagRow(range(1, 7), 3)
    assert m[i, j] == v


# _ 1 2 3
#   _ 4 5
#     _ 6
#       _
@pytest.mark.parametrize('i,j,v', [
    (0, 0, 0),
    (0, 3, 3),
    (1, 1, 0),
    (1, 2, 4),
    (1, 3, 5),
    (3, 0, 3),
    (2, 3, 6),
    (3, 3, 0),
])
def test_upper_row(i, j, v):
    m = matrix.UpperRow(range(1, 7), 4)
    assert m[i, j] == v


# _
# 1 _
# 2 3 _
# 4 5 6 _
@pytest.mark.parametrize('i,j,v', [
    (0, 0, 0),
    (0, 3, 4),
    (1, 1, 0),
    (1, 2, 3),
    (1, 3, 5),
    (3, 0, 4),
    (2, 3, 6),
    (3, 3, 0),
])
def test_lower_row(i, j, v):
    m = matrix.LowerRow(range(1, 7), 4)
    assert m[i, j] == v


# _ 1 2 4
#   _ 3 5
#     _ 6
#       _
@pytest.mark.parametrize('i,j,v', [
    (0, 0, 0),
    (0, 3, 4),
    (1, 1, 0),
    (1, 2, 3),
    (1, 3, 5),
    (3, 0, 4),
    (2, 3, 6),
    (3, 3, 0),
])
def test_upper_col(i, j, v):
    m = matrix.UpperCol(range(1, 7), 4)
    assert m[i, j] == v


# _
# 1 _
# 2 4 _
# 3 5 6 _
@pytest.mark.parametrize('i,j,v', [
    (0, 0, 0),
    (0, 3, 3),
    (1, 1, 0),
    (1, 2, 4),
    (1, 3, 5),
    (3, 0, 3),
    (2, 3, 6),
    (3, 3, 0),
])
def test_lower_col(i, j, v):
    m = matrix.LowerCol(range(1, 7), 4)
    assert m[i, j] == v


# 1 2 4
#   3 5
#     6
@pytest.mark.parametrize('i,j,v', [
    (0, 0, 1),
    (0, 2, 4),
    (1, 1, 3),
    (1, 2, 5),
    (2, 0, 4),
    (2, 2, 6),
])
def test_upper_diag_col(i, j, v):
    m = matrix.UpperDiagCol(range(1, 7), 3)
    assert m[i, j] == v


# 1
# 2 4
# 3 5 6
@pytest.mark.parametrize('i,j,v', [
    (0, 0, 1),
    (0, 2, 3),
    (1, 1, 4),
    (1, 2, 5),
    (2, 0, 3),
    (2, 2, 6),
])
def test_lower_diag_col(i, j, v):
    m = matrix.LowerDiagCol(range(1, 7), 3)
    assert m[i, j] == v
