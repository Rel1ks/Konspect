# yapf — Yet Another Python Formatter

**yapf** — форматтер кода от Google. В отличие от Black, имеет множество настроек стиля.

## 1. Установка

```bash
pip install yapf
```

## 2. Использование

```bash
# форматирование файла
yapf script.py

# in-place (изменить файл)
yapf -i script.py

# показать diff
yapf -d script.py

# форматировать папку
yapf -ir src/

# verbose
yapf -v -i script.py
```

## 3. Стили

yapf поддерживает несколько встроенных стилей.

```bash
yapf --style pep8 script.py
yapf --style google script.py
yapf --style facebook script.py
yapf --style chromium script.py
```

### Google Style (по умолчанию)

```python
# google style:
def function(a, b, c, d, e, f, g):
    pass

result = (a + b + c + d + e + f + g)

# однострочные if
if x: pass
```

### PEP 8 Style

```python
# pep8 style:
def function(a, b, c, d, e, f, g):
    pass

result = (a + b + c + d + e + f + g)

# if на отдельной строке
if x:
    pass
```

## 4. Настройка .style.yapf

```python
# .style.yapf
[style]
based_on_style = pep8
column_limit = 100
indent_width = 4
use_tabs = false
spaces_before_comment = 2

# отступы
dedent_closing_brackets = true
split_before_first_argument = true
split_before_named_first_argument = true

# пробелы
spaces_around_power_operator = true
spaces_around_default_or_equals = true

# строки
split_all_top_level_comma_separated_values = true
split_penalty_import_names = 30
coalesce_brackets = false

# пустые строки
blank_line_before_class_docstring = false
blank_line_before_module_docstring = false
```

## 5. pyproject.toml

```toml
[tool.yapf]
based_on_style = "pep8"
column_limit = 100
indent_width = 4
dedent_closing_brackets = true
split_before_first_argument = true
spaces_around_power_operator = true
```

## 6. Основные настройки

| Параметр | Описание | По умолчанию |
|---|---|---|
| `column_limit` | Максимальная длина строки | 80 |
| `indent_width` | Ширина отступа | 4 |
| `use_tabs` | Использовать табуляцию | false |
| `based_on_style` | Базовый стиль | pep8 |
| `dedent_closing_brackets` | Отступ закрывающей скобки | false |
| `split_before_first_argument` | Перенос перед первым аргументом | false |
| `split_before_named_first_argument` | Перенос перед именованным аргументом | false |
| `spaces_before_comment` | Пробелов перед комментарием | 2 |
| `spaces_around_power_operator` | Пробелы вокруг `**` | false |
| `blank_line_before_class_docstring` | Пустая строка перед docstring класса | false |
| `split_all_top_level_comma_separated_values` | Разделять значения через запятую | false |
| `coalesce_brackets` | Сжимать пустые скобки | false |

## 7. yapf в редакторах

### VS Code

```json
{
    "python.formatting.provider": "yapf",
    "python.formatting.yapfArgs": ["--style", ".style.yapf"],
    "editor.formatOnSave": true
}
```

### PyCharm

```
Settings → Tools → External Tools → Add
Program: yapf
Arguments: -i "$FilePath$"
```

## 8. yapf vs Black

```python
# Исходный код:
x = { 'a':37,'b':42,'c':9273,
'd': 12 }

# yapf (pep8):
x = {'a': 37, 'b': 42, 'c': 9273, 'd': 12}

# Black:
x = {"a": 37, "b": 42, "c": 9273, "d": 12}
```

| | yapf | Black |
|---|---|---|
| Настройка | **Гибкая** | Минимальная |
| Стили | Google, PEP 8, etc. | Один стиль |
| Философия | Настраиваемый | «Бескомпромиссный» |
| Скорость | Средняя | Средняя |
| Кавычки | Не меняет | Двойные |
| Команда | Google | PyPI |

## 9. Примеры форматирования

```python
# до
def func(a,b,c):
   return a+ b +c

# yapf (pep8):
def func(a, b, c):
    return a + b + c
```

```python
# длинные строки
def func(a, b, c, d, e, f, g, h, i, j):
    pass

# с column_limit = 79:
def func(a, b, c, d, e, f, g,
         h, i, j):
    pass
```

## 10. Отключение yapf

```python
# yapf: disable
d = {'a':   1,
     'b':   2,
     'c':   3}
# yapf: enable

# для одной строки
d = {'a': 1, 'b': 2}  # yapf: disable
```
