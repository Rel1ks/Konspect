# Mypy

**Mypy** — статический анализатор типов для Python. Проверяет соответствие кода аннотациям типов без запуска программы.

## 1. Установка

```bash
pip install mypy
```

## 2. Использование

```bash
# проверка файла
mypy script.py

# проверка папки
mypy src/

# строгий режим
mypy --strict src/

# verbose
mypy -v src/
```

```python
# script.py
from typing import Optional

def greet(name: str) -> str:
    return f"Привет, {name}"

def add(a: int, b: int) -> int:
    return a + b

greet(42)        # error: Argument 1 to "greet" has incompatible type "int"
add(1, "2")      # error: Argument 2 to "add" has incompatible type "str"
```

## 3. mypy.ini / pyproject.toml

```ini
# mypy.ini
[mypy]
python_version = 3.12
strict = true
ignore_missing_imports = true
check_untyped_defs = true
warn_unused_ignores = true
warn_return_any = true
warn_redundant_casts = true
show_error_codes = true
```

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
ignore_missing_imports = true
check_untyped_defs = true
warn_unused_ignores = true

# игнорировать файлы
[[tool.mypy.overrides]]
module = "tests.*"
ignore_errors = true

# конкретная библиотека
[[tool.mypy.overrides]]
module = "legacy.*"
ignore_missing_imports = true
```

## 4. Режимы строгости

```bash
# без флагов — базовые проверки
mypy script.py

# --strict включает всё:
#   --no-implicit-optional
#   --no-implicit-reexport
#   --strict-equality
#   --warn-unused-configs
#   --warn-redundant-casts
#   --warn-return-any
#   --warn-unused-ignores
#   --check-untyped-defs
mypy --strict script.py
```

### Выборочные флаги

| Флаг | Описание |
|---|---|
| `--strict` | Все строгие проверки |
| `--ignore-missing-imports` | Игнорировать импорты без типов |
| `--disallow-untyped-defs` | Ошибка, если функция без аннотаций |
| `--disallow-incomplete-defs` | Ошибка, если частичные аннотации |
| `--check-untyped-defs` | Проверять тела неаннотированных функций |
| `--warn-return-any` | Предупреждать, если возвращается Any |
| `--warn-unused-ignores` | Предупреждать о лишних `# type: ignore` |
| `--no-implicit-optional` | Требовать явный Optional |
| `--strict-equality` | Проверять сравнения типов |

## 5. Прагмы (type: ignore)

```python
# отключить проверку для строки
x: int = "str"  # type: ignore

# отключить конкретную ошибку
y: int = "str"  # type: ignore[assignment]

# отключить для всего файла
# в начале файла: # mypy: ignore-errors
```

## 6. Reveal type

```python
# mypy покажет тип переменной
x = "hello"
reveal_type(x)  # mypy: Revealed type is "builtins.str"

y = [1, 2, 3]
reveal_type(y)  # mypy: Revealed type is "builtins.list[builtins.int]"
```

## 7. Плагины mypy

```bash
# Django
pip install mypy django-stubs

# SQLAlchemy
pip install mypy sqlalchemy-stubs

# Pydantic
pip install pydantic mypy
```

```ini
[mypy]
plugins =
    pydantic.mypy,
    sqlalchemy.ext.mypy.plugin,
```

## 8. Работа с библиотеками без типов

```bash
# установить заглушки (stubs)
pip install types-requests
pip install types-PyYAML
pip install types-beautifulsoup4

# или игнорировать
mypy --ignore-missing-imports src/
```

## 9. Type Stub (.pyi)

```python
# my_library.pyi — заглушка для библиотеки без типов
class Client:
    def get(self, url: str) -> Response: ...
    def post(self, url: str, data: dict) -> Response: ...

class Response:
    status_code: int
    text: str
    def json(self) -> object: ...
```

```bash
# создать stub
stubgen my_library.py  # создаст .pyi файл

# или
mypy --generate-stub my_library.py
```

## 10. Mypy в CI/CD

```yaml
# GitHub Actions
- name: Type check
  run: mypy src/ --strict

# с кешированием
- name: mypy
  run: mypy src/ --strict --cache-dir .mypy_cache
```

## 11. Mypy vs Pyright

| | Mypy | Pyright |
|---|---|---|
| Язык | Python | TypeScript |
| Скорость | Средний | **Очень быстрый** |
| VS Code | Расширение | Pylance (встроен) |
| Плагины | **Есть** (Django, SA) | Нет |
| Конфигурация | mypy.ini / pyproject.toml | pyproject.toml |
| strict mode | `--strict` | `typeCheckingMode = "strict"` |
| Сложность | Выше | Ниже |

## 12. Примеры ошибок

```python
from typing import Optional, List

# error: Incompatible types
x: int = "str"

# error: Missing return type annotation (disallow_untyped_defs)
def func():
    pass

# error: Argument missing type annotation
def process(data):
    pass

# error: Optional type not allowed
def get(id: int) -> Optional[str]:
    return None

# error: Comparison of incompatible types (strict_equality)
x: int = 5
y: str = "hello"
# if x == y:  # error
#     pass
```
