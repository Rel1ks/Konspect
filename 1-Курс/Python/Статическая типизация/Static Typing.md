# Static Typing (Type Hints) в Python

Python — динамически типизированный язык. **Type hints** (аннотации типов) — подсказки для разработчиков и инструментов, не влияющие на выполнение.

## 1. Аннотации переменных

```python
# Python 3.6+
name: str = "Анна"
age: int = 25
price: float = 99.99
is_active: bool = True

# без значения
data: list
```

## 2. Аннотации функций

```python
def greet(name: str) -> str:
    return f"Привет, {name}!"

def add(a: int, b: int) -> int:
    return a + b

def process(data: str) -> None:
    print(data)
```

## 3. typing — стандартный модуль

```python
from typing import (
    List, Dict, Tuple, Set, Optional,
    Union, Any, Callable, TypeVar,
    Generic, Iterator, Iterable,
    Sequence, Mapping, Literal,
    Final, TypedDict,
)

# старый стиль (Python 3.8-)
from typing import List, Dict

def get_users() -> List[Dict[str, int]]:
    return [{"id": 1}]

# новый стиль (Python 3.9+)
def get_users() -> list[dict[str, int]]:
    return [{"id": 1}]
```

### List

```python
def process(items: list[int]) -> list[str]:
    return [str(x) for x in items]

# вложенные
matrix: list[list[int]] = [[1, 2], [3, 4]]
```

### Dict

```python
def lookup(data: dict[str, int], key: str) -> int | None:
    return data.get(key)

config: dict[str, str | int] = {"host": "localhost", "port": 8080}
```

### Tuple

```python
# фиксированная длина
point: tuple[int, int] = (3, 5)

# переменная длина
args: tuple[int, ...] = (1, 2, 3)
```

### Set

```python
tags: set[str] = {"python", "typing"}
```

### Optional

```python
from typing import Optional

def find_user(id: int) -> Optional[str]:
    # может вернуть str или None
    return None if id <= 0 else f"User {id}"

# Python 3.10+ можно str | None
def find_user(id: int) -> str | None:
    return None
```

### Union

```python
def parse(value: int | str | float) -> str:
    return str(value)

# старый стиль
from typing import Union
def parse(value: Union[int, str, float]) -> str:
    return str(value)
```

### Any

```python
from typing import Any

def log(message: Any) -> None:
    print(message)

# Any — отключает проверку типов
```

### Callable

```python
from typing import Callable

def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# сложная сигнатура
Callback = Callable[[int, str], bool]
Handler = Callable[..., Any]  # любые аргументы
```

## 4. TypeVar — обобщённые типы (Generics)

```python
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T | None:
    return items[0] if items else None

print(first([1, 2, 3]))     # int
print(first(["a", "b"]))    # str
```

### Ограничения

```python
T = TypeVar("T", int, float)  # только int или float
S = TypeVar("S", bound=Comparable)  # bound — ограничение

def add(a: T, b: T) -> T:
    return a + b
```

## 5. Generic — обобщённые классы

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def peek(self) -> T:
        return self._items[-1]

# использование
int_stack = Stack[int]()
int_stack.push(1)
value = int_stack.pop()  # тип int

str_stack = Stack[str]()
str_stack.push("hello")
```

## 6. TypedDict

```python
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int
    email: str | None

def create_user(user: User) -> None:
    print(user["name"])

user: User = {"name": "Анна", "age": 25, "email": None}
```

## 7. Literal

```python
from typing import Literal

def set_mode(mode: Literal["read", "write", "append"]) -> None:
    print(f"Режим: {mode}")

set_mode("read")
# set_mode("delete")  # TypeError от mypy

def get_status() -> Literal[200, 404, 500]:
    return 200
```

## 8. Final — константы

```python
from typing import Final

MAX_SIZE: Final = 100
NAME: Final[str] = "App"

# mypy выдаст ошибку:
# MAX_SIZE = 200  # error: Cannot assign to final name
```

## 9. Self — возврат себя

```python
from typing import Self

class Builder:
    def __init__(self) -> None:
        self._value = 0

    def add(self, x: int) -> Self:
        self._value += x
        return self

    def multiply(self, x: int) -> Self:
        self._value *= x
        return self

builder = Builder()
result = builder.add(5).multiply(2)  # цепочка
```

## 10. Новый синтаксис (Python 3.10+)

```python
# Union
def parse(value: int | str | float) -> str: ...

# Optional
def find(id: int) -> str | None: ...

# TypeAlias
type Vector = list[float]

# Python 3.12+
type Point = tuple[float, float]
type Matrix = list[list[float]]
```

## 11. mypy — проверка типов

```bash
pip install mypy
mypy script.py
mypy --strict script.py
mypy --ignore-missing-imports script.py
```

```python
# mypy найдёт ошибки
def add(a: int, b: int) -> int:
    return a + b

add(1, "2")  # error: Argument 2 to "add" has incompatible type "str"
```

## 12. Pydantic — валидация на типах

```bash
pip install pydantic
```

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str | None = None

# валидация
user = User(name="Анна", age=25)
print(user.model_dump())

# ошибка при неверном типе
# User(name="Анна", age="не число")  # ValidationError
```

## 13. Преимущества

```python
# 1. Документация — типы как документация
def process(user_id: int) -> User | None: ...

# 2. IDE — автодополнение и подсказки
# 3. mypy — статический анализ
# 4. Меньше багов — типы ловят ошибки на этапе написания
```

## 14. Когда НЕ использовать

```python
# излишняя сложность
def f(a: int | str | float | list[int] | None) -> dict[str, list[str | int]]: ...

# Лучше: разбить на несколько функций
# Или: упростить типы

# Для скриптов и прототипов — можно без типов
```

## 15. Сравнение динамической и статической типизации

| | Динамическая | Статическая (type hints) |
|---|---|---|
| Проверка | Runtime | mypy / IDE |
| Гибкость | Высокая | Средняя |
| Скорость разработки | Высокая | Средняя |
| Надёжность | Ниже | Выше |
| Документация | Код | Типы + код |
