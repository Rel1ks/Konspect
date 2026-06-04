# Black

**Black** — «бескомпромиссный» форматтер Python-кода. Минимум настроек, единый стиль.

## 1. Установка

```bash
pip install black
```

## 2. Использование

```bash
# отформатировать файл
black script.py

# отформатировать папку
black src/

# проверить, не изменяя
black --check src/

# показать diff
black --diff src/

# verbose
black -v src/

# тихий режим
black -q src/
```

## 3. Основные правила

```python
# 1. Двойные кавычки (по умолчанию)
name = "Анна"
text = "Hello"

# 2. Пробелы вокруг операторов
x = a + b
result = (a + b) * c

# 3. Последняя запятая
items = [
    1,
    2,
    3,
]

# 4. Закрывающая скобка на отдельной строке
result = some_function(
    argument1,
    argument2,
    argument3,
)

# 5. Магическая запятая — если есть запятая, Black раскрывает
# Без запятой — в строку
items = [1, 2, 3]  # в строку
items = [
    1,
    2,
    3,  # раскрыто
]
```

## 4. Форматирование в действии

```python
# До:
def foo(  a,b,c ) :
    return[ a, b,c ]

# После:
def foo(a, b, c):
    return [a, b, c]
```

```python
# До:
x = { 'a':37,'b':42,
'c':9273 }

# После:
x = {"a": 37, "b": 42, "c": 9273}
```

## 5. pyproject.toml

```toml
[tool.black]
line-length = 100
target-version = ["py312"]
skip-string-normalization = false
skip-magic-trailing-comma = false

# включать/исключать
include = '\.pyi?$'
extend-exclude = '''
/(
    \.mypy_cache
  | \.venv
  | \.git
  | migrations
)/
'''

# Force-exclude — всегда исключать
force-exclude = '''
/legacy/
'''
```

## 6. Настройки

| Параметр | Описание | По умолчанию |
|---|---|---|
| `line-length` | Максимальная длина строки | 88 |
| `target-version` | Версии Python | `["py39", "py310", "py311", "py312"]` |
| `skip-string-normalization` | Не менять кавычки | false |
| `skip-magic-trailing-comma` | Не добавлять магические запятые | false |
| `fast` | Быстрый режим (без безопасности) | false |
| `preview` | Экспериментальные фичи | false |

## 7. Preview режим

```bash
black --preview script.py
```

```python
# preview — более агрессивное форматирование
# 1. Пустые строки в скобках
result = (
    a + b + c
)

# 2. Однострочные docstring
def func():
    """Simplify docstring."""

# 3. Форматирование trailing commas
```

## 8. Кавычки

Black по умолчанию использует двойные кавычки.

```bash
# не менять кавычки
black --skip-string-normalization script.py
```

```python
# До
s = 'hello'
t = "world"
u = 'mixed "quotes"'

# После (по умолчанию)
s = "hello"
t = "world"
u = 'mixed "quotes"'  # не меняется из-за внутренних кавычек
```

## 9. Интеграция с редакторами

### VS Code

```json
{
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true
    }
}
```

### PyCharm

```
File → Settings → Tools → File Watchers → + → Black
Arguments: $FilePath$
Output paths to refresh: $FilePath$
Working directory: $ProjectFileDir$
```

## 10. pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black-pre-commit-mirror
    rev: 24.2.0
    hooks:
      - id: black
        args: [--line-length=100]
```

```bash
pip install pre-commit
pre-commit install
pre-commit run black --all-files
```

## 11. Black в CI

```yaml
# GitHub Actions
- name: Check formatting
  run: black --check --diff src/
```

## 12. Magic Trailing Comma

```python
# если есть запятая в конце — Black раскрывает
x = {
    1,
    2,
}  # останется раскрытым

# если нет запятой — Black может сжать
x = {
    1, 2, 3
}  # сожмёт: {1, 2, 3}
```

## 13. Black vs yapf vs autopep8

| | Black | yapf | autopep8 |
|---|---|---|---|
| Настройка | Минимальная | **Гибкая** | Гибкая |
| Стиль | Один | Google / pep8 / свой | PEP 8 |
| Философия | Не обсуждается | Настраиваемый | PEP 8 compl. |
| Скорость | Средняя | Средняя | Средняя |
| Популярность | **Самая высокая** | Средняя | Средняя |
| Команда | Python Software | Google | H. Krekel |

## 14. Отключение Black

```python
# fmt: off
# fmt: on

# отключить для блока
# fmt: off
d = {    'a'  :   1,
    'b':2
}
# fmt: on

# для отдельной строки — нельзя
# Используйте # fmt: off/on вокруг
```
