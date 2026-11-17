"""Тесты алгоритма обхода по спирали (без сети)."""
import pytest
from matrix_lib.spiral import traverse_spiral_ccw
def test_avito_example_4x4():
    """Официальный test case из задания Авито."""
    matrix = [
        [10, 20, 30, 40],
        [50, 60, 70, 80],
        [90, 100, 110, 120],
        [130, 140, 150, 160],
    ]
    expected = [
        10, 50, 90, 130,
        140, 150, 160, 120,
        80, 40, 30, 20,
        60, 100, 110, 70,
    ]
    assert traverse_spiral_ccw(matrix) == expected
def test_1x1():
    assert traverse_spiral_ccw([[7]]) == [7]
def test_2x2():
    assert traverse_spiral_ccw([[1, 2], [3, 4]]) == [1, 3, 4, 2]
def test_3x3_odd_with_center():
    """Нечётный размер: в конце остаётся центральный элемент."""
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert traverse_spiral_ccw(matrix) == [1, 4, 7, 8, 9, 6, 3, 2, 5]
def test_5x5():
    matrix = [[r * 5 + c + 1 for c in range(5)] for r in range(5)]
    expected = [
        1, 6, 11, 16, 21,
        22, 23, 24, 25,
        20, 15, 10, 5,
        4, 3, 2,
        7, 12, 17,
        18, 19,
        14, 9,
        8,
        13,
    ]
    assert traverse_spiral_ccw(matrix) == expected
def test_empty_matrix():
    assert traverse_spiral_ccw([]) == []
    assert traverse_spiral_ccw([[]]) == []
def test_not_square_raises():
    with pytest.raises(ValueError):
        traverse_spiral_ccw([[1, 2, 3], [4, 5, 6]])
def test_all_elements_present_once():
    """Каждый элемент встречается ровно один раз, ничего не теряется."""
    for n in range(1, 10):
        matrix = [[r * n + c for c in range(n)] for r in range(n)]
        result = traverse_spiral_ccw(matrix)
        assert len(result) == n * n
        assert sorted(result) == list(range(n * n))