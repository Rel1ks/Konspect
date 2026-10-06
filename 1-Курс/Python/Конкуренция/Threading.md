# Threading

**threading** — модуль для работы с потоками. Потоки выполняются в одном процессе, делят память, ограничены GIL для CPU-нагрузки.

## 1. Thread

```python
import threading
import time

def worker(name):
    print(f"Поток {name} начал")
    time.sleep(1)
    print(f"Поток {name} завершил")

# создание и запуск
t = threading.Thread(target=worker, args=("A",))
t.start()

# ожидание завершения
t.join()

print("Главный поток завершён")
```

### Параметры Thread

```python
t = threading.Thread(
    target=func,
    args=(arg1,),
    kwargs={"key": "value"},
    name="WorkerThread",
    daemon=True,  # поток-демон (завершится с главным)
)
```

## 2. Daemon-потоки

```python
import threading
import time

def background():
    while True:
        print("Фоновая работа...")
        time.sleep(1)

daemon = threading.Thread(target=background, daemon=True)
daemon.start()

time.sleep(3)
print("Главный завершён")  # daemon умрёт вместе с главным
```

## 3. ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor
import time

def task(n):
    time.sleep(0.5)
    return n * 2

with ThreadPoolExecutor(max_workers=4) as executor:
    # map
    results = list(executor.map(task, range(10)))

    # submit
    futures = [executor.submit(task, i) for i in range(10)]
    for future in futures:
        print(future.result())

    # as_completed
    from concurrent.futures import as_completed
    for future in as_completed(futures):
        print(future.result())
```

## 4. Lock — блокировка

Защита от состояния гонки (race condition).

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1
        # lock.acquire()
        # counter += 1
        # lock.release()

threads = [threading.Thread(target=increment) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print(counter)  # 500000
```

### RLock — реентерабельный Lock

```python
lock = threading.RLock()

# можно захватить несколько раз в одном потоке
with lock:
    with lock:
        counter += 1
```

## 5. Event — событие

Один поток сигналит, другой ждёт.

```python
import threading
import time

event = threading.Event()

def waiter():
    print("Ожидание события...")
    event.wait()
    print("Событие получено!")

def setter():
    print("Подготовка...")
    time.sleep(2)
    print("Отправка события")
    event.set()

t1 = threading.Thread(target=waiter)
t2 = threading.Thread(target=setter)
t1.start(); t2.start()
t1.join(); t2.join()
```

## 6. Condition — условная переменная

```python
import threading
import time

condition = threading.Condition()
items = []

def producer():
    for i in range(5):
        with condition:
            items.append(i)
            print(f"Произведено: {i}")
            condition.notify()
        time.sleep(0.5)

def consumer():
    while True:
        with condition:
            while not items:
                condition.wait()
            item = items.pop(0)
            print(f"Потреблено: {item}")
        if item == 4:
            break

t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start(); t2.start()
t1.join(); t2.join()
```

## 7. Semaphore — семафор

Ограничение количества одновременных доступов.

```python
import threading
import time

semaphore = threading.Semaphore(3)

def worker(id):
    with semaphore:
        print(f"Работает поток {id}")
        time.sleep(1)

threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
for t in threads: t.start()
for t in threads: t.join()
```

### BoundedSemaphore

```python
sem = threading.BoundedSemaphore(3)
# не даст сделать release() больше раз, чем acquire()
```

## 8. Barrier — барьер

Синхронизация N потоков в одной точке.

```python
import threading
import time

barrier = threading.Barrier(3)

def worker(id):
    print(f"Поток {id} ждёт у барьера")
    barrier.wait()
    print(f"Поток {id} прошёл барьер")

threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for t in threads: t.start()
for t in threads: t.join()
```

## 9. Queue — потокобезопасная очередь

```python
from queue import Queue
import threading
import time

queue = Queue()

def producer():
    for i in range(5):
        print(f"→ {i}")
        queue.put(i)
        time.sleep(0.5)

def consumer():
    while True:
        item = queue.get()
        if item is None:
            break
        print(f"  ← {item}")
        queue.task_done()

t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start(); t2.start()
t1.join()
queue.put(None)
t2.join()
```

## 10. Local — локальные данные потока

Каждый поток имеет свою копию данных.

```python
import threading

local = threading.local()

def worker():
    local.value = threading.current_thread().name
    print(f"{local.value}")

t1 = threading.Thread(target=worker, name="Thread-A")
t2 = threading.Thread(target=worker, name="Thread-B")
t1.start(); t2.start()
t1.join(); t2.join()
# local.value разный для каждого потока
```

## 11. Timer — отложенный запуск

```python
import threading

def hello():
    print("Hello, World!")

timer = threading.Timer(2.0, hello)
timer.start()

timer.cancel()  # отменить
```

## 12. Практические примеры

### Пул потоков вручную

```python
import threading
from queue import Queue

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue()
        self.workers = []

        for _ in range(num_threads):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            self.workers.append(t)

    def _worker(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Ошибка: {e}")
            finally:
                self.tasks.task_done()

    def submit(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def wait(self):
        self.tasks.join()

pool = ThreadPool(4)

def task(n):
    print(f"Task {n}")

for i in range(10):
    pool.submit(task, i)

pool.wait()
```

### I/O-bound задача

```python
import threading
import requests

def fetch(url, results):
    response = requests.get(url)
    results.append(len(response.content))

urls = ["https://example.com"] * 20
results = []
threads = []

for url in urls:
    t = threading.Thread(target=fetch, args=(url, results))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(sum(results))
```

## 13. Threading vs multiprocessing vs asyncio

| | threading | multiprocessing | asyncio |
|---|---|---|---|
| GIL | Да | Нет | Да |
| CPU-bound | ❌ | ✅ | ❌ |
| I/O-bound | ✅ | ✅ | ✅ |
| Память | Общая | Раздельная | Общая |
| Создание | Лёгкое | Тяжёлое | Очень лёгкое |
| Количество | ~1000 | ~ядра CPU | ~10000+ |
| Синхронизация | Lock, Queue | Queue, Pipe | await |
