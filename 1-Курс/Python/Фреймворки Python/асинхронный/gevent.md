# gevent

**gevent** — библиотека для асинхронного I/O на основе greenlet. Использует зелёные потоки (greenlets) и неблокирующие сокеты.

## 1. Установка

```bash
pip install gevent
```

## 2. Greenlets (зелёные потоки)

Лёгкие потоки, работающие в одном потоке ОС.

```python
import gevent

def task(name):
    print(f"Задача {name} началась")
    gevent.sleep(1)  # неблокирующая задержка
    print(f"Задача {name} завершена")

tasks = [
    gevent.spawn(task, "A"),
    gevent.spawn(task, "B"),
    gevent.spawn(task, "C"),
]

gevent.joinall(tasks)
```

## 3. Monkey patching

Замена блокирующих вызовов (socket, time, threading) на неблокирующие аналоги.

```python
from gevent import monkey
monkey.patch_all()  # заменить всё

import time
import socket
import threading

# теперь time.sleep() не блокирует — gevent.sleep()
# socket.connect() — неблокирующий
# threading — в рамках одного потока
```

```python
# выборочное патчинг
monkey.patch_socket()
monkey.patch_time()
monkey.patch_thread()
monkey.patch_ssl()
```

## 4. Синхронный vs асинхронный

```python
import time
import gevent
from gevent import monkey
monkey.patch_all()

def fetch(url):
    print(f"Загрузка {url}")
    time.sleep(2)  # обычно блокирует, но gevent это перехватывает
    print(f"Загружено {url}")
    return url

# синхронно — 6 секунд
start = time.time()
results = [fetch("url1"), fetch("url2"), fetch("url3")]
print(f"Синхронно: {time.time() - start:.1f} сек")

# асинхронно — 2 секунды
start = time.time()
tasks = [gevent.spawn(fetch, f"url{i}") for i in range(3)]
gevent.joinall(tasks)
results = [task.value for task in tasks]
print(f"Асинхронно: {time.time() - start:.1f} сек")
```

## 5. Обработка ошибок

```python
import gevent

def safe_task(url):
    try:
        # работа
        result = fetch(url)
        return result
    except Exception as e:
        print(f"Ошибка {url}: {e}")
        return None

tasks = [gevent.spawn(safe_task, f"url{i}") for i in range(3)]
gevent.joinall(tasks)

for task in tasks:
    if task.successful():
        print(f"Успех: {task.value}")
    else:
        print(f"Ошибка: {task.exception}")
```

## 6. Pool — пул greenlet'ов

Контроль количества одновременных задач.

```python
from gevent.pool import Pool

pool = Pool(10)  # не больше 10 одновременно

def worker(url):
    print(f"Обработка {url}")
    gevent.sleep(1)
    return url.upper()

urls = [f"url{i}" for i in range(100)]
results = pool.map(worker, urls)

# imap — ленивый
for result in pool.imap(worker, urls):
    print(result)

# imap_unordered — в порядке завершения
for result in pool.imap_unordered(worker, urls):
    print(f"Готово: {result}")
```

## 7. gevent.queue

```python
import gevent
from gevent.queue import Queue

queue = Queue()

def producer():
    for i in range(5):
        print(f"Произвёл: {i}")
        queue.put(i)
        gevent.sleep(0.5)

def consumer():
    while True:
        item = queue.get()
        print(f"Потребил: {item}")
        if item == 4:
            break

tasks = [
    gevent.spawn(producer),
    gevent.spawn(consumer),
]
gevent.joinall(tasks)
```

## 8. gevent.event

```python
import gevent
from gevent.event import Event

event = Event()

def waiter():
    print("Ожидание события...")
    event.wait()
    print("Событие получено!")

def setter():
    print("Подготовка...")
    gevent.sleep(2)
    print("Отправка события")
    event.set()

gevent.joinall([
    gevent.spawn(waiter),
    gevent.spawn(setter),
])
```

## 9. gevent + сокеты

```python
from gevent import socket
from gevent.pool import Pool

pool = Pool(100)

def handle_request(conn, addr):
    try:
        data = conn.recv(1024)
        if data:
            conn.sendall(b"HTTP/1.1 200 OK\r\n\r\nHello")
    finally:
        conn.close()

def server():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("0.0.0.0", 8080))
    listener.listen(128)
    while True:
        conn, addr = listener.accept()
        pool.spawn(handle_request, conn, addr)

if __name__ == "__main__":
    server()
```

## 10. gevent + requests

```python
import gevent
from gevent import monkey
monkey.patch_all()

import requests
from gevent.pool import Pool

def fetch_url(url):
    response = requests.get(url)
    return len(response.content)

urls = [
    "https://example.com",
    "https://httpbin.org/get",
    "https://jsonplaceholder.typicode.com/posts",
]

pool = Pool(10)
results = pool.map(fetch_url, urls)
print(results)
```

## 11. timeout

```python
import gevent
from gevent import Timeout

# таймаут на блок кода
timeout = Timeout(2)
timeout.start()

try:
    gevent.sleep(5)
except Timeout:
    print("Таймаут!")

# или через with
with Timeout(2):
    gevent.sleep(5)
```

## 12. gevent vs asyncio

| | gevent | asyncio |
|---|---|---|
| Подход | Greenlets (зелёные потоки) | async/await |
| Патчинг | monkey.patch_all() | Не нужен |
| Совместимость | Любая библиотека (через патч) | Только async-библиотеки |
| Синтаксис | Как обычный код | async/await |
| Производительность | Высокая | Высокая |
| Популярность | Классический | Современный |

```python
# gevent — пишете обычный код
response = requests.get(url)

# asyncio — нужен async клиент
response = await httpx.AsyncClient().get(url)
```
