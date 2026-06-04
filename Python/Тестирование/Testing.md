# Testing in Python

**Тестирование** — проверка корректности кода. Виды тестов, инструменты, best practices.

## 1. Виды тестов

| Тип | Описание | Пример |
|---|---|---|
| **Unit** | Проверка одной функции/класса | `test_add()` |
| **Integration** | Взаимодействие модулей | БД + API |
| **Functional** | Поведение с точки зрения пользователя | `requests.get()` |
| **Regression** | Старая функциональность не сломалась | Запуск всех тестов |
| **Smoke** | Критичные пути работают | Сервер отвечает 200 |
| **Performance** | Скорость выполнения | > 1000 rps |

## 2. pytest

```python
# pip install pytest

# test_sample.py

def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, 1) == 0
```

```bash
pytest                     # все тесты
pytest test_sample.py      # конкретный файл
pytest test_sample.py::test_add  # конкретный тест
pytest -v                  # verbose
pytest -k "add"            # фильтр по имени
pytest -x                  # остановиться на первой ошибке
pytest --tb=short          # короткий traceback
pytest --maxfail=5         # остановиться после N ошибок
```

### Fixtures

```python
import pytest

@pytest.fixture
def data():
    return {"name": "Анна", "age": 30}

def test_name(data):
    assert data["name"] == "Анна"

# scope: function (default), class, module, session
@pytest.fixture(scope="session")
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()
```

### Parametrize

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Conftest

```python
# conftest.py — общие фикстуры для всей папки

@pytest.fixture
def client():
    from app import app
    return app.test_client()
```

### Моки (monkeypatch)

```python
def get_user_name(user_id):
    import requests
    resp = requests.get(f"https://api.example.com/users/{user_id}")
    return resp.json()["name"]

def test_get_user_name(monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return {"name": "Анна"}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    assert get_user_name(1) == "Анна"
```

## 3. unittest

```python
import unittest

def add(a, b):
    return a + b

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(add(-1, 1), 0)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            add("a", 1)

if __name__ == "__main__":
    unittest.main()
```

```bash
python -m unittest test_module.py
python -m unittest discover  # все тесты
```

## 4. pytest vs unittest

| | pytest | unittest |
|---|---|---|
| Установка | `pip install pytest` | Встроенный |
| Синтаксис | `assert` | `self.assertEqual()` |
| Fixtures | Встроенные | `setUp` / `tearDown` |
| Parametrize | `@pytest.mark.parametrize` | `subTest()` |
| Плагины | Множество | Ограниченно |
| Популярность | **Стандарт** | legacy |

## 5. Coverage

```bash
pip install pytest-cov

pytest --cov=src/           # отчёт
pytest --cov=src/ --cov-report=html  # html отчёт
pytest --cov=src/ --cov-report=term-missing  + непокрытые строки
```

```python
# .coveragerc или pyproject.toml
[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/migrations/*"]
```

## 6. Doctest

```python
def add(a, b):
    """Складывает два числа.

    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    """
    return a + b
```

```bash
python -m doctest module.py
```

## 7. Структура тестов

```
src/
├── app/
│   ├── models.py
│   ├── views.py
│   └── services.py
tests/
├── conftest.py
├── test_models.py
├── test_views.py
└── test_services.py
```

### Именование

```python
# файл: test_<module>.py
# функция: test_<description>()

def test_create_user_success():
    ...

def test_create_user_duplicate_email():
    ...
```

## 8. Best Practices

```python
# 1. Один assert на тест (или один логический)
def test_add_positive():
    assert add(1, 2) == 3

def test_add_negative():
    assert add(-1, 1) == 0

# 2. Изолированные тесты — не зависят друг от друга
# 3. Fixtures для подготовки данных
# 4. Тесты должны быть быстрыми
# 5. Тестируй граничные случаи
@pytest.mark.parametrize("value", [None, "", 0, [], {}])
def test_empty_values(value):
    assert process(value) is None

# 6. Не тестируй встроенное
# плохо:
def test_len():
    assert len([1, 2]) == 2

# 7. Используй factories/builders для сложных данных
@pytest.fixture
def user_dict():
    return {
        "id": 1,
        "name": "Анна",
        "email": "anna@example.com",
    }
```

## 9. Плагины pytest

| Плагин | Описание |
|---|---|
| `pytest-cov` | Coverage report |
| `pytest-xdist` | Параллельный запуск |
| `pytest-mock` | Лучшая работа с mocks |
| `pytest-asyncio` | Асинхронные тесты |
| `pytest-django` | Тесты Django |
| `pytest-flask` | Тесты Flask |
| `pytest-httpx` | Мок для HTTPX |
| `pytest-timeout` | Тайм-аут для тестов |
| `pytest-randomly` | Случайный порядок |

## 10. Mock

```python
from unittest.mock import Mock, patch, MagicMock

# Mock объект
mock = Mock()
mock.return_value = 42
assert mock() == 42

# patch контекст
with patch("module.requests.get") as mock_get:
    mock_get.return_value.json.return_value = {"key": "val"}
    result = module.fetch_data()
    assert result["key"] == "val"

# patch декоратор
@patch("module.requests.get")
def test_fetch(mock_get):
    mock_get.return_value.json.return_value = {"key": "val"}
    ...
```

## 11. TDD (Test Driven Development)

1. Написать тест (он падает — **Red**)
2. Написать минимальный код (тест проходит — **Green**)
3. Рефакторинг (**Refactor**)
```
Red → Green → Refactor ↻
```
