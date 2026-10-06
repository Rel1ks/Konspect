# Pyright

**Pyright** — статический анализатор типов от Microsoft. Быстрый, написан на TypeScript. Используется в VS Code (через Pylance).

## 1. Установка

```bash
# через npm (основной способ)
npm install -g pyright

# через pip
pip install pyright
```

## 2. Использование

```bash
# проверка файла
pyright script.py

# проверка папки
pyright src/

# проверка всех файлов
pyright .

# verbose
pyright src/ --verbose
```

```python
# script.py
def add(a: int, b: int) -> int:
    return a + b

result = add(1, "2")  # Pyright найдёт ошибку
```

## 3. VS Code + Pylance

В VS Code Pyright работает через расширение **Pylance**.

```json
// settings.json
{
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,
    "python.analysis.inlayHints.functionReturnTypes": true,
    "python.analysis.inlayHints.variableTypes": true,
    "python.analysis.diagnosticMode": "workspace",
}
```

### Режимы проверки

| Режим | Описание |
|---|---|
| `off` | Отключена |
| `basic` | Базовые проверки |
| `strict` | Строгие проверки (рекомендуется) |

## 4. pyproject.toml

```toml
[tool.pyright]
include = ["src"]
exclude = ["tests", "**/node_modules"]
pythonVersion = "3.12"
pythonPlatform = "Windows"
typeCheckingMode = "basic"

# отключить конкретные правила
reportMissingTypeStubs = false
reportMissingImports = false
reportPrivateUsage = false
reportGeneralTypeIssues = "warning"
```

### command-line флаги

```bash
pyright src/ --pythonversion 3.12
pyright src/ --typecheckingmode strict
pyright src/ --skipunannotated  # пропустить неаннотированный код
pyright src/ --createstub requests  # создать .pyi заглушку
```

## 5. Коды ошибок

```python
# reportGeneralTypeIssues
def add(a: int, b: int) -> int:
    return a + b

add(1, "2")  # error: Argument of type "str" cannot be assigned

# reportOptionalMemberAccess
x: str | None = None
# print(x.upper())  # error: Cannot access member of optional type

# reportUnusedVariable
name = "Анна"
# warning: "name" is not accessed

# reportUnknownParameterType
def func(param):  # warning: Parameter missing type annotation
    pass
```

### Типы диагностики

| Уровень | Описание |
|---|---|
| `error` | Ошибка |
| `warning` | Предупреждение |
| `information` | Информация |
| `none` | Отключено |

## 6. Type Stub (.pyi)

Файлы с аннотациями для библиотек без типов.

```python
# requests-stubs/requests.pyi
def get(url: str, params: dict | None = None) -> Response: ...
class Response:
    status_code: int
    text: str
    def json(self) -> object: ...
```

```bash
pyright --createstub requests  # создаст заглушку
```

## 7. Pyright vs Mypy

```python
# оба проверяют одно и то же:
def greet(name: str) -> str:
    return f"Привет, {name}"

greet(42)  # оба найдут ошибку
```

| | Pyright | Mypy |
|---|---|---|
| Язык | TypeScript | Python |
| Скорость | **Очень быстрый** | Средний |
| VS Code | Pylance (встроен) | Расширение |
| Конфигурация | pyproject.toml | mypy.ini |
| strict mode | `basic` / `strict` | `--strict` |
| Плагины | Нет | Есть (Django, SQLAlchemy) |
| Популярность | Растёт | Стабильная |
| Распространение | npm + pip | pip |

```bash
# mypy — медленнее, но больше плагинов
mypy src/ --strict

# pyright — быстрее, встроен в VS Code
pyright src/ --typecheckingmode strict
```

## 8. Совместное использование

```toml
# pyproject.toml
[tool.pyright]
typeCheckingMode = "basic"

[tool.mypy]
strict = true
```

```bash
# оба в CI
pyright src/
mypy src/
```

## 9. Практические советы

```python
# 1. Используйте Pylance в VS Code (Pyright внутри)
# 2. Начните с basic, переходите к strict
# 3. Добавьте pyright в CI

# type: ignore — отключить проверку строки
x: int = "str"  # type: ignore

# Reveal type (для отладки)
reveal_type(x)  # Pyright покажет тип в терминале
```

## 10. Полезные команды

```bash
# версия
pyright --version

# помощь
pyright --help

# информация о типе
# reveal_type(x) в коде

# игнорировать конкретные файлы
pyright src/ --exclude tests

# создать заглушки
pyright --createstub my_library
```
