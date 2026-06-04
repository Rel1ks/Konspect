# Doctest

**doctest** — встроенный модуль для тестирования через примеры в docstring.

## 1. Базовый пример

```python
def add(a, b):
    """
    Складывает два числа.

    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    >>> add(0, 0)
    0
    """
    return a + b
```

```bash
python -m doctest module.py          # без вывода если ОК
python -m doctest module.py -v       # verbose
```

## 2. Запуск из кода

```python
import doctest

# запустить doctest для модуля
doctest.testmod()

# с verbose
doctest.testmod(verbose=True)

# запустить для конкретной функции
doctest.run_docstring_examples(add, globals())
```

```python
if __name__ == "__main__":
    import doctest
    doctest.testmod()
```

## 3. Формат

```python
def multiply(a, b):
    """
    Умножает два числа.

    Примеры:

    >>> multiply(2, 3)
    6

    >>> multiply(4, 5)
    20

    >>> multiply(-1, 5)
    -5
    """
    return a * b
```

### Исключения

```python
def divide(a, b):
    """
    Делит a на b.

    >>> divide(10, 2)
    5.0
    >>> divide(10, 0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero
    """
    return a / b
```

### Многострочный вывод

```python
def get_items():
    """
    >>> get_items()
    ['a', 'b', 'c']
    """
    return ["a", "b", "c"]
```

```python
def print_items():
    """
    >>> print_items()
    a
    b
    c
    """
    for item in ["a", "b", "c"]:
        print(item)
```

## 4. Директивы

```python
def format_price(price):
    """
    >>> format_price(10.0)
    '10.00 руб.'
    >>> format_price(10.5)
    '10.50 руб.'
    >>> format_price(10.555)  # doctest: +ELLIPSIS
    '10.56...'
    """
    return f"{price:.2f} руб."
```

| Директива | Описание |
|---|---|
| `+ELLIPSIS` | `...` совпадает с любым текстом |
| `+NORMALIZE_WHITESPACE` | Пробелы не важны |
| `+SKIP` | Пропустить тест |
| `+IGNORE_EXCEPTION_DETAIL` | Игнорировать детали исключения |
| `+DONT_ACCEPT_TRUE_FOR_1` | `True` ≠ `1` |

```python
# глобально в вызове
doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
```

## 5. Doctest в файлах

```txt
# readme.txt
Пример использования:

>>> from mymodule import add
>>> add(2, 3)
5
>>> add(10, 20)
30
```

```bash
python -m doctest readme.txt -v
```

## 6. Doctest с pytest

```bash
pytest --doctest-modules          # найти doctest в модулях
pytest --doctest-glob="*.rst"     # .rst файлы
pytest --doctest-report=udiff     # diff формат
```

```python
# conftest.py
collect_ignore = ["setup.py"]
```

## 7. Ограничения

```python
# 1. float — не точное сравнение
# плохо:
def div(a, b):
    """
    >>> div(1, 3)
    0.3333333333333333
    """
    return a / b

# лучше:
def div(a, b):
    """
    >>> div(1, 3)  # doctest: +ELLIPSIS
    0.333...
    """
    return a / b

# 2. dict — порядок не гарантирован
# плохо:
def get_dict():
    """
    >>> get_dict()
    {'a': 1, 'b': 2}
    """
    return dict(b=2, a=1)
```

## 8. Doctest vs unittest

| | Doctest | unittest |
|---|---|---|
| Где живёт | В docstring | В отдельных файлах |
| Читаемость | Как документация | Классы/методы |
| Сложные тесты | Тяжело | Легко |
| setUp/tearDown | Нет | Есть |
| Моки | Нет | `unittest.mock` |
| Использование | Дополнение | Основной фреймворк |

## 9. Best Practices

```python
# 1. Короткие, наглядные примеры
# 2. Покрытие основных случаев
# 3. ELLIPSIS для float / длинного вывода
# 4. Не заменять unittest, а дополнять
# 5. Обновлять docstring при изменении кода

def validate_email(email):
    """
    Проверяет email.

    >>> validate_email("user@example.com")
    True
    >>> validate_email("invalid")
    False
    >>> validate_email("")
    False
    """
    return "@" in email and "." in email.split("@")[-1]
```
