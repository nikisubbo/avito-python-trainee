"""Алгоритм обхода квадратной матрицы по спирали против часовой стрелки."""
from typing import List
def traverse_spiral_ccw(matrix: List[List[int]]) -> List[int]:
    """Обходит квадратную матрицу по спирали против часовой стрелки.
    Обход начинается с левого верхнего угла: вниз по левому столбцу,
    вправо по нижней строке, вверх по правому столбцу, влево по верхней
    строке. После каждого круга границы сужаются к центру.
    Args:
        matrix: квадратная матрица целых чисел размера NxN.
    Returns:
        Плоский список элементов в порядке обхода.
    Raises:
        ValueError: если матрица не квадратная.
    Сложность: O(N^2) по времени, O(1) дополнительной памяти
    (не считая списка результата).
    """
    if not matrix or not matrix[0]:
        return []
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("Матрица должна быть квадратной (NxN)")
    result: List[int] = []
    top, bottom = 0, n - 1   # границы строк
    left, right = 0, n - 1   # границы столбцов
    while top <= bottom and left <= right:
        # 1. Вниз по левому столбцу
        for row in range(top, bottom + 1):
            result.append(matrix[row][left])
        left += 1
        # 2. Вправо по нижней строке
        for col in range(left, right + 1):
            result.append(matrix[bottom][col])
        bottom -= 1
        # 3. Вверх по правому столбцу (если остался хотя бы один столбец)
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][right])
            right -= 1
        # 4. Влево по верхней строке (если осталась хотя бы одна строка)
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[top][col])
            top += 1
    return result