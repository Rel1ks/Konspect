# Форматирование кода (Code Formatting)

**Форматирование кода** — автоматическое приведение стиля кода к единым правилам: отступы, пробелы, кавычки, длина строк.

## 1. Зачем нужно

- Единый стиль во всём проекте
- Без споров в команде
- Автоматизация (не нужно думать о форматировании)
- Улучшает читаемость кода

## 2. PEP 8 — стандарт оформления

**PEP 8** — официальный гайд по стилю Python.

```python
# 1. Отступы — 4 пробела (не табуляция)
def func():
    pass

# 2. Максимальная длина строки — 79 символов (можно 88-100)
long_line = "это очень длинная строка, которая не должна " \
            "превышать определённую длину"

# 3. Две пустые строки между функциями
# 4. Одна пустая строка между методами класса
# 5. Пробелы вокруг операторов: a + b, a == b, a = 5
# 6. После запятых: func(a, b, c)
```

## 3. Black

**Black** — самый популярный форматтер. «Бескомпромиссный» — стиль не настраивается.

```bash
pip install black

# форматирование файла
black script.py

# форматирование папки
black src/

# проверка без изменений
black --check src/

# показать, что изменится
black --diff src/
```

```python
# До:
def foo(  a,b,c ) :
    return[ a, b,c ]

# После:
def foo(a, b, c):
    return [a, b, c]
```

### pyproject.toml

```toml
[tool.black]
line-length = 100
target-version = ["py312"]
skip-string-normalization = false
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.mypy_cache
  | \.venv
)/
'''
```

## 4. Ruff

**Ruff** — форматтер + линтер на Rust. Заменяет Black, Flake8, isort.

```bash
pip install ruff

# форматирование
ruff format src/

# линтинг
ruff check src/

# исправление автоматическое
ruff check --fix src/

# формат + линтинг одновременно
ruff check --fix src/ && ruff format src/
```

### pyproject.toml

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Ruff vs Black

```bash
# Ruff форматирует быстрее Black (на Rust)
# Ruff заменяет Black + isort + flake8 + pyupgrade
# Один инструмент вместо четырёх
```

## 5. isort

**isort** — сортировка импортов.

```bash
pip install isort

# сортировка
isort script.py
isort src/

# проверка
isort --check src/
```

```python
# До:
import os
import sys
from flask import Flask
import requests
from typing import List

# После:
import os
import sys
from typing import List

import requests
from flask import Flask
```

### pyproject.toml

```toml
[tool.isort]
profile = "black"
line_length = 100
known_first_party = ["my_project"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
```

## 6. autopep8

**autopep8** — форматтер на основе PEP 8. Более гибкий, чем Black.

```bash
pip install autopep8

autopep8 script.py
autopep8 --in-place script.py
autopep8 --aggressive --in-place script.py
```

## 7. yapf

**yapf** — форматтер от Google. Много настроек.

```bash
pip install yapf

yapf script.py
yapf -i script.py  # in-place
yapf -d script.py  # diff
```

## 8. pyproject.toml — общий

```toml
[tool.black]
line-length = 100

[tool.isort]
profile = "black"
line-length = 100

[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[tool.ruff.format]
quote-style = "double"
```

## 9. EditorConfig

```ini
# .editorconfig
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false
```

## 10. pre-commit hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
```

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## 11. Сравнение инструментов

| Инструмент | Тип | Скорость | Настройка | Язык |
|---|---|---|---|---|
| **Black** | Форматтер | Средняя | Минимальная | Python |
| **Ruff** | Форматтер + линтер | **Очень быстрый** | Средняя | Rust |
| **isort** | Сортировка импортов | Средняя | Средняя | Python |
| **autopep8** | Форматтер | Средняя | Гибкая | Python |
| **yapf** | Форматтер | Средняя | **Гибкая** | Python |

## 12. CI/CD

```yaml
# GitHub Actions
- name: Check formatting
  run: |
    ruff format --check src/
    ruff check src/

# или
- name: Black check
  run: black --check src/

- name: isort check
  run: isort --check src/
```
