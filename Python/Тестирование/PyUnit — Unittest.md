# PyUnit / Unittest

**unittest** — встроенный фреймворк для тестирования (PyUnit, аналог JUnit). Поставляется с Python.

## 1. Базовый тест

```python
import unittest

def add(a, b):
    return a + b

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(add(-1, 1), 0)

if __name__ == "__main__":
    unittest.main()
```

## 2. Assert методы

| Метод | Проверка |
|---|---|
| `assertEqual(a, b)` | `a == b` |
| `assertNotEqual(a, b)` | `a != b` |
| `assertTrue(x)` | `x is True` |
| `assertFalse(x)` | `x is False` |
| `assertIs(a, b)` | `a is b` |
| `assertIsNot(a, b)` | `a is not b` |
| `assertIsNone(x)` | `x is None` |
| `assertIsNotNone(x)` | `x is not None` |
| `assertIn(a, b)` | `a in b` |
| `assertNotIn(a, b)` | `a not in b` |
| `assertIsInstance(a, b)` | `isinstance(a, b)` |
| `assertNotIsInstance(a, b)` | `not isinstance(a, b)` |
| `assertAlmostEqual(a, b)` | `round(a-b, 7) == 0` |
| `assertNotAlmostEqual(a, b)` | `round(a-b, 7) != 0` |
| `assertGreater(a, b)` | `a > b` |
| `assertGreaterEqual(a, b)` | `a >= b` |
| `assertLess(a, b)` | `a < b` |
| `assertLessEqual(a, b)` | `a <= b` |

### Исключения и логи

```python
def test_raises(self):
    with self.assertRaises(ValueError):
        int("abc")

def test_raises_regex(self):
    with self.assertRaisesRegex(ValueError, "invalid"):
        int("abc")

def test_logs(self):
    with self.assertLogs("mymodule", level="INFO") as log:
        mymodule.do_something()
        self.assertIn("started", log.output[0])
```

## 3. setUp и tearDown

```python
class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Вызывается перед каждым тестом."""
        self.conn = create_connection()
        self.conn.execute("CREATE TABLE test (id INT)")

    def tearDown(self):
        """Вызывается после каждого теста."""
        self.conn.execute("DROP TABLE test")
        self.conn.close()

    def test_insert(self):
        self.conn.execute("INSERT INTO test VALUES (1)")
        result = self.conn.execute("SELECT COUNT(*) FROM test")
        self.assertEqual(result[0], 1)
```

### setUpClass / tearDownClass

```python
class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Один раз перед всеми тестами класса."""
        cls.conn = create_connection()

    @classmethod
    def tearDownClass(cls):
        """Один раз после всех тестов."""
        cls.conn.close()
```

### setUpModule / tearDownModule

```python
def setUpModule():
    """Один раз перед всеми тестами модуля."""
    ...

def tearDownModule():
    """Один раз после всех тестов модуля."""
    ...
```

## 4. Пропуск тестов

```python
class TestSkip(unittest.TestCase):
    @unittest.skip("не готово")
    def test_not_ready(self):
        ...

    @unittest.skipIf(sys.version_info < (3, 11), "только 3.11+")
    def test_new_feature(self):
        ...

    @unittest.skipUnless(sys.platform.startswith("win"), "только Windows")
    def test_windows(self):
        ...

    @unittest.expectedFailure
    def test_known_bug(self):
        self.assertEqual(1, 0)
```

## 5. Запуск

```bash
# конкретный модуль
python -m unittest test_module.py

# класс
python -m unittest test_module.TestMath

# метод
python -m unittest test_module.TestMath.test_add

# все тесты в папке
python -m unittest discover
python -m unittest discover -s tests/ -p "*_test.py"

# verbose
python -m unittest -v test_module.py

# без буферизации вывода
python -m unittest -b test_module.py

# быстрый (первая ошибка — stop)
python -m unittest -f test_module.py
```

## 6. subTest

```python
def test_even(self):
    for i in range(0, 10, 2):
        with self.subTest(i=i):
            self.assertEqual(i % 2, 0)
```

## 7. Mock

```python
from unittest.mock import Mock, patch, MagicMock

class TestMock(unittest.TestCase):
    def test_mock_return(self):
        mock = Mock(return_value=42)
        self.assertEqual(mock(), 42)

    @patch("mymodule.requests.get")
    def test_api(self, mock_get):
        mock_get.return_value.json.return_value = {"key": "val"}
        result = mymodule.fetch_data()
        self.assertEqual(result["key"], "val")

    def test_context_manager(self):
        with patch("mymodule.os.remove") as mock_remove:
            mymodule.cleanup()
            mock_remove.assert_called_once_with("tmp.txt")
```

### assert_called

```python
mock.assert_called()                  # вызывался
mock.assert_called_once()             # один раз
mock.assert_called_with(arg, kw=val)  # с конкретными аргументами
mock.assert_called_once_with(arg)     # один раз с аргументом
mock.assert_any_call(arg)             # хотя бы раз с аргументом
mock.assert_not_called()              # не вызывался
```

## 8. TestLoader и TestSuite

```python
import unittest

# загрузка тестов
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# из модуля
suite.addTests(loader.loadTestsFromModule(test_module))
# из класса
suite.addTests(loader.loadTestsFromTestCase(TestMath))
# из имени
suite.addTests(loader.loadTestsFromName("test_module.TestMath.test_add"))

# запуск
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
```

## 9. Структура тестов

```
tests/
├── __init__.py
├── test_math.py
├── test_strings.py
└── test_api.py
```

```python
# __init__.py — собрать все
import unittest

def load_tests(loader, standard_tests, pattern):
    suite = unittest.TestSuite()
    suite.addTests(loader.discover("tests"))
    return suite
```

## 10. pytest с unittest

```python
import pytest

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

# можно запускать pytest test_module.py
# pytest поддерживает unittest.TestCase
```

## 11. unittest vs pytest

| | unittest | pytest |
|---|---|---|
| Встроен | ✅ | ❌ |
| Assert | `self.assertEqual(...)` | `assert ...` |
| Фикстуры | `setUp` / `tearDown` | `@pytest.fixture` |
| Параметризация | `subTest()` | `@pytest.mark.parametrize` |
| Плагины | Нет | Множество |
| Код | Более многословный | Лаконичный |
| Популярность | Легаси | Стандарт |
