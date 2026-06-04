# pytest

**pytest** — самый популярный фреймворк для тестирования Python. Лаконичный, мощный, с кучей плагинов.

## 1. Установка

```bash
pip install pytest
pip install pytest-cov pytest-mock pytest-xdist
```

## 2. Базовые тесты

```python
# test_sample.py

def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, 1) == 0

# тест с исключением
def test_type_error():
    with pytest.raises(TypeError):
        add("a", 1)
```

```bash
pytest
pytest -v
pytest test_sample.py
pytest test_sample.py::test_add
pytest -k "add"
pytest -x              # остановиться на первой ошибке
pytest --tb=short
pytest --maxfail=3
```

## 3. Fixtures

```python
import pytest

@pytest.fixture
def user():
    return {"name": "Анна", "age": 30}

def test_name(user):
    assert user["name"] == "Анна"

def test_age(user):
    assert user["age"] == 30
```

### Scope

```python
@pytest.fixture(scope="function")   # по умолчанию — каждый тест
@pytest.fixture(scope="class")      # один раз на класс
@pytest.fixture(scope="module")     # один раз на модуль
@pytest.fixture(scope="session")    # один раз на всю сессию
```

### yield fixture (teardown)

```python
@pytest.fixture
def db():
    conn = create_connection()
    yield conn
    conn.close()
```

### autouse

```python
@pytest.fixture(autouse=True)
def setup_teardown():
    print("before")
    yield
    print("after")
```

## 4. Parametrize

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Несколько параметров

```python
@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("b", [10, 20])
def test_multiply(a, b):
    assert multiply(a, b) == a * b
# 4 теста: (1,10), (1,20), (2,10), (2,20)
```

### ids

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
], ids=["positive", "zeros"])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

## 5. conftest.py

```python
# conftest.py — фикстуры доступны всем тестам в папке

import pytest

@pytest.fixture
def api_client():
    from app import create_app
    app = create_app()
    return app.test_client()

@pytest.fixture(scope="session")
def db_url():
    return "sqlite:///test.db"
```

## 6. Маркеры

```python
@pytest.mark.slow
def test_big_computation():
    ...

@pytest.mark.skip(reason="not implemented")
def test_new_feature():
    ...

@pytest.mark.skipif(sys.version_info < (3, 11), reason="3.11+")
def test_walrus():
    ...

@pytest.mark.xfail(reason="known bug")
def test_bug():
    assert 1 == 0
```

```bash
pytest -m slow               # только slow
pytest -m "not slow"          # всё кроме slow
pytest -m "slow or api"       # slow или api
```

### Свои маркеры

```python
# pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: slow tests",
    "api: api tests",
    "integration: integration tests",
]
```

## 7. Mock и monkeypatch

### monkeypatch

```python
def test_get_user(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")
    monkeypatch.setattr(os, "getcwd", lambda: "/tmp")
```

### pytest-mock (mocker)

```bash
pip install pytest-mock
```

```python
def test_api(mocker):
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.json.return_value = {"key": "val"}

    result = fetch_data()
    assert result["key"] == "val"
    mock_get.assert_called_once_with("https://api.example.com/data")
```

## 8. tmp_path и tmpdir

```python
def test_write_file(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    f = d / "test.txt"
    f.write_text("hello")
    assert f.read_text() == "hello"

def test_temp_dir(tmpdir):
    f = tmpdir.join("test.txt")
    f.write("hello")
    assert f.read() == "hello"
```

## 9. capsys / caplog

```python
def test_output(capsys):
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"

def test_logs(caplog):
    import logging
    logging.getLogger().info("test log")
    assert "test log" in caplog.text
```

## 10. Запуск

```bash
pytest                          # все
pytest tests/                   # папка
pytest test_mod.py              # файл
pytest tests/test_mod.py::test_func  # функция
pytest -k "MyClass and not method"   # фильтр
pytest -v                       # verbose
pytest -q                       # quiet
pytest -s                       # показать stdout
pytest --tb=long                # полный traceback
pytest --tb=short               # короткий
pytest --tb=no                  # без traceback
pytest -l                       # показать локальные переменные
pytest --lf                     # только упавшие
pytest --ff                     # сначала упавшие
pytest -p no:cacheprovider      # без кэша
```

### Параллельно

```bash
pip install pytest-xdist
pytest -n auto                  # на всех ядрах
pytest -n 4                     # 4 воркера
pytest --dist=loadscope         # по модулям
```

## 11. Coverage

```bash
pip install pytest-cov

pytest --cov=src/
pytest --cov=src/ --cov-report=term-missing
pytest --cov=src/ --cov-report=html
pytest --cov=src/ --cov-report=xml
```

```ini
# .coveragerc
[run]
source = src
omit = */tests/*, */migrations/*
```

## 12. pyproject.toml

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

markers = [
    "slow: slow tests",
    "api: api tests",
]

filterwarnings = [
    "ignore::DeprecationWarning",
]

addopts = "-v --tb=short --strict-markers"
```

## 13. Плагины

| Плагин | Описание |
|---|---|
| `pytest-cov` | Coverage |
| `pytest-xdist` | Параллельный запуск |
| `pytest-mock` | Удобные моки (`mocker`) |
| `pytest-asyncio` | Асинхронные тесты |
| `pytest-django` | Django |
| `pytest-flask` | Flask |
| `pytest-httpx` | Мок HTTPX |
| `pytest-timeout` | Тайм-аут |
| `pytest-randomly` | Случайный порядок |
| `pytest-sugar` | Красивый вывод |
| `pytest-watch` | Автозапуск при изменениях |
| `pytest-benchmark` | Бенчмарки |

## 14. Структура тестов

```
tests/
├── conftest.py
├── test_models.py
├── test_views.py
└── test_services.py
```

```python
# test_models.py

class TestUser:
    def test_create(self, db):
        user = User(name="Анна")
        db.add(user)
        db.commit()
        assert user.id is not None

    def test_email_validation(self):
        with pytest.raises(ValueError):
            User(email="invalid")
```

## 15. pytest vs unittest

```python
# unittest
class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

# pytest
def test_add():
    assert add(2, 3) == 5
```

| | pytest | unittest |
|---|---|---|
| Синтаксис | `assert` | `self.assertEqual` |
| Фикстуры | `@pytest.fixture` | `setUp` / `tearDown` |
| Параметризация | `@pytest.mark.parametrize` | `subTest()` |
| Плагины | ✅ | ❌ |
| Популярность | **Стандарт** | Легаси |
