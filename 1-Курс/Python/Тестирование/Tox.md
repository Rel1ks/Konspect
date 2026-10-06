# Tox

**Tox** — инструмент для тестирования в нескольких окружениях (разные версии Python, зависимости). Автоматизация прогона тестов, линтеров, форматтеров.

## 1. Установка

```bash
pip install tox
```

## 2. pyproject.toml

```toml
[project]
name = "myproject"
requires-python = ">=3.10"

[tool.tox]
legacy_tox_ini = """
[tox]
envlist = py310, py311, py312
"""

[tool.tox.env_run_base]
commands = pytest tests/
```

## 3. tox.ini

```ini
[tox]
envlist = py310, py311, py312, lint, typecheck
min_version = 4.0

[testenv]
deps =
    pytest
    pytest-cov
commands =
    pytest tests/ --cov=src/ --cov-report=term-missing

[testenv:lint]
deps = ruff
commands = ruff check src/

[testenv:typecheck]
deps = mypy
commands = mypy src/
```

## 4. Запуск

```bash
tox                  # все окружения
tox -e py312         # только Python 3.12
tox -e lint           # только lint
tox -p               # параллельно
tox -r               # пересоздать окружения
tox --devenv venv    # создать dev окружение
tox list             # список окружений
```

## 5. pyproject.toml (альтернатива)

```toml
[tool.tox]
legacy_tox_ini = """
[tox]
envlist = py310, py311, py312, lint

[testenv]
deps =
    pytest
commands = pytest tests/

[testenv:lint]
deps = ruff
commands = ruff check src/
"""
```

## 6. factor — зависимости и команды

```ini
[tox]
envlist = py{310,311,312}-django{42,50}

[testenv]
deps =
    django42: Django>=4.2,<5.0
    django50: Django>=5.0,<5.1
commands =
    pytest tests/
```

## 7. Переменные окружения

```ini
[testenv]
setenv =
    PYTHONPATH = {toxinidir}/src
    DATABASE_URL = sqlite:///test.db

passenv =
    CI
    GITHUB_ACTIONS
```

## 8. Дополнительные команды

```ini
[testenv]
commands_pre =
    pip install -e .
commands =
    pytest tests/
commands_post =
    echo "Done"
```

## 9. Флаги

```bash
tox -v               # verbose
tox -q               # quiet
tox --showconfig     # показать конфигурацию
tox --help           # справка
```

## 10. Tox в CI

```yaml
# GitHub Actions
- name: Test with tox
  run: tox -e py312

# матрица
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]

steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
  - run: pip install tox
  - run: tox -e py
```

## 11. Tox vs Nox

| | Tox | Nox |
|---|---|---|
| Конфиг | INI (или pyproject.toml) | Python (`noxfile.py`) |
| Гибкость | Шаблоны, факторы | **Максимальная** |
| Кривая обучения | Ниже | Выше |
| Популярность | Стандарт | Меньше |
| Когда выбрать | Стандартный проект | Особая логика |

## 12. Полезные команды

```ini
[tox]
envlist = py310, py311, py312, lint, docs
skip_missing_interpreters = true   # пропустить если нет python

[testenv]
deps =
    -r requirements-dev.txt
commands =
    pytest {posargs:tests/}        # передача аргументов

[testenv:docs]
changedir = docs
deps = sphinx
commands = sphinx-build -b html . build/html
```
