# Sphinx

**Sphinx** — генератор документации из reStructuredText / Markdown. Стандарт для Python-проектов.

## 1. Установка

```bash
pip install sphinx

# тема Read the Docs
pip install sphinx_rtd_theme

# поддержка Markdown
pip install myst-parser
```

## 2. Быстрый старт

```bash
# создать структуру
sphinx-quickstart docs/
# отвечаем на вопросы, разделяем source и build
```

```
docs/
├── source/
│   ├── conf.py       # конфигурация
│   ├── index.rst     # корневой документ
│   └── *_rst         # страницы документации
└── build/            # сгенерированные файлы
```

## 3. conf.py

```python
# docs/source/conf.py
project = "My Project"
author = "Name"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",         # автодокументация из докстрингов
    "sphinx.ext.napoleon",        # Google/NumPy style docstrings
    "sphinx.ext.viewcode",        # ссылки на исходный код
    "sphinx.ext.todo",            # TODO блоки
    "sphinx_rtd_theme",           # тема
    "myst_parser",                # Markdown
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
```

## 4. reStructuredText

```rst
.. My Project documentation master file

Welcome to My Project's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
```

```rst
Installation
============

.. code-block:: bash

   pip install myproject
```

### Основные элементы RST

```rst
Заголовок
=========  # H1

Заголовок
---------  # H2

Заголовок
~~~~~~~~~  # H3

**жирный**
*курсив*

.. code-block:: python

   def hello():
       pass

.. note::
   Это заметка.

.. warning::
   Предупреждение.

Ссылка на `Google <https://google.com>`_

.. image:: img/logo.png
```

## 5. Поддержка Markdown (MyST)

```md
# Заголовок

```{note}
Заметка
```

```{warning}
Предупреждение
```

```{code-block} python
def hello():
    pass
```

Ссылка на {doc}`installation` или {ref}`my-anchor`.
```

## 6. Автодокументация (autodoc)

```python
# mymodule.py

def add(a: int, b: int) -> int:
    """Складывает два числа.

    Args:
        a (int): Первое число.
        b (int): Второе число.

    Returns:
        int: Сумма a и b.

    Example:
        >>> add(2, 3)
        5
    """
    return a + b
```

```rst
.. automodule:: mymodule
   :members:
   :undoc-members:
   :show-inheritance:
```

```rst
.. autoclass:: MyClass
   :members:
   :private-members:
```

### Napoleon — Google style

```python
def func(a, b):
    """Описание.

    Args:
        a: первое.
        b: второе.

    Returns:
        Результат.

    Raises:
        ValueError: если что-то не так.
    """
```

### Napoleon — NumPy style

```python
def func(a, b):
    """Описание.

    Parameters
    ----------
    a : int
        Первое.
    b : int
        Второе.

    Returns
    -------
    int
        Результат.
    """
```

## 7. Сборка

```bash
# HTML
sphinx-build -b html source/ build/html/

# PDF (требуется LaTeX)
sphinx-build -b latex source/ build/latex/

# проще — Makefile от sphinx-quickstart
cd docs/
make html      # Windows: make.bat html
make latexpdf
```

## 8. Публикация

### Read the Docs

1. Зарегистрироваться на https://readthedocs.org
2. Подключить репозиторий
3. Добавить `.readthedocs.yaml`

```yaml
# .readthedocs.yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.12"

sphinx:
  configuration: docs/source/conf.py

python:
  install:
    - requirements: docs/requirements.txt
```

### GitHub Pages

```yaml
# .github/workflows/docs.yml
- name: Build documentation
  run: |
    sphinx-build docs/source/ docs/build/html

- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    publish_dir: ./docs/build/html
```

## 9. Настройки conf.py

```python
# язык
language = "ru"

# тема
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
}

# favicon / logo
html_favicon = "_static/favicon.ico"
html_logo = "_static/logo.png"

# suppression
suppress_warnings = ["image.nonlocal_uri"]

# для автодокументации
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": False,
    "show-inheritance": True,
}
autodoc_typehints = "description"  # или "signature", "none"
```

## 10. Полезные расширения

| Расширение | Описание |
|---|---|
| `sphinx.ext.autodoc` | Автодокументация из докстрингов |
| `sphinx.ext.napoleon` | Google/NumPy docstring style |
| `sphinx.ext.viewcode` | Ссылки на исходный код |
| `sphinx.ext.todo` | TODO блоки |
| `sphinx.ext.coverage` | Покрытие документацией |
| `sphinx.ext.intersphinx` | Ссылки на другие проекты |
| `sphinx.ext.imgmath` | Математические формулы |
| `sphinx_rtd_theme` | Тема Read the Docs |
| `myst_parser` | Поддержка Markdown |
| `sphinxcontrib-apidoc` | Авто-генерация .rst из модулей |
| `sphinx-copybutton` | Кнопка копирования в code blocks |

## 11. Сборка требований

```txt
# docs/requirements.txt
sphinx>=7.0
sphinx_rtd_theme>=2.0
myst-parser>=3.0
```
