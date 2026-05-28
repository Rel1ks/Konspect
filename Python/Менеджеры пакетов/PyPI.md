# PyPI — Python Package Index

**PyPI** (Python Package Index) — репозиторий пакетов Python. pip по умолчанию устанавливает пакеты именно оттуда.

## 1. Основное

```bash
# URL: https://pypi.org/
# pip скачивает пакеты с pypi.org

# установка из PyPI
pip install requests

# pip ищет на pypi.org/simple/
# https://pypi.org/simple/requests/
```

## 2. Поиск пакетов

```bash
# через pip (не работает с 2021)
# pip search requests  # deprecated

# через веб-интерфейс
# https://pypi.org/search/?q=requests

# через API
# https://pypi.org/pypi/requests/json
```

## 3. Структура пакета на PyPI

```bash
# каждый пакет имеет страницу:
# https://pypi.org/project/requests/
# https://pypi.org/project/requests/2.31.0/  # конкретная версия

# метаданные:
#   name, version, author, license
#   description, keywords, classifiers
#   dependencies, python_requires
```

## 4. Загрузка своего пакета на PyPI

### Регистрация

```bash
# создать аккаунт: https://pypi.org/account/register/
# получить API-токен: https://pypi.org/manage/account/token/
```

### Подготовка

```bash
# создать проект
my-package/
├── pyproject.toml
├── README.md
├── LICENSE
└── src/
    └── my_package/
        ├── __init__.py
        └── module.py
```

### pyproject.toml (PEP 621)

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "Описание моего пакета"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Имя", email = "email@example.com"}
]
requires-python = ">=3.9"
dependencies = [
    "requests>=2.31.0",
]
keywords = ["example", "tutorial"]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
]

[project.urls]
Homepage = "https://github.com/user/my-package"
Documentation = "https://my-package.readthedocs.io"
Source = "https://github.com/user/my-package"
```

### setup.py (старый стиль)

```python
from setuptools import setup, find_packages

setup(
    name="my-package",
    version="0.1.0",
    description="Описание пакета",
    author="Имя",
    author_email="email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.31.0",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
```

### Сборка и публикация

```bash
# установить необходимые инструменты
pip install build twine

# сборка
python -m build
# создаёт dist/my_package-0.1.0.tar.gz
# создаёт dist/my_package-0.1.0-py3-none-any.whl

# проверка
twine check dist/*

# публикация на тестовый PyPI
twine upload -r testpypi dist/*

# публикация на PyPI
twine upload dist/*

# с API-токеном
twine upload dist/* -u __token__ -p pypi-xxxxxxxx
```

## 5. TestPyPI

Тестовый репозиторий для проверки перед публикацией.

```bash
# URL: https://test.pypi.org/
# установка с testpypi
pip install -i https://test.pypi.org/simple/ my-package

# публикация на testpypi
twine upload -r testpypi dist/*

# настройка ~/.pypirc
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-xxxxxxxx

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-xxxxxxxx
```

## 6. Версионирование (SemVer)

```
major.minor.patch
1.0.0 — первая стабильная
1.2.3 — major.minor.patch
```

| Часть | Когда менять |
|---|---|
| **major** | Несовместимые изменения API |
| **minor** | Новая функциональность (обратно совместимо) |
| **patch** | Исправление багов (обратно совместимо) |

```bash
# pre-release
1.0.0a1  # alpha
1.0.0b1  # beta
1.0.0rc1 # release candidate

# dev
1.0.0.dev1

# post
1.0.0.post1
```

## 7. Классификаторы

```bash
# trove classifiers — метки для категоризации пакета
# https://pypi.org/classifiers/

Development Status :: 5 - Production/Stable
Programming Language :: Python :: 3
Programming Language :: Python :: 3.12
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Topic :: Internet :: WWW/HTTP
```

## 8. README (PyPI форматирование)

PyPI поддерживает Markdown (с PyPandoc) и reStructuredText.

```markdown
# My Package

## Установка
```bash
pip install my-package
```

## Использование
```python
from my_package import hello
print(hello())
```

## Лицензия
MIT
```

Настройка в pyproject.toml:

```toml
[project]
readme = "README.md"
```

## 9. Лицензии

```toml
[project]
# SPDX identifiers
license = {text = "MIT"}
license = {text = "Apache-2.0"}
license = {text = "GPL-3.0-only"}
```

## 10. Автоматизация публикации

### GitHub Actions

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install build twine
      - run: python -m build
      - run: twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

## 11. Альтернативные репозитории

```bash
# частный PyPI (devpi, pypiserver, AWS CodeArtifact)
pip install -i https://my-private-pypi.com/simple my-package

# зеркала
# Яндекс: https://mirror.yandex.ru/pypi/simple
# Tsinghua: https://pypi.tuna.tsinghua.edu.cn/simple
```

## 12. PyPI vs Conda-forge

| | PyPI | Conda-forge |
|---|---|---|
| Установка | `pip install` | `conda install -c conda-forge` |
| Пакеты | Только Python | Python + C/R/... |
| Бинарные | Собирает на лету | Готовые бинарники |
| Зависимости | pip разрешает | Conda разрешает |
| Модерация | Автоматическая | Ревью |
