# Pydantic

**Pydantic** — библиотека для валидации данных через type hints. Используется в FastAPI, SQLModel и других проектах.

## 1. Установка

```bash
pip install pydantic
```

## 2. BaseModel

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str | None = None
    is_active: bool = True

# создание с валидацией
user = User(name="Анна", age=25, email="anna@example.com")
print(user.model_dump())
# {"name": "Анна", "age": 25, "email": "anna@example.com", "is_active": True}
```

## 3. Валидация

### Автоматическое приведение типов

```python
class Product(BaseModel):
    name: str
    price: float
    quantity: int

# pydantic сам приведёт типы
product = Product(name="Товар", price="99.99", quantity="5")
print(product.price)     # 99.99 (float)
print(product.quantity)  # 5 (int)
```

### Ошибки валидации

```python
from pydantic import ValidationError

try:
    user = User(name="Анна", age="не число")
except ValidationError as e:
    print(e.errors())
    # [{"type": "int_parsing", "loc": ["age"], "msg": "...", "input": "не число"}]
```

## 4. Поля и типы

### Стандартные типы

```python
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID, uuid4
from decimal import Decimal

class Item(BaseModel):
    id: UUID = uuid4()
    created_at: datetime = datetime.now()
    event_date: date
    price: Decimal
    tags: list[str] = []
    metadata: dict[str, str] = {}
```

### Констрейнты (ограничения)

```python
from pydantic import BaseModel, Field
from typing import Annotated

class Product(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    price: float = Field(gt=0, le=10000)
    quantity: int = Field(ge=0, default=0)
    code: str = Field(pattern=r"^[A-Z]{3}-\d{4}$")
    description: str = Field(default="", max_length=500)

# через Annotated (Python 3.9+)
from typing import Annotated
from pydantic import StringConstraints, conint, confloat

class Config(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    version: Annotated[int, conint(ge=1)]
    timeout: Annotated[float, confloat(ge=0.1)]
```

## 5. Валидаторы

### @field_validator

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    age: int
    password: str

    @field_validator("name")
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        if " " not in v.strip():
            raise ValueError("Имя должно содержать фамилию")
        return v.title()

    @field_validator("age")
    @classmethod
    def adult(cls, v: int) -> int:
        if v < 18:
            raise ValueError("Только для взрослых")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Минимум 8 символов")
        return v
```

### @model_validator

```python
from pydantic import BaseModel, model_validator

class Order(BaseModel):
    items: list[str]
    discount: float = 0
    total: float

    @model_validator(mode="after")
    def check_total(self) -> "Order":
        if self.discount < 0 or self.discount > 100:
            raise ValueError("Скидка от 0 до 100")
        return self

    @model_validator(mode="before")
    @classmethod
    def parse_data(cls, data: dict) -> dict:
        if "total" not in data:
            data["total"] = len(data.get("items", [])) * 100
        return data
```

## 6. Настройки модели (Config)

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        frozen=True,           # объект неизменяемый
        str_strip_whitespace=True,  # обрезать пробелы
        str_min_length=1,      # минимальная длина строк
        extra="forbid",        # запретить лишние поля
        populate_by_name=True, # доступ по имени поля
        validate_default=True, # валидация дефолтных значений
    )

    name: str
    age: int

# frozen — объект нельзя изменить
user = User(name="Анна", age=25)
# user.age = 30  # ValidationError
```

### Режимы extra

```python
# extra = "ignore" (по умолч.) — игнорировать лишние поля
# extra = "forbid" — ошибка при лишних полях
# extra = "allow" — лишние поля сохраняются

class StrictUser(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    age: int

# StrictUser(name="Анна", age=25, extra_field=1)  # ошибка
```

## 7. Сериализация

```python
class User(BaseModel):
    name: str
    age: int
    email: str | None = None

user = User(name="Анна", age=25)

# dict
user.model_dump()
user.model_dump(exclude={"email"})
user.model_dump(include={"name", "age"})
user.model_dump(mode="json")  # datetime → str

# JSON
user.model_dump_json()
user.model_dump_json(indent=2)

# by_alias
class Item(BaseModel):
    item_id: int = Field(alias="id")

item = Item(id=1)
print(item.model_dump())           # {"item_id": 1}
print(item.model_dump(by_alias=True))  # {"id": 1}
```

## 8. Десериализация

```python
# из dict
user = User.model_validate({"name": "Анна", "age": 25})

# из JSON
json_str = '{"name": "Анна", "age": 25}'
user = User.model_validate_json(json_str)

# из любого объекта
class ExternalUser:
    def __init__(self):
        self.full_name = "Анна Петрова"
        self.years = 25

external = ExternalUser()
user = User.model_validate(external, from_attributes=True)
```

## 9. Вложенные модели

```python
class Address(BaseModel):
    city: str
    street: str
    house: int

class User(BaseModel):
    name: str
    address: Address

user = User(
    name="Анна",
    address={"city": "Москва", "street": "Арбат", "house": 10},
)
print(user.address.city)
```

## 10. Generic Models

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    status: str
    data: T

user_response = Response[User](status="ok", data=User(name="Анна", age=25))
```

## 11. Dataclass vs Pydantic

```python
from dataclasses import dataclass

@dataclass
class UserDataclass:
    name: str
    age: int

# pydantic делает то же + валидация + сериализация
class UserPydantic(BaseModel):
    name: str
    age: int

# pydantic-dataclass
from pydantic.dataclasses import dataclass as pydantic_dataclass

@pydantic_dataclass
class User:
    name: str
    age: int
```

## 12. Performance

```python
# Pydantic v2 написан на Rust (pydantic-core)
# Значительно быстрее v1

# для максимальной производительности — mode="python"
user.model_dump(mode="python")
```

## 13. Pydantic в FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.post("/items")
async def create_item(item: Item):
    # item уже валидирован Pydantic
    return item
```
