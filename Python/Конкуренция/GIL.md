# GIL (Global Interpreter Lock)

**GIL** — глобальная блокировка интерпретатора CPython. Разрешает выполнение только одного потока в каждый момент времени.

## 1. Что такое GIL

```python
# GIL — мьютекс, который не позволяет двум потокам
# CPython выполняться одновременно на разных ядрах
```

- GIL есть только в **CPython** (основная реализация)
- В других реализациях (Jython, IronPython) GIL нет
- GIL упрощает управление памятью (reference counting)
- GIL — причина, почему threading не ускоряет CPU-bound код

## 2. Как GIL влияет на код

### I/O-bound — GIL не мешает

```python
import threading
import time
import requests

def fetch(url):
    response = requests.get(url)
    return len(response.content)

urls = ["https://example.com"] * 10

def sync_version():
    start = time.time()
    results = [fetch(url) for url in urls]
    print(f"Sync: {time.time() - start:.2f} сек")

def threaded_version():
    start = time.time()
    threads = [threading.Thread(target=fetch, args=(u,)) for u in urls]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"Threaded: {time.time() - start:.2f} сек")

# threading ускоряет I/O-bound — GIL отпускается при ожидании
```

### CPU-bound — GIL блокирует

```python
import threading
import time

def count(n):
    while n > 0:
        n -= 1

def single_thread():
    start = time.time()
    count(100_000_000)
    count(100_000_000)
    print(f"Single: {time.time() - start:.2f} сек")

def two_threads():
    start = time.time()
    t1 = threading.Thread(target=count, args=(100_000_000,))
    t2 = threading.Thread(target=count, args=(100_000_000,))
    t1.start(); t2.start()
    t1.join(); t2.join()
    print(f"Two threads: {time.time() - start:.2f} сек")

# два потока НЕ быстрее одного — GIL не отпускается
```

## 3. Как GIL работает

```
Thread 1:  ████████████████░░░░░░░░░░░░░░░░
Thread 2:  ░░░░░░░░░░░░░░████████████████
Time:      ──────────────────────────────→

GIL переключается между потоками каждые ~5ms
```

```python
import sys

# интервал переключения GIL (по умолчанию 5ms)
print(sys.getswitchinterval())

# изменить интервал
sys.setswitchinterval(0.01)
```

## 4. Когда GIL отпускается

GIL отпускается при блокирующих операциях:

- `time.sleep()`
- I/O (сеть, диск, БД)
- Ожидание блокировок (`Lock.acquire()`)
- Вызов C-расширений (numpy, pandas)

```python
import threading
import time

def io_task():
    time.sleep(1)  # GIL отпущен — другой поток работает

def cpu_task():
    for i in range(10_000_000):
        i * i  # GIL захвачен — другие потоки ждут
```

## 5. Обход GIL

### Multiprocessing — процессы (рекомендуется)

```python
from multiprocessing import Pool

def cpu_heavy(n):
    total = 0
    for i in range(n):
        total += i
    return total

if __name__ == "__main__":
    with Pool(4) as pool:
        results = pool.map(cpu_heavy, [50_000_000] * 4)
```

### C-расширения (numpy, Cython)

```python
import numpy as np

# numpy отпускает GIL при операциях над массивами
a = np.random.rand(1000, 1000)
b = np.random.rand(1000, 1000)
c = np.dot(a, b)  # GIL отпущен
```

### asyncio (не обходит, но эффективен для I/O)

```python
import asyncio

async def fetch(url):
    # GIL отпускается при await
    await asyncio.sleep(1)
    return url
```

### Другие реализации Python

```bash
# Jython — нет GIL (Java)
# IronPython — нет GIL (.NET)
# PyPy — есть GIL (но быстрее CPython)
# Cython — можно отключить GIL вручную
```

## 6. Демонстрация GIL

```python
import threading
import time

def count(n):
    while n > 0:
        n -= 1

# 1 поток — 1 ядро
# 2 потока — всё ещё 1 ядро (GIL)
# 2 процесса — 2 ядра (нет GIL)

def benchmark():
    N = 50_000_000

    # один поток
    start = time.time()
    count(N)
    print(f"1 поток: {time.time() - start:.2f} сек")

    # два потока
    start = time.time()
    t1 = threading.Thread(target=count, args=(N,))
    t2 = threading.Thread(target=count, args=(N,))
    t1.start(); t2.start()
    t1.join(); t2.join()
    print(f"2 потока: {time.time() - start:.2f} сек")

    # два процесса
    from multiprocessing import Process
    start = time.time()
    p1 = Process(target=count, args=(N,))
    p2 = Process(target=count, args=(N,))
    p1.start(); p2.start()
    p1.join(); p2.join()
    print(f"2 процесса: {time.time() - start:.2f} сек")

if __name__ == "__main__":
    benchmark()
```

## 7. GIL и C-расширения

```python
# C-расширения могут отпускать GIL вручную

# Пример: ctypes
import ctypes

# Вызов C-функции, которая отпускает GIL
lib = ctypes.CDLL("mylib.so")
lib.heavy_computation.restype = ctypes.c_double

# GIL не удерживается во время C-вызова
result = lib.heavy_computation()

# numpy
import numpy as np
# numpy отпускает GIL при операциях > 100 элементов
```

## 8. GIL в разных версиях Python

```python
# Python 3.2 — улучшенный GIL
# Раньше: переключение каждые 100 инструкций
# Сейчас: переключение каждые 5ms (меньше переключений)

# Python 3.9 — возможность отключить GIL (экспериментально)
# python -X gil=0

# Python 3.13 — free-threaded mode (экспериментально)
# https://peps.python.org/pep-0703/
```

## 9. Мифы о GIL

```python
# ❌ GIL делает Python однопоточным
# ✅ Да, для CPU-bound. Нет, для I/O-bound

# ❌ GIL — это баг Python
# ✅ GIL — архитектурное решение для упрощения памяти

# ❌ multiprocessing обходит GIL полностью
# ✅ Да, но с накладными расходами на IPC

# ❌ asyncio не использует GIL
# ✅ asyncio работает в одном потоке с GIL, но эффективно переключается
```

## 10. Рекомендации

```python
# I/O-bound → asyncio или threading
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# CPU-bound → multiprocessing или numpy
from multiprocessing import Pool

def compute(data):
    return heavy_calculation(data)

with Pool() as pool:
    results = pool.map(compute, dataset)

# Смешанное → сочетать
# Использовать C-расширения для тяжёлых вычислений
# numpy, numba, cython
```
