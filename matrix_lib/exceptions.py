"""Ошибки библиотеки."""
class MatrixError(Exception):
    """Базовая ошибка библиотеки."""
class MatrixFetchError(MatrixError):
    """Не удалось скачать матрицу: проблема с сетью или ответом сервера."""
class MatrixParseError(MatrixError):
    """В ответе сервера нет корректной квадратной матрицы."""   