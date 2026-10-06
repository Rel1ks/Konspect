# PDM — менеджер пакетов и зависимостей

**PDM (Python Development Master)** — современный менеджер пакетов с поддержкой PEP 582 (локальные пакеты без виртуального окружения) и PEP 621 (pyproject.toml).

## 1. Установка

```bash
# через pip
pip install pdm

# через официальный установщик (Windows)
# (Invoke-WebRequest -Uri https://pdm-project.org/install-pdm.py -UseBasicParsing).Content | python -

# проверка
pdm --version
```

## 2. Создание проекта

```bash
# создать новый проект
pdm init

# ответить на вопросы — создаст pyproject.toml

# инициализация в существующей папке
pdm init
```

## 3. `pyproject.toml`

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Описание проекта"
authors = [{name = "Имя", email = "email@example.com"}]
license = {text = "MIT"}
requires-python = ">=3.9"
dependencies = [
    "requests>=2.31.0",
    "flask>=3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "black>=24.0",
]
docs = [
    "mkdocs>=1.5",
]

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"

[tool.pdm]
# настройки PDM
package-dir = "src"  # исходники в src/
```

## 4. Управление зависимостями

```bash
# установка зависимостей (из pyproject.toml + pdm.lock)
pdm install

# установка без dev
pdm install --production

# установка только определённой группы
pdm install -G dev
pdm install -G docs

# добавление пакета
pdm add requests

# с указанием версии
pdm add "requests>=2.31.0"

# как dev-зависимость
pdm add -d pytest
pdm add --dev pytest

# в группу
pdm add -G test pytest

# удаление
pdm remove requests

# обновление всех зависимостей
pdm update

# обновление конкретного пакета
pdm update requests

# проверка устаревших
pdm outdated
```

## 5. Команды

```bash
# выполнить команду в окружении
pdm run python script.py
pdm run pytest

# запуск shell
pdm shell

# показать установленные пакеты
pdm list

# дерево зависимостей
pdm list --graph

# информация о пакете
pdm show requests

# проверить pyproject.toml
pdm validate

# очистить кеш
pdm cache clear
```

## 6. PEP 582 — локальные пакеты (без venv)

PDM поддерживает установку пакетов в `__pypackages__` рядом с проектом.

```bash
# включить режим PEP 582
pdm config python.use_venv false

# после этого пакеты устанавливаются в __pypackages__
pdm add requests
```

```python
# Python сам находит пакеты в __pypackages__ (PEP 582)
# без активации окружения, без source/activate
python script.py
```

```bash
# переключение обратно на venv
pdm config python.use_venv true
```

## 7. Виртуальное окружение

```bash
# PDM автоматически создаёт venv (как Poetry)

# информация об окружении
pdm info

# показать пути
pdm info --env

# список окружений
pdm venv list

# создать новое окружение
pdm venv create 3.12

# удалить окружение
pdm venv remove my-env

# активировать другое окружение
pdm use .venv
pdm use 3.12  # создать с Python 3.12

# venv в папке проекта
pdm config venv.in-project true
```

## 8. Зависимости — расширенный синтаксис

```toml
[project]
dependencies = [
    "requests>=2.31.0",
    "click>=8.0,<9.0",
    "numpy~=1.24",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
]
test = [
    "pytest>=8.0",
]
```

### Из разных источников

```toml
# прямое указание в pdm add
pdm add "my-lib @ git+https://github.com/user/my-lib.git@main"
pdm add "my-lib @ https://example.com/my-lib.tar.gz"
pdm add "my-lib @ path:../my-lib"

# или в pyproject.toml:
[tool.pdm.dev-dependencies]
dev = [
    "my-lib @ git+https://github.com/user/my-lib.git",
]
```

## 9. Сборка и публикация

```bash
# сборка (wheel + sdist)
pdm build

# публикация на PyPI
pdm publish

# публикация на тестовый PyPI
pdm publish -r test-pypi

# настройка репозитория
pdm config repository.pypi.url https://upload.pypi.org/legacy/
pdm config repository.test-pypi.url https://test.pypi.org/legacy/
```

## 10. Запуск скриптов

```toml
[project.scripts]
start = "my_project.cli:main"
test = "pytest:main"
lint = "ruff:check"
```

```bash
pdm run start
pdm run lint
```

## 11. PDm и монorepo

```bash
# установка из нескольких проектов
pdm add --project ../other-project
```

## 12. Lock-файл

```bash
# pdm.lock создаётся автоматически
# фиксирует точные версии

# принудительное обновление lock
pdm lock

# установка из lock
pdm install

# использование lock в CI
pdm install --frozen-lockfile  # не менять lock
```

## 13. Настройки

```bash
# глобальные настройки
pdm config
pdm config python.path C:\Python312\python.exe
pdm config cache_dir C:\Users\user\.cache\pdm

# настройка зеркал PyPI
pdm config pypi.url https://mirror.example.com/simple
```

## 14. pdm vs poetry

| Возможность | PDM | Poetry |
|---|---|---|
| Стандарты | PEP 582, PEP 621 | Свой формат |
| Lock-файл | `pdm.lock` | `poetry.lock` |
| PEP 582 | Поддерживает (без venv) | Нет |
| pyproject.toml | PEP 621 (стандарт) | Свой [tool.poetry] |
| Скорость | Быстрый (parallel install) | Средний |
| Плагины | Есть | Нет |
| Monorepo | Поддерживает | Сложнее |
| PEP 621 | Да (стандартные поля) | Нет |
| Source-зависимости | Git, URL, path | Git, URL, path |
