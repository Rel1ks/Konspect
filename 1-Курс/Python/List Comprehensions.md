# List Comprehensions

**List comprehension** — компактный способ создания списков. Заменяет цикл `for` в одну строку.

## 1. Базовый синтаксис

| Синтаксис | Описание |
|---|---|
| `[expr for x in seq]` | Применить выражение к каждому элементу |
| `[expr for x in seq if cond]` | С фильтрацией |
| `[expr if cond else other for x in seq]` | С тернарным условием |

```python
# обычный цикл
squares = []
for x in range(10):
    squares.append(x ** 2)

# comprehension
squares = [x ** 2 for x in range(10)]
```

## 2. Примеры

```python
nums = [1, 2, 3, 4, 5]

# удвоение
doubled = [x * 2 for x in nums]

# квадраты
squares = [x ** 2 for x in nums]

# строки
words = ["hello", "world", "python"]
upper = [w.upper() for w in words]
lengths = [len(w) for w in words]
```

## 3. С фильтром (if)

```python
# чётные числа
evens = [x for x in range(20) if x % 2 == 0]

# числа больше 5
big = [x for x in nums if x > 5]

# строки длиннее 3
long = [w for w in words if len(w) > 3]

# гласные из строки
vowels = [ch for ch in "hello world" if ch in "aeiou"]
```

## 4. С тернарным условием (if-else)

```python
# if-else ПЕРЕД for
tags = ["чёт" if x % 2 == 0 else "нечёт" for x in range(10)]

# знак числа
signs = ["+" if x > 0 else "-" if x < 0 else "0" for x in [-3, 0, 5]]
```

## 5. Вложенные циклы

```python
# все пары
pairs = [(i, j) for i in range(3) for j in range(2)]
# [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1)]

# таблица умножения
table = [f"{i}*{j}={i*j}" for i in range(1, 10) for j in range(1, 10)]

# с фильтром
pairs = [(i, j) for i in range(5) for j in range(5) if i != j]
```

## 6. flatten (сплющивание)

```python
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6]

# вложенные списки разной глубины
nested = [[1, 2, [3, 4]], [5, [6, 7]], 8]
# для разной глубины нужна рекурсия
```

## 7. С функциями

```python
import math

nums = [1, 4, 9, 16, 25]
roots = [math.sqrt(x) for x in nums]

# с собственной функцией
def process(x):
    return x * 2 + 1

result = [process(x) for x in nums]
```

## 8. Dict comprehension

```python
# {key: value for x in seq}
squares = {x: x ** 2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 25}

# инвертирование словаря
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}

# фильтр
even_squares = {x: x ** 2 for x in range(10) if x % 2 == 0}
```

## 9. Set comprehension

```python
# {expr for x in seq}
unique = {x % 3 for x in range(10)}
# {0, 1, 2}

squares_set = {x ** 2 for x in range(5)}

# фильтр
evens = {x for x in range(20) if x % 2 == 0}
```

## 10. Generator expression (ленивый)

Круглые скобки — генератор, а не tuple comprehension.

```python
# генератор (ленивый)
squares = (x ** 2 for x in range(10))
print(squares)  # <generator object>
print(list(squares))

# сумма квадратов (без создания списка)
total = sum(x ** 2 for x in range(10))

# проверка
any_even = any(x % 2 == 0 for x in nums)
all_positive = all(x > 0 for x in nums)
```

## 11. Вложенные comprehensions

```python
# матрица
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
# [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

# транспонирование
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
```

## 12. Практические примеры

```python
# извлечение данных из списка словарей
users = [
    {"name": "Анна", "age": 25},
    {"name": "Борис", "age": 30},
    {"name": "Вика", "age": 22},
]
names = [u["name"] for u in users]
adults = [u for u in users if u["age"] >= 18]

# обработка файлов
files = ["data.csv", "image.png", "doc.txt"]
csvs = [f for f in files if f.endswith(".csv")]

# удаление дубликатов (с сохранением порядка)
seen = set()
unique = [x for x in [1, 2, 2, 3, 3, 3] if not (x in seen or seen.add(x))]

# матрица из строк
data = "1 2 3\n4 5 6\n7 8 9"
matrix = [[int(x) for x in row.split()] for row in data.split("\n")]

# все комбинации
colors = ["красный", "синий"]
sizes = ["S", "M", "L"]
products = [f"{c} {s}" for c in colors for s in sizes]
```

## 13. Производительность

```python
# comprehension быстрее, чем append в цикле
import timeit

def with_loop():
    result = []
    for i in range(1000):
        result.append(i ** 2)
    return result

def with_comprehension():
    return [i ** 2 for i in range(1000)]

# timeit.show(with_loop, number=10000)
# timeit.show(with_comprehension, number=10000)
```

## 14. Когда не стоит использовать

```python
# сложные comprehension — лучше цикл
# плохо:
matrix = [[x * y for x in range(1, 100) if x % 2 == 0] for y in range(1, 100) if y % 3 == 0]

# хорошо:
result = []
for y in range(1, 100):
    if y % 3 == 0:
        row = []
        for x in range(1, 100):
            if x % 2 == 0:
                row.append(x * y)
        result.append(row)
```
