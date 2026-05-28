# Контекстные менеджеры (Context Manager)

**Context manager** — объект, управляющий ресурсами с гарантированной очисткой даже при ошибках.

## 1. `with` — оператор контекста

```python
with open("file.txt", "r") as f:
    content = f.read()
# файл автоматически закроется
```

## 2. Как это работает

```python
# эквивалент:
f = open("file.txt", "r")
try:
    content = f.read()
finally:
    f.close()
```

## 3. Создание через класс

Нужны методы `__enter__` и `__exit__`.

```python
class ManagedFile:
    def __init__(self, filename, mode="r"):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        print(f"Открытие {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        print(f"Закрытие {self.filename}")
        if exc_type:
            print(f"Ошибка: {exc_val}")
        return False  # не подавлять исключение

with ManagedFile("test.txt", "w") as f:
    f.write("Hello, World!")
```

### Параметры `__exit__`

| Параметр | Описание |
|---|---|
| `exc_type` | Тип исключения (None если нет) |
| `exc_val` | Значение исключения |
| `exc_tb` | Traceback |

```python
def __exit__(self, exc_type, exc_val, exc_tb):
    if exc_type is None:
        # всё хорошо
        return False
    # произошла ошибка
    if exc_type == ValueError:
        print("Перехватили ValueError")
        return True  # подавить исключение
    return False  # не подавлять
```

## 4. Создание через `@contextmanager`

```python
from contextlib import contextmanager

@contextmanager
def managed_file(filename, mode="r"):
    print(f"Открытие {filename}")
    f = open(filename, mode)
    try:
        yield f  # то, что возвращает with ... as
    finally:
        print(f"Закрытие {filename}")
        f.close()

with managed_file("test.txt", "w") as f:
    f.write("Hello, World!")
```

```python
@contextmanager
def temporary_redirect():
    import sys
    old_stdout = sys.stdout
    sys.stdout = open("output.txt", "w")
    try:
        yield
    finally:
        sys.stdout.close()
        sys.stdout = old_stdout

with temporary_redirect():
    print("Это попадёт в файл, а не в консоль")
```

## 5. Встроенные контекстные менеджеры

```python
# open
with open("file.txt") as f:
    pass

# lock
import threading
lock = threading.Lock()
with lock:
    pass  # критическая секция

# subprocess
import subprocess
with subprocess.Popen(["ls"]) as proc:
    pass

# decimal
from decimal import localcontext
with localcontext() as ctx:
    ctx.prec = 50
    print(Decimal(1) / Decimal(3))
```

## 6. `contextlib.redirect_stdout`

```python
from contextlib import redirect_stdout

with open("output.txt", "w") as f:
    with redirect_stdout(f):
        print("Это в файл")
        print("И это тоже")
```

## 7. `contextlib.suppress`

Подавление определённых исключений.

```python
from contextlib import suppress

# вместо:
try:
    os.remove("file.txt")
except FileNotFoundError:
    pass

# можно так:
with suppress(FileNotFoundError):
    os.remove("file.txt")

# несколько исключений
with suppress(FileNotFoundError, PermissionError):
    os.remove("file.txt")
```

## 8. `contextlib.nullcontext`

Заглушка, когда контекст не нужен.

```python
from contextlib import nullcontext

def process(need_db=False):
    if need_db:
        ctx = database_connection()
    else:
        ctx = nullcontext()

    with ctx as conn:
        # если need_db=False, conn будет None
        pass
```

## 9. `contextlib.ExitStack`

Управление несколькими контекстными менеджерами.

```python
from contextlib import ExitStack

with ExitStack() as stack:
    files = [
        stack.enter_context(open(f"file_{i}.txt", "w"))
        for i in range(3)
    ]
    for f in files:
        f.write("data")
    # все файлы закроются при выходе из with
```

```python
# условное открытие
def open_files(names):
    with ExitStack() as stack:
        files = [
            stack.enter_context(open(name))
            for name in names
        ]
        return files  # файлы останутся открыты!
```

## 10. Контекстный менеджер для таймера

```python
import time
from contextlib import contextmanager

@contextmanager
def timer(label="Time"):
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"{label}: {end - start:.4f} сек")

with timer("Загрузка"):
    time.sleep(1)
# Загрузка: 1.0000 сек
```

## 11. Контекстный менеджер для БД

```python
@contextmanager
def db_connection(uri):
    conn = create_connection(uri)
    try:
        yield conn
        conn.commit()  # успешно — коммит
    except Exception:
        conn.rollback()  # ошибка — откат
        raise
    finally:
        conn.close()

with db_connection("sqlite:///db.sqlite") as conn:
    conn.execute("INSERT INTO users VALUES (?)", ("Анна",))
```

## 12. Асинхронный контекстный менеджер

```python
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_managed():
    print("Вход")
    try:
        yield "значение"
    finally:
        print("Выход")

async def main():
    async with async_managed() as val:
        print(val)

asyncio.run(main())
```

```python
class AsyncResource:
    async def __aenter__(self):
        print("Подключение")
        await asyncio.sleep(1)
        return self

    async def __aexit__(self, *args):
        print("Отключение")
        await asyncio.sleep(0.5)

async def use_resource():
    async with AsyncResource() as res:
        print("Работа с ресурсом")
```

## 13. Несколько контекстов

```python
# оба варианта работают
with open("a.txt") as a, open("b.txt") as b:
    content = a.read() + b.read()

with open("a.txt") as a:
    with open("b.txt") as b:
        content = a.read() + b.read()
```

## 14. Практические примеры

```python
# временная смена директории
import os
from contextlib import contextmanager

@contextmanager
def cd(path):
    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)

with cd("/tmp"):
    print(os.getcwd())  # /tmp
print(os.getcwd())      # обратно

# временный файл
import tempfile
with tempfile.TemporaryFile() as f:
    f.write(b"temp data")
    f.seek(0)
    print(f.read())  # файл удалится при выходе
```
