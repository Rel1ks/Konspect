# Multiprocessing

**multiprocessing** — модуль для параллельного выполнения кода через отдельные процессы. Обходит GIL, использует несколько ядер CPU.

## 1. Process

```python
import multiprocessing
import os

def worker(name):
    print(f"Процесс {name}, PID: {os.getpid()}")

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=worker, args=("A",))
    p2 = multiprocessing.Process(target=worker, args=("B",))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
```

### Параметры Process

```python
p = multiprocessing.Process(
    target=func,
    args=(arg1,),
    kwargs={"key": "value"},
    name="Worker-1",
    daemon=True,  # процесс-демон
)
```

## 2. Pool

Пул процессов для параллельного выполнения задач.

```python
from multiprocessing import Pool
import time

def square(x):
    time.sleep(0.5)
    return x * x

if __name__ == "__main__":
    with Pool(4) as pool:
        # map — блокирующий
        results = pool.map(square, range(10))

        # imap — ленивый (по одному результату)
        for result in pool.imap(square, range(10)):
            print(result)

        # imap_unordered — в порядке завершения
        for result in pool.imap_unordered(square, range(10)):
            print(result)

        # apply — один вызов
        result = pool.apply(square, (5,))

        # apply_async — асинхронный
        async_result = pool.apply_async(square, (5,))
        print(async_result.get(timeout=2))

        # starmap — с распаковкой аргументов
        results = pool.starmap(pow, [(2, 3), (3, 4), (4, 5)])
```

## 3. ProcessPoolExecutor (concurrent.futures)

Альтернативный интерфейс для пула процессов.

```python
from concurrent.futures import ProcessPoolExecutor
import time

def task(n):
    time.sleep(0.5)
    return n * 2

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        # map
        results = list(executor.map(task, range(10)))

        # submit
        futures = [executor.submit(task, i) for i in range(10)]
        for future in futures:
            print(future.result())

        # as_completed — по готовности
        from concurrent.futures import as_completed
        for future in as_completed(futures):
            print(future.result())
```

## 4. Передача данных между процессами

### Queue

```python
from multiprocessing import Process, Queue

def producer(q):
    for i in range(5):
        q.put(i)

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"Получено: {item}")

if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    q.put(None)
    p2.join()
```

### Pipe

```python
from multiprocessing import Process, Pipe

def worker(conn):
    conn.send("Привет от worker")
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    p = Process(target=worker, args=(child_conn,))
    p.start()

    msg = parent_conn.recv()
    print(msg)  # Привет от worker

    p.join()
```

### Value и Array (разделяемая память)

```python
from multiprocessing import Process, Value, Array

def increment(counter, arr):
    counter.value += 1
    for i in range(len(arr)):
        arr[i] *= 2

if __name__ == "__main__":
    counter = Value("i", 0)  # int, начальное 0
    arr = Array("i", [1, 2, 3])

    p = Process(target=increment, args=(counter, arr))
    p.start()
    p.join()

    print(counter.value)
    print(arr[:])
```

### Типы для Value/Array

| Код | Тип | Размер |
|---|---|---|
| `'b'` | signed char | 1 |
| `'B'` | unsigned char | 1 |
| `'h'` | signed short | 2 |
| `'H'` | unsigned short | 2 |
| `'i'` | signed int | 4 |
| `'I'` | unsigned int | 4 |
| `'f'` | float | 4 |
| `'d'` | double | 8 |

## 5. Manager

Менеджер для разделяемых объектов (list, dict, и т.д.).

```python
from multiprocessing import Process, Manager

def worker(d, lst, name):
    d[name] = len(name)
    lst.append(name)

if __name__ == "__main__":
    with Manager() as manager:
        d = manager.dict()
        lst = manager.list()

        processes = [
            Process(target=worker, args=(d, lst, f"proc{i}"))
            for i in range(3)
        ]

        for p in processes: p.start()
        for p in processes: p.join()

        print(dict(d))
        print(list(lst))
```

## 6. Lock и синхронизация

```python
from multiprocessing import Process, Lock

def worker(lock, counter):
    for _ in range(100):
        with lock:
            counter.value += 1

if __name__ == "__main__":
    lock = Lock()
    counter = Value("i", 0)

    processes = [Process(target=worker, args=(lock, counter)) for _ in range(4)]
    for p in processes: p.start()
    for p in processes: p.join()

    print(counter.value)  # 400
```

### Другие примитивы

```python
from multiprocessing import Lock, RLock, Semaphore, Event, Condition

sem = Semaphore(3)  # не больше 3 одновременно
event = Event()      # ожидание сигнала
cond = Condition()   # условная переменная
```

## 7. CPU-bound примеры

### Числа Фибоначчи

```python
from multiprocessing import Pool
import time

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

if __name__ == "__main__":
    numbers = [500000] * 8

    # один поток
    start = time.time()
    results = [fib(n) for n in numbers]
    print(f"Single: {time.time() - start:.2f} сек")

    # несколько процессов
    start = time.time()
    with Pool(4) as pool:
        results = pool.map(fib, numbers)
    print(f"Pool(4): {time.time() - start:.2f} сек")
```

### Простые числа

```python
import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def count_primes(limit):
    return sum(1 for n in range(limit) if is_prime(n))

if __name__ == "__main__":
    ranges = [(0, 100000), (100000, 200000), (200000, 300000)]

    with Pool(3) as pool:
        results = pool.starmap(count_primes, [(r[1] - r[0]) for r in ranges])
        print(sum(results))
```

## 8. initializer и initargs

Инициализация перед запуском процессов (например, подключение к БД).

```python
from multiprocessing import Pool

def init_worker():
    global db
    db = create_connection()

def worker_task(id):
    return db.query(id)

if __name__ == "__main__":
    with Pool(4, initializer=init_worker) as pool:
        results = pool.map(worker_task, range(100))
```

## 9. multiprocessing vs threading vs asyncio

| | multiprocessing | threading | asyncio |
|---|---|---|---|
| GIL | Нет | Да | Да |
| CPU-bound | ✅ | ❌ | ❌ |
| I/O-bound | ✅ | ✅ | ✅ |
| Память | Раздельная | Общая | Общая |
| Создание | Тяжёлое | Лёгкое | Очень лёгкое |
| Количество | ~CPU cores | ~1000 | ~10000+ |
| Обмен данными | Queue, Pipe, Manager | Queue, Lock | await |
