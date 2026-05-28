# uv — менеджер пакетов на Rust

**uv** — быстрый менеджер пакетов и проектов на Rust от создателей Ruff. Замена pip, pip-tools, poetry, virtualenv.

## 1. Установка

```bash
# Windows (powershell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# через pip
pip install uv

# через cargo
cargo install uv

# проверка
uv --version
```

## 2. Основные команды

```bash
# установка пакетов (как pip)
uv pip install requests
uv pip install "requests>=2.31.0"

# установка из requirements.txt
uv pip install -r requirements.txt

# синхронизация окружения
uv pip sync requirements.txt

# удаление
uv pip uninstall requests

# список пакетов
uv pip list

# дерево зависимостей
uv pip tree

# проверка устаревших
uv pip list --outdated

# заморозка (как pip freeze)
uv pip freeze > requirements.txt
```

## 3. uv как замена pip

```bash
# pip install → uv pip install
uv pip install requests

# pip install -r → uv pip install -r
uv pip install -r requirements.txt

# pip freeze → uv pip freeze
uv pip freeze

# pip show → uv pip show
uv pip show requests

# pip check → uv pip check
uv pip check
```

## 4. Виртуальное окружение

```bash
# создать venv
uv venv
uv venv .venv
uv venv --python 3.12

# активация (стандартная)
.venv\Scripts\activate  # Windows

# выполнить команду в venv
uv run python script.py
uv run pytest
```

## 5. Управление проектами (`uv project`)

```bash
# создать проект
uv init my-project

# инициализировать проект
uv init

# добавить зависимости
uv add requests
uv add "flask>=3.0"
uv add --dev pytest
uv add --group docs mkdocs

# удалить
uv remove requests

# установить проект
uv sync

# установить без dev
uv sync --no-dev

# обновить
uv lock
uv sync

# запуск
uv run python main.py
```

### pyproject.toml (создаётся uv init)

```toml
[project]
name = "my-project"
version = "0.1.0"
description = ""
authors = []
requires-python = ">=3.9"
dependencies = [
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
]

[tool.uv]
dev-dependencies = [
    "ruff>=0.3.0",
]
```

## 6. uv tool (инструменты)

Установка и запуск CLI-инструментов.

```bash
# установка инструмента
uv tool install ruff
uv tool install black

# запуск без установки
uvx ruff check .
uvx black --check .

# список инструментов
uv tool list

# обновление
uv tool upgrade ruff

# удаление
uv tool uninstall ruff
```

## 7. uv python (управление версиями Python)

```bash
# список доступных версий
uv python list

# установка Python
uv python install 3.12
uv python install 3.11 3.10

# найти Python
uv python find

# использовать определённую версию
uv python pin 3.12
```

## 8. uv pip compile (как pip-compile)

```bash
# генерация lock-файла из pyproject.toml
uv pip compile pyproject.toml -o requirements.txt

# с dev-зависимостями
uv pip compile pyproject.toml --extra dev -o requirements.txt

# из requirements.in
uv pip compile requirements.in -o requirements.txt
```

## 9. Скорость

uv **значительно** быстрее pip и Poetry, потому что написан на Rust.

```bash
# сравнение
time pip install requests    # ~2-5 сек
time uv pip install requests # ~0.3-1 сек
```

## 10. uv в CI/CD

```bash
# GitHub Actions — быстрая установка
- name: Install uv
  run: pip install uv

- name: Install dependencies
  run: uv pip install -r requirements.txt

# или через actions/setup-python
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
- run: pip install uv
- run: uv pip install -r requirements.txt --system
```

## 11. uv vs pip vs poetry

```bash
# pip — медленный, нет разрешения зависимостей
pip install requests

# poetry — средний, свой формат
poetry add requests

# uv — быстрый, совместим с pip
uv pip install requests
```

| Возможность | uv | pip | Poetry | PDM |
|---|---|---|---|---|
| Язык | Rust | Python | Python | Python |
| Скорость | **Очень быстрый** | Медленный | Средний | Средний |
| Lock-файл | `uv.lock` | Нет | `poetry.lock` | `pdm.lock` |
| pip-совместимость | Полная | — | Нет | Нет |
| Управление Python | Да | Нет | Нет | Нет |
| Инструменты (uvx) | Да | Нет | Нет | Нет |
| Разрешение зависимостей | Да | Нет | Да | Да |
| PEP 621 | Да | Нет | Нет | Да |

## 12. Полезные флаги

```bash
# подробный вывод
uv pip install requests -v

# кеш
uv cache dir
uv cache clean

# использовать системный Python
uv pip install --system requests

# не использовать кеш
uv pip install --no-cache requests

# флаг --reinstall
uv pip install --reinstall requests

# только если нужно обновить
uv pip install --upgrade requests
```

## 13. uv.lock

```bash
# uv.lock — детерминированный lock-файл
# создаётся при uv sync / uv lock

# установка по lock-файлу
uv sync

# не обновлять lock
uv sync --frozen

# только обновить lock
uv lock

# обновить конкретный пакет в lock
uv lock --upgrade-package requests
```
