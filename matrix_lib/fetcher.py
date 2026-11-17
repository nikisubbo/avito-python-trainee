"""Асинхронная загрузка матрицы с сервера и обход по спирали."""
from typing import List
import httpx
from .exceptions import MatrixFetchError, MatrixParseError
from .spiral import traverse_spiral_ccw
TIMEOUT = 5.0  # секунд на весь запрос
def parse_matrix(text: str) -> List[List[int]]:
    """Превращает текст с таблицей в квадратную матрицу чисел.

    Строки-границы вида +-----+ пропускаем, числа берём из строк с |.
    """
    matrix: List[List[int]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = line.strip("|").split("|")
        try:
            # int() сам игнорирует пробелы вокруг числа: int("  10 ") == 10
            matrix.append([int(cell) for cell in cells])
        except ValueError as exc:
            raise MatrixParseError(f"В строке матрицы не число: {line}") from exc
    if not matrix:
        raise MatrixParseError("В ответе сервера нет ни одной строки матрицы")
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise MatrixParseError("Матрица не квадратная")
    return matrix
async def get_matrix(url: str) -> List[int]:
    """Скачивает матрицу по URL и возвращает обход по спирали против часовой стрелки.

    Args:
        url: адрес, по которому лежит матрица (HTTP или HTTPS).

    Returns:
        Список чисел в порядке обхода.

    Raises:
        MatrixFetchError: сервер недоступен, ответил ошибкой или не успел ответить.
        MatrixParseError: в ответе нет корректной квадратной матрицы.
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(url)
            response.raise_for_status()  # 4xx и 5xx превращаются в исключение
            text = response.text
    except httpx.HTTPStatusError as exc:
        raise MatrixFetchError(f"Сервер вернул ошибку {exc.response.status_code}") from exc
    except httpx.RequestError as exc:
        # сюда попадают таймаут, отказ соединения, проблемы с DNS
        raise MatrixFetchError(f"Не удалось получить данные: {exc}") from exc
    return traverse_spiral_ccw(parse_matrix(text))