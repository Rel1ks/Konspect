# Generator Expressions

**Generator expression** — ленивый аналог list comprehension. Создаёт генератор, который вычисляет элементы по одному по мере необходимости.

## 1. Синтаксис

Круглые скобки вместо квадратных.

```python
# list comprehension — создаёт список в памяти
list_comp = [x ** 2 for x in range(10)]
print(list_comp)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# generator expression — ленивый
gen_expr = (x ** 2 for x in range(10))
print(gen_expr)   # <generator object>
print(list(gen_expr))  # [0, 1, 4, ...]
```

## 2. Ленивость

Элементы вычисляются только когда запрошены.

```python
def expensive(x):
    print(f"вычисление {x}")
    return x ** 2

# list — вычисляет всё сразу
squares = [expensive(x) for x in range(5)]
# вычисление 0, 1, 2, 3, 4 (сразу)

# generator — вычисляет по запросу
squares = (expensive(x) for x in range(5))
# ничего не выведено
print(next(squares))  # вычисление 0 → 0
print(next(squares))  # вычисление 1 → 1
```

## 3. Использование в функциях

Generator expression часто передаётся напрямую в функцию (можно без двойных скобок).

```python
# сумма квадратов (без создания списка)
total = sum(x ** 2 for x in range(10))

# проверка
any_even = any(x % 2 == 0 for x in numbers)
all_positive = all(x > 0 for x in numbers)

# минимум/максимум по условию
min_len = min(len(w) for w in words)
max_len = max(len(w) for w in words)
```

```python
# обе записи работают
sum((x ** 2 for x in range(10)))  # с доп. скобками
sum(x ** 2 for x in range(10))    # без (предпочтительно)
```

## 4. Экономия памяти

```python
import sys

# список — занимает память
list_comp = [x for x in range(1000000)]
print(sys.getsizeof(list_comp))  # ~8 MB

# генератор — почти не занимает
gen_expr = (x for x in range(1000000))
print(sys.getsizeof(gen_expr))   # ~112 bytes
```

## 5. Фильтрация

```python
# с условием
evens = (x for x in range(20) if x % 2 == 0)
print(list(evens))

# тернарный if-else
tags = ("чёт" if x % 2 == 0 else "нечёт" for x in range(5))
```

## 6. Вложенные циклы

```python
# все пары
pairs = ((i, j) for i in range(3) for j in range(2))
print(list(pairs))

# flatten
matrix = [[1, 2], [3, 4], [5, 6]]
flat = (x for row in matrix for x in row)
print(list(flat))
```

## 7. Generator expression vs list comprehension

| | list comprehension | generator expression |
|---|---|---|
| Память | O(n) | O(1) |
| Скорость создания | Быстрее список | Быстрее генератор |
| Итерация | Многократная | Однократная |
| Индексация | Да | Нет |
| len() | Да | Нет |

```python
# генератор одноразовый
gen = (x for x in [1, 2, 3])
print(list(gen))  # [1, 2, 3]
print(list(gen))  # [] — пусто

# список можно обходить сколько угодно
lst = [1, 2, 3]
print(lst)  # [1, 2, 3]
print(lst)  # [1, 2, 3]
```

## 8. Преобразование в другие типы

```python
gen = (x ** 2 for x in range(5))

# в список
print(list(gen))  # [0, 1, 4, 9, 16]

# во множество
gen = (x % 3 for x in range(10))
print(set(gen))

# в кортеж
gen = (x for x in range(5))
print(tuple(gen))
```

## 9. Бесконечные генераторы

```python
# бесконечный — осторожно!
# inf = (x for x in count(0))

# list(inf)  # никогда не закончится
# for x in inf:  # бесконечный цикл
#     print(x)

# нужно с условием остановки
def take(n, gen):
    for _ in range(n):
        yield next(gen)

first_10 = list(x for x in range(10))  # безопасно
```

## 10. Chaining (цепочки генераторов)

```python
# цепочка фильтров и преобразований
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# через несколько генераторов
evens = (x for x in numbers if x % 2 == 0)
squares = (x ** 2 for x in evens)
result = list(squares)
print(result)  # [4, 16, 36, 64, 100]

# цепочка — ленивая, вычисление происходит один раз
```

## 11. Generator expression с open()

```python
# чтение файла лениво (по строкам)
with open("file.txt") as f:
    lines = (line.strip() for line in f)
    non_empty = (line for line in lines if line)
    for line in non_empty:
        print(line)

# сумма чисел в файле
with open("numbers.txt") as f:
    total = sum(int(line) for line in f)
```

## 12. dict и set comprehension vs generator

```python
# dict comprehension — не ленивый
d = {x: x ** 2 for x in range(5)}

# нет "generator expression" для dict/set
# но можно так:
gen = ((x, x ** 2) for x in range(5))
d = dict(gen)

# set comprehension — не ленивый
s = {x % 3 for x in range(10)}

# generator для set
gen = (x % 3 for x in range(10))
s = set(gen)
```

## 13. Практические примеры

```python
# чтение больших файлов лениво
def read_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

# обработка без загрузки всего в память
lines = read_lines("huge_file.txt")
filtered = (line for line in lines if "error" in line)
for line in filtered:
    print(line)

# группировка данных
data = [("a", 1), ("b", 2), ("a", 3), ("b", 4)]
grouped = ((k, sum(v for _, v in data if _ == k)) for k in {"a", "b"})

# генератор URL
base_url = "https://api.example.com/page"
urls = (f"{base_url}/{i}" for i in range(1, 11))
```
