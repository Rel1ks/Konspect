# Парадигмы программирования в Python

Python поддерживает несколько парадигм — подходов к написанию кода.

## 1. Императивное программирование

Последовательные инструкции, изменяющие состояние программы.

```python
total = 0
for i in range(1, 11):
    total += i
print(total)
```

## 2. Процедурное программирование

Код организован в процедуры/функции.

```python
def calculate_total(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

def print_result(n):
    print(f"Сумма от 1 до {n}: {calculate_total(n)}")

print_result(10)
```

## 3. Объектно-ориентированное программирование (ООП)

Код организован вокруг объектов — экземпляров классов.

```python
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def show_history(self):
        return self.history

calc = Calculator()
print(calc.add(3, 5))
print(calc.add(10, 20))
print(calc.show_history())
```

### Наследование

```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Гав!"

class Cat(Animal):
    def speak(self):
        return "Мяу!"

animals = [Dog(), Cat()]
for a in animals:
    print(a.speak())
```

### Полиморфизм

```python
def make_sound(animal):
    print(animal.speak())

make_sound(Dog())
make_sound(Cat())
```

### Инкапсуляция

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False

    def get_balance(self):
        return self._balance
```

## 4. Функциональное программирование

Функции как объекты первого класса, чистые функции, неизменяемость, функции высшего порядка.

### map

```python
nums = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, nums))
print(squares)  # [1, 4, 9, 16, 25]
```

### filter

```python
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)  # [2, 4]
```

### reduce

```python
from functools import reduce
product = reduce(lambda a, b: a * b, nums)
print(product)  # 120
```

### Чистые функции

```python
# чистая — одинаковый вход = одинаковый выход, нет побочных эффектов
def add(a, b):
    return a + b

# нечистая — зависит от внешнего состояния
counter = 0
def increment():
    global counter
    counter += 1
    return counter
```

### Неизменяемость

```python
# функциональный стиль — не изменять данные
nums = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, nums))
# nums не изменился

# вместо изменения списка — создавать новый
def add_element(lst, item):
    return lst + [item]  # новый список

original = [1, 2, 3]
new = add_element(original, 4)
print(original)  # [1, 2, 3]
print(new)       # [1, 2, 3, 4]
```

### Функции высшего порядка

```python
def apply_twice(func, value):
    return func(func(value))

result = apply_twice(lambda x: x * 2, 5)
print(result)  # 20

def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))  # 10
print(triple(5))  # 15
```

## 5. Декларативное программирование

Описывает ЧТО нужно сделать, а не КАК.

```python
# императивно
evens = []
for x in range(20):
    if x % 2 == 0:
        evens.append(x)

# декларативно (list comprehension)
evens = [x for x in range(20) if x % 2 == 0]

# SQLAlchemy (декларативный ORM)
# users = session.query(User).filter(User.age > 18).all()
```

## 6. Аспектно-ориентированное (через декораторы)

```python
from functools import wraps

def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Вызов {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def process(data):
    return data * 2

process(5)
```

## 7. Асинхронное программирование

```python
import asyncio

async def fetch_data(url):
    print(f"Загрузка {url}")
    await asyncio.sleep(1)
    return f"Данные с {url}"

async def main():
    tasks = [
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3"),
    ]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

## 8. Сравнение парадигм

| Парадигма | Фокус | Когда использовать |
|---|---|---|
| Процедурная | Функции, последовательность | Простые скрипты |
| ООП | Объекты, классы | Сложные системы, GUI |
| Функциональная | Чистые функции, map/filter | Обработка данных |
| Декларативная | Что сделать | SQL, list comprehension |
| Асинхронная | Конкурентность | I/O, сеть, API |

## 9. Комбинирование парадигм

Python позволяет сочетать парадигмы в одном проекте.

```python
# функциональный map + ООП
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def is_adult(self):
        return self.age >= 18

users = [
    User("Анна", 25),
    User("Борис", 17),
    User("Вика", 22),
]

# map + filter — функциональный подход к списку объектов
adult_names = list(map(
    lambda u: u.name,
    filter(lambda u: u.is_adult(), users)
))

# или через list comprehension (более питонично)
adult_names = [u.name for u in users if u.is_adult()]

# генератор + ООП
def adult_generator(users):
    for u in users:
        if u.is_adult():
            yield u.name

for name in adult_generator(users):
    print(f"Взрослый: {name}")
```
