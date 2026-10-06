# pip — менеджер пакетов Python

**pip** (Pip Installs Packages) — стандартный менеджер пакетов для Python. Устанавливает пакеты из PyPI.

## 1. Установка pip

```bash
# проверка
pip --version
python -m pip --version

# обновить pip
python -m pip install --upgrade pip

# установить, если не установлен
python -m ensurepip --upgrade
```

## 2. Основные команды

```bash
# установка пакета
pip install requests
pip install "requests>=2.31.0"
pip install "requests==2.31.0"
pip install "requests>=2.31,<3.0"

# несколько
pip install requests flask numpy

# из файла
pip install -r requirements.txt

# editable mode
pip install -e .

# удаление
pip uninstall requests
pip uninstall -r requirements.txt -y

# список
pip list
pip list --outdated
pip list --not-required

# информация о пакете
pip show requests
pip show -f requests
```

## 3. Установка из разных источников

```bash
# PyPI (по умолчанию)
pip install requests

# URL
pip install https://example.com/package.tar.gz

# Git
pip install git+https://github.com/user/repo.git
pip install git+https://github.com/user/repo.git@main
pip install git+https://github.com/user/repo.git@v1.0

# локальная папка
pip install ./my-package
pip install /path/to/package

# wheel
pip install package.whl

# приватный репозиторий
pip install -i https://my-pypi.example.com/simple my-package
```

## 4. Форматы версий

| Формат | Описание | Пример |
|---|---|---|
| `==1.0` | Точная версия | `requests==2.31.0` |
| `>=1.0` | Больше или равно | `requests>=2.31.0` |
| `>1.0` | Строго больше | `requests>2.30` |
| `<2.0` | Меньше | `requests<3.0` |
| `<=2.0` | Меньше или равно | `requests<=2.31` |
| `~=1.2.3` | Совместимая (>=1.2.3, <1.3) | `requests~=2.31` |
| `>=1.0,<2.0` | Диапазон | `requests>=2.31,<3.0` |

## 5. requirements.txt

```
# requirements.txt
requests>=2.31.0
flask==3.0.0
numpy>=1.24,<2.0
git+https://github.com/user/repo.git@main
-e .
```

```bash
# создать на основе текущего окружения
pip freeze > requirements.txt

# установить из файла
pip install -r requirements.txt

# dev-зависимости (отдельный файл)
# requirements-dev.txt
-r requirements.txt
pytest>=8.0
black>=24.0
```

## 6. Виртуальное окружение (venv)

```bash
# создать
python -m venv .venv

# активировать (Windows)
.venv\Scripts\activate

# деактивировать
deactivate

# установка в окружение
pip install requests
```

### Без активации

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install requests
.venv\Scripts\python.exe script.py
```

## 7. Флаги

```bash
# без зависимостей
pip install requests --no-deps

# переустановка
pip install --force-reinstall requests

# без кеша
pip install --no-cache-dir requests

# verbose
pip install -v requests

# пользовательская установка (без прав админа)
pip install --user requests

# только двоичные
pip install --only-binary :all: numpy
```

## 8. Настройка зеркал PyPI

```bash
# разово
pip install -i https://mirror.yandex.ru/pypi/simple requests

# постоянно (pip.ini в %APPDATA%\pip\)
# [global]
# index-url = https://mirror.yandex.ru/pypi/simple
# trusted-host = mirror.yandex.ru

# через переменную окружения
set PIP_INDEX_URL=https://mirror.yandex.ru/pypi/simple
```

## 9. pip и кеш

```bash
pip cache dir
pip cache info
pip cache list
pip cache purge
```

## 10. pip check

```bash
# проверить конфликты зависимостей
pip check

# проверить устаревшие
pip list --outdated
```

## 11. Разделение dev/prod

```bash
# requirements.txt — production
flask==3.0.0
requests==2.31.0

# requirements-dev.txt — разработка
-r requirements.txt
pytest>=8.0
black>=24.0
```

## 12. pip vs uv vs poetry

| Возможность | pip | uv | Poetry |
|---|---|---|---|
| Скорость | Медленный | **Очень быстрый** | Средний |
| Lock-файл | `requirements.txt` | `uv.lock` | `poetry.lock` |
| Разрешение зависимостей | Нет | Да | Да |
| Виртуальное окружение | Через venv | Встроенное | Встроенное |
| Простота | Высокая | Высокая | Средняя |
| Стандарт | Стандартный | Новый | Свой формат |
