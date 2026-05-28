# pyproject.toml

**pyproject.toml** — стандартный файл конфигурации Python-проекта (PEP 517, PEP 518, PEP 621).

## 1. Зачем нужен

- Определяет систему сборки (build-backend)
- Содержит метаданные проекта (имя, версия, зависимости)
- Настройки инструментов (ruff, black, pytest)
- Заменяет `setup.py`, `setup.cfg`, `MANIFEST.in`

## 2. Базовая структура

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "Описание пакета"
readme = "README.md"
authors = [
    {name = "Имя", email = "email@example.com"}
]
license = {text = "MIT"}
requires-python = ">=3.9"
dependencies = [
    "requests>=2.31.0",
]
```

## 3. Build-system

Определяет, какой инструмент собирает пакет.

```toml
# setuptools (классический)
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

# flit (лёгкий)
[build-system]
requires = ["flit_core>=3.8"]
build-backend = "flit_core.buildapi"

# poetry
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

# pdm
[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"

# hatch
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# meson-py (C/C++ расширения)
[build-system]
requires = ["meson-python"]
build-backend = "mesonpy"
```

## 4. Project metadata

```toml
[project]
name = "my-package"
version = "0.1.0"
description = "Описание моего пакета"
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
authors = [
    {name = "Имя", email = "email@example.com"}
]
maintainers = [
    {name = "Другое имя", email = "other@example.com"}
]
keywords = ["example", "python", "tutorial"]

classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

dependencies = [
    "requests>=2.31.0",
    "click>=8.0",
]

[project.urls]
Homepage = "https://github.com/user/my-package"
Documentation = "https://my-package.readthedocs.io"
Repository = "https://github.com/user/my-package"
"Bug Tracker" = "https://github.com/user/my-package/issues"

[project.scripts]
my-cli = "my_package.cli:main"

[project.gui-scripts]
my-gui = "my_package.gui:main"

[project.entry-points."my_plugin"]
my-plugin = "my_package.plugin:register"
```

## 5. Optional dependencies (groups)

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.3.0",
    "black>=24.0",
    "mypy>=1.8",
]
test = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
]
docs = [
    "mkdocs>=1.5",
    "mkdocs-material>=9.0",
]
all = [
    "my-package[dev,test,docs]",
]
```

```bash
pip install my-package[dev]
pip install my-package[test]
pip install my-package[all]
```

## 6. Dynamic version

```toml
[project]
name = "my-package"
dynamic = ["version"]

[tool.setuptools.dynamic]
version = {attr = "my_package.__version__"}
```

```python
# my_package/__init__.py
__version__ = "0.1.0"
```

### Из Git

```toml
[tool.setuptools_scm]
```

## 7. Настройки инструментов

### ruff

```toml
[tool.ruff]
target-version = "py39"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[tool.ruff.format]
quote-style = "double"
```

### black

```toml
[tool.black]
line-length = 100
target-version = ["py39"]
skip-string-normalization = false
```

### pytest

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short"
```

### mypy

```toml
[tool.mypy]
python_version = "3.9"
strict = true
ignore_missing_imports = true
```

### coverage

```toml
[tool.coverage.run]
source = ["my_package"]
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = ["pragma: no cover", "def __repr__"]
```

### isort

```toml
[tool.isort]
profile = "black"
line_length = 100
```

## 8. setuptools-specific

```toml
[tool.setuptools.packages.find]
where = ["src"]
include = ["my_package*"]
exclude = ["my_package.tests*"]

[tool.setuptools.package-data]
my_package = ["*.json", "*.yaml"]

[tool.setuptools]
include-package-data = true
```

## 9. Poetry-Specific

```toml
[tool.poetry]
name = "my-package"
version = "0.1.0"
description = ""
authors = ["Имя <email@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.31.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## 10. Пример полного файла

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "Утилиты для работы с данными"
readme = "README.md"
authors = [
    {name = "Имя", email = "email@example.com"}
]
license = {text = "MIT"}
requires-python = ">=3.9"
keywords = ["utils", "data"]

dependencies = [
    "requests>=2.31.0",
    "click>=8.1",
    "rich>=13.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.3.0",
    "mypy>=1.8",
]
docs = [
    "mkdocs>=1.5",
]

[project.urls]
Homepage = "https://github.com/user/my-package"
Issues = "https://github.com/user/my-package/issues"

[project.scripts]
my-app = "my_package.cli:app"

[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.coverage.run]
source = ["my_package"]

[tool.setuptools.packages.find]
where = ["src"]
```

## 11. PEP 621 vs setup.py

| Поле | pyproject.toml | setup.py |
|---|---|---|
| Метаданные | `[project]` | `setup(name=...)` |
| Зависимости | `dependencies` | `install_requires` |
| Dev | `[project.optional-dependencies]` | `extras_require` |
| CLI | `[project.scripts]` | `entry_points` |
| Сборка | `[build-system]` | `setup()` |
| Динамическое | `dynamic` | `version=...` |
