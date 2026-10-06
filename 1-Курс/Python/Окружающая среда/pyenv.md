# pyenv — управление версиями Python

**pyenv** — инструмент для установки и переключения между разными версиями Python.

## 1. Установка (Windows)

```bash
# для Windows — pyenv-win (официальный порт)
pip install pyenv-win --target %USERPROFILE%\.pyenv
```

или через `winget`:

```bash
winget install pyenv-win
```

### Настройка PATH

```powershell
# добавить в профиль PowerShell:
[System.Environment]::SetEnvironmentVariable("PYENV", "$env:USERPROFILE\.pyenv\pyenv-win", "User")
[System.Environment]::SetEnvironmentVariable("PYENV_ROOT", "$env:USERPROFILE\.pyenv\pyenv-win", "User")
[System.Environment]::SetEnvironmentVariable("PYENV_HOME", "$env:USERPROFILE\.pyenv\pyenv-win", "User")

# PATH
[System.Environment]::SetEnvironmentVariable("Path",
    "$env:USERPROFILE\.pyenv\pyenv-win\bin;" +
    "$env:USERPROFILE\.pyenv\pyenv-win\shims;" +
    [Environment]::GetEnvironmentVariable("Path", "User"), "User")
```

```bash
# проверка
pyenv --version
```

## 2. Основные команды

```bash
# список доступных для установки версий
pyenv install --list

# установка версии
pyenv install 3.12.0
pyenv install 3.11.0
pyenv install 3.10.0

# список установленных
pyenv versions

# текущая версия
pyenv version

# глобальная версия (по умолчанию)
pyenv global 3.12.0

# локальная версия (для папки)
pyenv local 3.11.0

# временная (для сессии)
pyenv shell 3.10.0
```

## 3. Как это работает

pyenv использует **shims** — перехватчики вызовов `python`, `pip` и т.д.

```
pyenv global 3.12.0
# python → shim → ~/.pyenv/versions/3.12.0/bin/python

pyenv local 3.11.0
# в этой папке python → shim → ~/.pyenv/versions/3.11.0/bin/python
```

### Порядок выбора версии

1. `PYENV_VERSION` (переменная окружения)
2. `.python-version` (локальный файл в папке)
3. `~/.pyenv/version` (глобальная)
4. системный Python

## 4. Управление версиями

```bash
# глобальная — для всей системы
pyenv global 3.12.0

# локальная — для текущей папки (создаёт .python-version)
cd my-project
pyenv local 3.11.0
cat .python-version  # 3.11.0

# временная — для текущей сессии
pyenv shell 3.10.0
```

### .python-version

```bash
# файл .python-version в корне проекта
echo "3.11.0" > .python-version
# pyenv автоматически переключит версию при входе в папку
```

## 5. Установка версий

```bash
# доступные версии
pyenv install --list
pyenv install --list | grep "3.12"

# установка
pyenv install 3.12.0
pyenv install 3.11.5

# установка с флагами
pyenv install --verbose 3.12.0

# переустановка
pyenv install --force 3.12.0

# удаление
pyenv uninstall 3.10.0

# расположение установленных версий
ls ~/.pyenv/versions/
```

### Требования для сборки (Linux/macOS)

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
  libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
```

## 6. Виртуальные окружения (pyenv-virtualenv)

```bash
# установка плагина (Linux/macOS)
git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv

# или через pip
pip install pyenv-virtualenv
```

### Использование

```bash
# создать виртуальное окружение
pyenv virtualenv 3.12.0 my-project-env

# список окружений
pyenv virtualenvs

# активировать
pyenv activate my-project-env

# деактивировать
pyenv deactivate

# удалить
pyenv uninstall my-project-env

# локальное использование (через .python-version)
pyenv local my-project-env
```

## 7. pyenv и poetry

```bash
# pyenv ставит версию Python
pyenv install 3.12.0
pyenv local 3.12.0

# poetry использует этот Python
poetry env use $(pyenv which python)
poetry install
```

## 8. pyenv vs другие инструменты

| | pyenv | conda | uv | Docker |
|---|---|---|---|---|
| Управление Python | ✅ | ✅ | ✅ | ✅ |
| Изоляция проектов | pyenv-virtualenv | Окружения | Встроена | Контейнеры |
| Простота | Средняя | Высокая | Высокая | Низкая |
| Скорость | Средняя | Медленный | Очень быстрый | Зависит |
| Только Python | Да | Нет | Да | Нет |

## 9. Полезные команды

```bash
# показать текущий Python и его путь
pyenv which python
pyenv which pip

# список всех версий (включая системную)
pyenv versions

# где лежат shims
ls ~/.pyenv/shims/

# обновить базу shims
pyenv rehash

# отладка
pyenv --help

# где python на самом деле
# Windows: посмотреть PATH — shims должны быть первыми
```
