# Pipenv

**Pipenv** — менеджер пакетов и окружений. Объединяет pip и virtualenv в одном инструменте. Использует `Pipfile` и `Pipfile.lock`.

## 1. Установка

```bash
pip install pipenv
```

## 2. Создание проекта

```bash
# инициализация (создаёт Pipfile)
cd my-project
pipenv install

# с указанием Python
pipenv --python 3.12
pipenv --python C:\Python312\python.exe

# установка пакета
pipenv install requests

# установка dev-зависимости
pipenv install --dev pytest

# активация
pipenv shell

# выход
exit
```

## 3. Pipfile

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = ">=2.31.0"
flask = "==3.0.0"

[dev-packages]
pytest = ">=8.0"
ruff = ">=0.3.0"

[requires]
python_version = "3.12"
python_full_version = "3.12.0"
```

## 4. Основные команды

```bash
# установка всех зависимостей
pipenv install

# установка только production
pipenv install --deploy  # из Pipfile.lock

# установка без dev
pipenv install --ignore-pipfile  # из lock-файла

# добавить пакет
pipenv install requests
pipenv install "requests>=2.31.0"

# dev
pipenv install --dev pytest

# удалить
pipenv uninstall requests

# обновить
pipenv update         # все
pipenv update requests  # конкретный

# проверить устаревшие
pipenv update --outdated

# дерево зависимостей
pipenv graph
```

## 5. Работа с окружением

```bash
# активировать shell
pipenv shell

# выполнить команду в окружении
pipenv run python script.py
pipenv run pytest
pipenv run black .

# информация об окружении
pipenv --venv       # путь к .venv
pipenv --py         # путь к Python
pipenv --where      # путь к проекту

# удалить окружение
pipenv --rm
```

## 6. Pipfile.lock

```bash
# автоматически создаётся при install/add
# фиксирует точные версии и хеши для воспроизводимости

# принудительное обновление lock
pipenv lock

# установка из lock (не меняет Pipfile)
pipenv install --ignore-pipfile
```

## 7. Переменные окружения

```python
# .env файл в корне проекта
SECRET_KEY=my-secret
DATABASE_URL=sqlite:///db.sqlite
```

```bash
# pipenv автоматически загружает .env
pipenv run python -c "import os; print(os.getenv('SECRET_KEY'))"

# или при активации
pipenv shell
```

```python
# в коде
import os
secret = os.getenv("SECRET_KEY")
```

## 8. Поддержка Python версий

```bash
# указать версию при создании
pipenv --python 3.12

# проверить совместимость
pipenv verify

# установить из разных источников
pipenv install "https://github.com/user/repo/archive/main.zip"
pipenv install -e ./my-package
```

## 9. Pipenv vs Poetry vs pip

| | Pipenv | Poetry | pip + venv |
|---|---|---|---|
| Формат | Pipfile | pyproject.toml | requirements.txt |
| Lock | Pipfile.lock | poetry.lock | Вручную |
| Окружение | Встроенное | Встроенное | venv |
| Простота | Средняя | Средняя | Высокая |
| Скорость | Средняя | Средняя | Медленная |
| graph | ✅ | ✅ | pipdeptree |
| .env | ✅ | ❌ | ❌ |
| Поддержка | Стабильная | Активная | Стандарт |

## 10. Тестирование

```python
# test_requests.py
import requests

def test_get():
    response = requests.get("https://httpbin.org/get")
    assert response.status_code == 200
```

```bash
# установка dev-зависимостей
pipenv install --dev pytest

# запуск тестов
pipenv run pytest
```

## 11. Пример рабочего процесса

```bash
# новый проект
mkdir my-app && cd my-app
pipenv --python 3.12
pipenv install flask requests
pipenv install --dev pytest black

# установка из существующего проекта
git clone project && cd project
pipenv install --dev
pipenv shell
```
