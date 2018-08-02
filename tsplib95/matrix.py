# -*- coding: utf-8 -*-
# assume zero indexing


def _int_sum(n, memo={}):
    if n not in memo:
        s = n * (n + 1) // 2
        memo[n] = s
    return memo[n]


def integer_sum(n, m=None):
    s = _int_sum(n)
    if m:
        s -= _int_sum(m)
    return s


class Matrix:
    def __init__(self, numbers, size, min_index=0):
        self.numbers = list(numbers)
        self.size = size
        self.min_index = min_index

    def __getitem__(self, key):
        return self.value_at(*key)

    def value_at(self, i, j):
        i -= self.min_index
        j -= self.min_index
        if not self.is_valid_row_column(i, j):
            raise IndexError(f'({i}, {j}) is out of bonuds')
        index = self.get_index(i, j)
        return self.numbers[index]

    def is_valid_row_column(self, i, j):
        return 0 <= i < self.size and 0 <= j < self.size

    def get_index(self, i, j):
        pass


class FullMatrix(Matrix):
    def get_index(self, i, j):
        return i * self.size + j


class HalfMatrix(Matrix):
    has_diagonal = True

    def value_at(self, i, j):
        if i == j and not self.has_diagonal:
            return 0
        i, j = self.fix_indices(i, j)
        return super().value_at(i, j)


class UpperDiagRow(HalfMatrix):
    has_diagonal = True

    def fix_indices(self, i, j):
        return (j, i) if i > j else (i, j)

    def get_index(self, i, j):
        n = self.size - int(not self.has_diagonal)
        # index = 0
        # while i > 0:
        #     index += n
        #     i -= 1
        #     j -= 1
        #     n -= 1

        # return index + j
        return integer_sum(n, n - i) + (j - i)


class LowerDiagRow(HalfMatrix):
    has_diagonal = True

    def fix_indices(self, i, j):
        return (j, i) if i < j else (i, j)

    def get_index(self, i, j):
        # s = 1
        # index = 0
        # while i > 0:
        #     index += s
        #     i -= 1
        #     s += 1
        # return index + j
        return integer_sum(i) + j


class UpperRow(UpperDiagRow):
    has_diagonal = False

    def fix_indices(self, i, j):
        i, j = super().fix_indices(i, j)
        return i, j - 1


class LowerRow(LowerDiagRow):
    has_diagonal = False

    def fix_indices(self, i, j):
        i, j = super().fix_indices(i, j)
        return i - 1, j


TYPES = {
    'FULL_MATRIX': FullMatrix,
    'UPPER_DIAG_ROW': UpperDiagRow,
    'UPPER_ROW': UpperRow,
    'LOWER_DIAG_ROW': LowerDiagRow,
    'LOWER_ROW': LowerRow,
}
