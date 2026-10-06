# Poetry — менеджер пакетов и зависимостей

**Poetry** — инструмент для управления зависимостями, сборки и публикации Python-пакетов.

## 1. Установка

```bash
# через pip (рекомендуется)
pip install poetry

# через официальный установщик (Windows)
# (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# проверка
poetry --version
```

## 2. Создание проекта

```bash
# создать новый проект
poetry new my-project
# структура:
# my-project/
# ├── pyproject.toml
# ├── README.md
# ├── my_project/
# │   └── __init__.py
# └── tests/
#     └── __init__.py

# создать проект внутри существующей папки
poetry init
```

## 3. `pyproject.toml`

Основной файл конфигурации.

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "Описание проекта"
authors = ["Имя <email@example.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.31.0"
numpy = ">=1.21,<2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
black = "^24.0"
ruff = "^0.3.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## 4. Управление зависимостями

```bash
# установка зависимостей (из pyproject.toml + poetry.lock)
poetry install

# установка без dev-зависимостей
poetry install --without dev

# установка только production
poetry install --only main

# добавление пакета
poetry add requests
poetry add "requests>=2.31.0"

# добавление dev-зависимости
poetry add --dev pytest
poetry add -D pytest

# добавление групповой зависимости
poetry add --group test pytest

# удаление пакета
poetry remove requests

# обновление всех зависимостей
poetry update

# обновление конкретного пакета
poetry update requests
```

## 5. Команды

```bash
# активировать виртуальное окружение
poetry shell

# выполнить команду в окружении
poetry run python script.py
poetry run pytest

# показать установленные пакеты
poetry show
poetry show --tree  # дерево зависимостей

# проверить устаревшие пакеты
poetry show --outdated

# проверить конфликты
poetry check
```

## 6. Зависимости — форматы версий

| Формат | Описание | Пример |
|---|---|---|
| `^1.2.3` | Совместимые (>=1.2.3, <2.0) | `^1.2.3` → 1.2.3 до 2.0 |
| `~1.2.3` | (>=1.2.3, <1.3) | |
| `>=1.2.3` | Больше или равно | |
| `>1.2.3` | Строго больше | |
| `<2.0` | Меньше | |
| `>=1.0,<2.0` | Диапазон | |
| `*` | Любая | |
| `1.2.3` | Точная версия | |

## 7. Группы зависимостей

```toml
[tool.poetry.dependencies]
# основные зависимости
flask = "^3.0"

[tool.poetry.group.dev.dependencies]
# для разработки
pytest = "^8.0"
ipython = "^8.0"

[tool.poetry.group.docs.dependencies]
# для документации
mkdocs = "^1.5"

[tool.poetry.group.test.dependencies]
# для тестов (можно назвать по-своему)
pytest-cov = "^4.0"
```

```bash
poetry install --with dev,docs
poetry install --without test
poetry install --only docs
```

## 8. Виртуальное окружение

```bash
# создаётся автоматически при poetry install/add

# просмотр информации об окружении
poetry env info

# список окружений
poetry env list

# удаление окружения
poetry env remove python

# указать версию Python для окружения
poetry env use python3.12

# создать окружение внутри проекта
poetry config virtualenvs.in-project true
```

### Настройка `config`

```bash
# окружение в папке проекта (создаётся .venv)
poetry config virtualenvs.in-project true

# путь к окружениям
poetry config virtualenvs.path

# отключить создание окружения
poetry config virtualenvs.create false
```

## 9. Сборка и публикация

```bash
# сборка пакета (wheel + tar.gz)
poetry build
# создаёт: dist/my_project-0.1.0-py3-none-any.whl

# публикация на PyPI
poetry publish

# публикация на тестовый PyPI
poetry publish -r test-pypi
```

## 10. Зависимости из разных источников

```toml
[tool.poetry.dependencies]
# с PyPI
requests = "^2.31.0"

# из Git
my-lib = {git = "https://github.com/user/my-lib.git", branch = "main"}
my-lib = {git = "https://github.com/user/my-lib.git", rev = "abc1234"}
my-lib = {git = "https://github.com/user/my-lib.git", tag = "v1.0"}

# из локальной папки
my-lib = {path = "../my-lib"}

# с URL
my-lib = {url = "https://example.com/my-lib.tar.gz"}
```

## 11. Скрипты

```toml
[tool.poetry.scripts]
start = "my_project.cli:main"
test = "pytest:main"
```

```bash
poetry run start
```

## 12. Lock-файл

`poetry.lock` фиксирует точные версии всех зависимостей.

```bash
# создать/обновить lock-файл
poetry lock

# установка из lock-файла (точные версии)
poetry install

# если удалить lock и переустановить — версии могут измениться
poetry.lock должен быть в репозитории (git)
```

## 13. poetry vs pip

| Возможность | poetry | pip |
|---|---|---|
| Зависимости | `pyproject.toml` | `requirements.txt` |
| Lock-файл | `poetry.lock` | `pip freeze > requirements.txt` |
| Виртуальное окружение | Автоматически | Вручную (venv) |
| Сборка | `poetry build` | `python -m build` |
| Публикация | `poetry publish` | `twine upload` |
| Dev-зависимости | Группы | Доп. requirements |
| Дерево зависимостей | `poetry show --tree` | `pipdeptree` |
| Разрешение конфликтов | Встроенное | Нет |
