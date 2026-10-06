# virtualenv / venv

**virtualenv/venv** — изолированные окружения Python. Каждое окружение имеет свои пакеты, не затрагивая системный Python.

## 1. venv (встроенный, Python 3.3+)

```bash
# создать окружение
python -m venv .venv

# активировать (Windows)
.venv\Scripts\activate

# активировать (Linux/macOS)
source .venv/bin/activate

# деактивировать
deactivate

# удалить окружение
rm -rf .venv
```

## 2. virtualenv (сторонний, Python 2 + 3)

```bash
# установка
pip install virtualenv

# создать
virtualenv .venv
virtualenv -p python3.12 .venv  # указать версию
virtualenv -p C:\Python312\python.exe .venv  # путь

# остальное так же, как venv
```

## 3. Различия venv vs virtualenv

| | venv | virtualenv |
|---|---|---|
| Встроен | Да (3.3+) | Нет |
| Python 2 | Нет | Да |
| Скорость | Быстрее | Медленнее |
| Расширенные опции | Нет | Есть |

## 4. Активация (все способы)

### Windows

```bash
# cmd
.venv\Scripts\activate.bat

# PowerShell
.venv\Scripts\Activate.ps1

# если ошибка выполнения скриптов:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Linux/macOS

```bash
# bash/zsh
source .venv/bin/activate

# fish
source .venv/bin/activate.fish

# csh/tcsh
source .venv/bin/activate.csh
```

## 5. Работа без активации

```bash
# Windows
.venv\Scripts\python.exe script.py
.venv\Scripts\pip.exe install requests

# Linux/macOS
.venv/bin/python script.py
.venv/bin/pip install requests
```

## 6. Структура окружения

```
.venv/
├── pyvenv.cfg          # конфиг (версия Python, путь)
├── Scripts/            # активация, python.exe, pip.exe
│   ├── activate
│   ├── activate.bat
│   ├── Activate.ps1
│   ├── deactivate.bat
│   ├── python.exe
│   └── pip.exe
├── Lib/
│   └── site-packages/  # установленные пакеты
└── Include/
```

## 7. Копирование и перемещение

```bash
# создать копию окружения
python -m venv --clear .venv  # очистить
pip freeze > requirements.txt
python -m venv .venv-copy
.venv-copy\Scripts\pip install -r requirements.txt

# перемещать окружение НЕЛЬЗЯ (пути жёстко прописаны)
# лучше удалить и создать заново
```

## 8. Использование в IDE

### VS Code

```bash
# выбрать интерпретатор:
# Ctrl+Shift+P → Python: Select Interpreter → .venv\Scripts\python.exe

# автопоиск: VS Code сам находит .venv в корне проекта
```

### PyCharm

```bash
# Settings → Project → Python Interpreter → Add → Existing environment
# выбрать .venv\Scripts\python.exe
```

## 9. virtualenvwrapper (Linux/macOS)

```bash
pip install virtualenvwrapper

# настройка в ~/.bashrc
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh

# команды
mkvirtualenv myproject     # создать
workon myproject           # активировать
deactivate                 # деактивировать
rmvirtualenv myproject     # удалить
lsvirtualenv               # список
cdvirtualenv               # перейти в папку окружения
add2virtualenv /path       # добавить путь в PYTHONPATH
```

## 10. Best practices

```bash
# .venv в .gitignore
echo ".venv/" >> .gitignore

# requirements.txt в репозитории
pip freeze > requirements.txt

# фиксировать версии
pip freeze > requirements.txt
# pip install -r requirements.txt для восстановления

# разделять dev/prod
# requirements.txt (prod)
requests>=2.31.0
flask>=3.0.0

# requirements-dev.txt (dev)
-r requirements.txt
pytest>=8.0
ruff>=0.3.0
```

## 11. pip внутри окружения

```bash
# после активации pip использует окружение
pip install requests       # установит в .venv
pip list                   # пакеты в .venv
pip freeze                 # только пакеты окружения

# без активации
.venv\Scripts\pip install requests
```

## 12. Сравнение

| | venv | virtualenv | conda | poetry |
|---|---|---|---|---|
| Встроен | ✅ | ❌ | ❌ | ❌ |
| Простота | Высокая | Высокая | Средняя | Средняя |
| Управление Python | Нет | Нет | ✅ | Через pyenv |
| Lock-файл | Нет | Нет | environment.yml | poetry.lock |
| Когда использовать | Всегда | Python 2 | Наука | Проекты |
