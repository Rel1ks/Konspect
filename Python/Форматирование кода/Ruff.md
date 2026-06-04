# Ruff

**Ruff** — очень быстрый линтер и форматтер для Python, написан на Rust. Замена Flake8, isort, Black и другим.

## 1. Установка

```bash
pip install ruff

# или через uv
uv tool install ruff
```

## 2. Быстрый старт

```bash
# линтинг
ruff check src/

# автоисправление
ruff check --fix src/

# форматирование
ruff format src/

# показать diff
ruff format --diff src/

# проверить, не изменяя
ruff format --check src/
```

## 3. pyproject.toml

```toml
[tool.ruff]
target-version = "py312"
line-length = 100

# включать/исключать
include = ["*.py", "*.pyi"]
exclude = ["migrations", ".venv"]

# правила линтинга
[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "S", "RUF"]
ignore = ["E501"]  # line length — проверяет Ruff formatter

[tool.ruff.lint.per-file-ignores]
"tests/*.py" = ["S101"]   # allow assert in tests

# настройки форматтера
[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
docstring-code-format = true
```

## 4. Линтинг (ruff check)

### Основные группы правил

| Код | Категория | Пример |
|---|---|---|
| `E` | pycodestyle errors | `E225 missing whitespace` |
| `W` | pycodestyle warnings | `W291 trailing whitespace` |
| `F` | Pyflakes | `F401` — неиспользуемый импорт |
| `I` | isort | сортировка импортов |
| `N` | PEP 8 naming | `N802` — имя функции не с lower_case |
| `UP` | pyupgrade | синтаксис новой версии Python |
| `B` | flake8-bugbear | баги и подозрительный код |
| `S` | flake8-bandit | безопасность |
| `SIM` | flake8-simplify | упрощение кода |
| `PL` | Pylint | `PLR0913` — too many arguments |
| `RUF` | Специфичные для Ruff | |

```bash
# показать доступные правила
ruff rule E501

# список всех правил
ruff check --show-settings src/
```

## 5. Форматирование (ruff format)

Совместимость с Black — Ruff форматирует почти идентично Black.

```bash
ruff format src/
ruff format --check src/
```

```python
# До
def foo(  a,b,c ) :
    return[ a, b,c ]

# После
def foo(a, b, c):
    return [a, b, c]
```

### Настройки форматтера

| Параметр | Описание | По умолчанию |
|---|---|---|
| `quote-style` | Кавычки: `double`, `single`, `preserve` | `double` |
| `indent-style` | Отступы: `space`, `tab` | `space` |
| `line-ending` | `lf`, `cr-lf`, `auto` | `auto` |
| `docstring-code-format` | Форматировать код в docstring | `false` |
| `docstring-code-line-length` | Длина строки в docstring | `dynamic` |

## 6. Автоисправление (--fix)

```bash
# исправить все, что можно
ruff check --fix src/

# неприменимые — показать
ruff check --show-fixes src/

# добавить NOQA
ruff check --add-noqa src/
```

```python
# ruff check --fix исправит:
import os  # F401 — удалит
x = 1 ; y = 2  # E703 — уберёт ;
```

## 7. pre-commit

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## 8. vs code

```json
{
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": true
        }
    },
    "ruff.lineLength": 100
}
```

## 9. CI

```yaml
- name: Lint with Ruff
  run: |
    ruff check --output-format=github
    ruff format --check
```

## 10. Ruff vs аналоги

| | Ruff | Flake8 | Black | isort | Pylint |
|---|---|---|---|---|---|
| Скорость | **x10-100** | Средняя | Средняя | Средняя | Медленная |
| Форматтер | ✅ | ❌ | ✅ | ❌ | ❌ |
| isort | ✅ | ❌ | ❌ | ✅ | ❌ |
| Rust | ✅ | ❌ | ❌ | ❌ | ❌ |
| Все в одном | ✅ | ❌ | ❌ | ❌ | ❌ |

## 11. Отключение правил

```python
# для строки
x = 1  # noqa: E501

# для блока
# ruff: noqa: F401
import os
import sys
# ruff: noqa

# в pyproject.toml
[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401", "F403"]

# отключить форматирование
# ruff: fmt: off
x = {     'a':1 }
# ruff: fmt: on
```

## 12. Полезные команды

```bash
# показать конфигурацию
ruff check --show-settings

# чистить кэш
ruff clean

# показать версию
ruff version

# сгенерировать документацию по правилам
ruff rule --all
```
