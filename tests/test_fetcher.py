"""Тесты парсинга и сетевых ошибок. Реальный интернет не нужен."""
import asyncio
import httpx
import pytest
from matrix_lib.exceptions import MatrixFetchError, MatrixParseError
from matrix_lib.fetcher import _fetch_text, parse_matrix
from matrix_lib.spiral import traverse_spiral_ccw
# Текст в том же формате, что и matrix.txt из задания
MATRIX_TEXT = """+-----+-----+-----+-----+
|  10 |  20 |  30 |  40 |
+-----+-----+-----+-----+
|  50 |  60 |  70 |  80 |
+-----+-----+-----+-----+
|  90 | 100 | 110 | 120 |
+-----+-----+-----+-----+
| 130 | 140 | 150 | 160 |
+-----+-----+-----+-----+
"""
TRAVERSAL = [10, 50, 90, 130, 140, 150, 160, 120, 80, 40, 30, 20, 60, 100, 110, 70]
def test_parse_avito_example():
    """Текст из задания превращается в правильный обход."""
    assert traverse_spiral_ccw(parse_matrix(MATRIX_TEXT)) == TRAVERSAL

def test_parse_other_size():
    """Размерность может меняться:.matrix 1x1 тоже работает."""
    assert traverse_spiral_ccw(parse_matrix("+---+\n| 7 |\n+---+\n")) == [7]

def test_parse_empty_response():
    with pytest.raises(MatrixParseError):
        parse_matrix("")

def test_parse_not_a_number():
    with pytest.raises(MatrixParseError):
        parse_matrix("| a | 2 |\n| 3 | 4 |\n")

def test_parse_not_square():
    with pytest.raises(MatrixParseError):
        parse_matrix("| 1 | 2 | 3 |\n| 4 | 5 | 6 |\n")

def _fetch_with_mock(handler):
    """Делает запрос к фейковому серверу, который отвечает по сценарию handler."""

    async def run():
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport) as client:
            return await _fetch_text(client, "https://example.com/matrix.txt")

    return asyncio.run(run())

def test_fetch_success():
    text = _fetch_with_mock(lambda request: httpx.Response(200, text=MATRIX_TEXT))
    assert traverse_spiral_ccw(parse_matrix(text)) == TRAVERSAL

def test_fetch_server_error_500():
    with pytest.raises(MatrixFetchError, match="500"):
        _fetch_with_mock(lambda request: httpx.Response(500))

def test_fetch_timeout():
    def handler(request):
        raise httpx.ConnectTimeout("сервер не ответил вовремя")

    with pytest.raises(MatrixFetchError):
        _fetch_with_mock(handler)
def test_fetch_connection_refused():
    def handler(request):
        raise httpx.ConnectError("соединение отклонено")
    with pytest.raises(MatrixFetchError):
        _fetch_with_mock(handler)