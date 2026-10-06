# Модуль typing

**typing** — стандартный модуль Python для аннотаций типов. Поддерживается начиная с Python 3.5.

## 1. Базовые типы

```python
from typing import (
    List, Dict, Tuple, Set, FrozenSet,
    Optional, Union, Any, Callable,
    TypeVar, Generic, Iterator, Iterable,
    Sequence, Mapping, MutableMapping,
    Type, Literal, Final, Self,
    TypedDict, Never, NoReturn,
    cast, overload, Protocol,
)
```

## 2. Container типы

### List

```python
from typing import List

# Python 3.8-
def process(items: List[int]) -> List[str]:
    return [str(x) for x in items]

# Python 3.9+
def process(items: list[int]) -> list[str]:
    return [str(x) for x in items]
```

### Dict

```python
from typing import Dict

config: Dict[str, int] = {"port": 8080, "timeout": 30}

# вложенный
data: Dict[str, List[int]] = {"scores": [1, 2, 3]}

# Python 3.9+
config: dict[str, int] = {"port": 8080}
data: dict[str, list[int]] = {"scores": [1, 2, 3]}
```

### Tuple

```python
from typing import Tuple

# фиксированная длина
point: Tuple[int, int] = (3, 5)
user: Tuple[str, int, bool] = ("Анна", 25, True)

# переменная длина
args: Tuple[int, ...] = (1, 2, 3, 4)

# Python 3.9+
point: tuple[int, int] = (3, 5)
args: tuple[int, ...] = (1, 2, 3)
```

### Set / FrozenSet

```python
from typing import Set, FrozenSet

tags: Set[str] = {"python", "typing"}
immutable: FrozenSet[int] = frozenset([1, 2, 3])

# Python 3.9+
tags: set[str] = {"python", "typing"}
```

## 3. Optional и Union

### Optional

```python
from typing import Optional

# Optional[X] = X | None
def find(id: int) -> Optional[str]:
    return None if id <= 0 else f"User {id}"

# Python 3.10+
def find(id: int) -> str | None:
    return None
```

### Union

```python
from typing import Union

def parse(value: Union[int, str, float]) -> str:
    return str(value)

# Python 3.10+
def parse(value: int | str | float) -> str:
    return str(value)

# несколько
def process(data: Union[int, str, List[int], None]) -> None:
    pass
```

## 4. Any и TypeVar

### Any

```python
from typing import Any

# Any — отключает проверку типов
def log(message: Any) -> None:
    print(message)

value: Any = 5
value = "str"
value = [1, 2, 3]  # всё допустимо
```

### TypeVar

```python
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T | None:
    return items[0] if items else None

# ограничения
N = TypeVar("N", int, float)
S = TypeVar("S", bound=str)

def add(a: N, b: N) -> N:
    return a + b

def repeat(item: S, count: int) -> S:
    return item * count
```

## 5. Callable

```python
from typing import Callable

# функция (int, int) → int
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# без параметров → str
def get_greeting(func: Callable[[], str]) -> str:
    return func()

# любые аргументы → Any
Handler = Callable[..., Any]

# Callable[[int], str] — принимает int, возвращает str
```

## 6. Literal

```python
from typing import Literal

def set_mode(mode: Literal["read", "write", "append"]) -> None:
    print(f"Режим: {mode}")

def get_status() -> Literal[200, 404, 500]:
    return 200

# комбинация
def set_size(size: Literal["S", "M", "L", "XL"]) -> None:
    pass
```

## 7. Final

```python
from typing import Final

MAX_SIZE: Final = 100
NAME: Final[str] = "App"

# mypy: Cannot assign to final name
# MAX_SIZE = 200
```

## 8. Self

```python
from typing import Self

class Builder:
    def __init__(self) -> None:
        self._value = 0

    def add(self, x: int) -> Self:
        self._value += x
        return self

    def build(self) -> int:
        return self._value

class ExtendedBuilder(Builder):
    def multiply(self, x: int) -> Self:
        self._value *= x
        return self

b = ExtendedBuilder().add(5).multiply(2).build()
```

## 9. Type — тип класса

```python
from typing import Type

class User:
    def __init__(self, name: str) -> None:
        self.name = name

def create_user(cls: Type[User], name: str) -> User:
    return cls(name)

# Type[User] — класс User (или его подклассы)
```

## 10. TypedDict

```python
from typing import TypedDict

class UserDict(TypedDict):
    name: str
    age: int
    email: str | None

# total=False — все поля опциональны
class Config(TypedDict, total=False):
    debug: bool
    port: int
    host: str

user: UserDict = {"name": "Анна", "age": 25, "email": None}

# альтернативный синтаксис
UserDict = TypedDict("UserDict", {"name": str, "age": int})
```

## 11. Protocol (Structural Subtyping)

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Рисую круг")

class Square:
    def draw(self) -> None:
        print("Рисую квадрат")

# структурная типизация — «утиная» на типах
def render(obj: Drawable) -> None:
    obj.draw()

render(Circle())  # OK
render(Square())  # OK
```

## 12. Never / NoReturn

```python
from typing import Never, NoReturn

# функция никогда не возвращает управление
def exit_app() -> NoReturn:
    raise SystemExit(0)

# сужение до Never (Python 3.11+)
def assert_never(value: Never) -> None:
    raise AssertionError(f"Неожиданное значение: {value}")
```

## 13. cast и overload

### cast

```python
from typing import cast

value = get_data()  # type: ignore
x = cast(int, value)  # mypy считает, что это int
```

### overload

```python
from typing import overload

@overload
def process(data: int) -> str: ...

@overload
def process(data: str) -> int: ...

@overload
def process(data: list[int]) -> list[str]: ...

def process(data):
    # реализация
    if isinstance(data, int):
        return str(data)
    elif isinstance(data, str):
        return int(data)
    else:
        return [str(x) for x in data]

reveal_type(process(42))        # str
reveal_type(process("hello"))   # int
reveal_type(process([1, 2, 3])) # list[str]
```

## 14. Iterable, Iterator, Sequence

```python
from typing import Iterable, Iterator, Sequence

def process(items: Iterable[int]) -> None:
    for item in items:  # только for
        pass

def read() -> Iterator[int]:
    yield from range(10)

def get(index: int, items: Sequence[int]) -> int:
    return items[index]  # Sequence поддерживает __getitem__
```

## 15. Mapping, MutableMapping

```python
from typing import Mapping, MutableMapping

def read(config: Mapping[str, int]) -> int | None:
    return config.get("port")

def update(config: MutableMapping[str, int]) -> None:
    config["port"] = 8080
```

## 16. Annotated (Python 3.9+)

```python
from typing import Annotated

def process(data: Annotated[str, "минимум 10 символов"]) -> None:
    pass

# с Pydantic
from pydantic import Field

class User(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50)]
```

## 17. TypeAlias (Python 3.10+)

```python
from typing import TypeAlias

Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[list[float]]

def scale(v: Vector, factor: float) -> Vector:
    return [x * factor for x in v]
```

## 18. Concatenate и ParamSpec

```python
from typing import ParamSpec, Concatenate, Callable

P = ParamSpec("P")

def decorator(func: Callable[P, int]) -> Callable[P, str]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
        return str(func(*args, **kwargs))
    return wrapper
```
