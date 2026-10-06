# File Handling in Python

**Файловый ввод-вывод** — чтение и запись файлов, работа с путями, временные файлы, сериализация.

## 1. Открытие и закрытие файлов

```python
# базовая запись
file = open("file.txt", "r")
content = file.read()
file.close()

# with — автоматическое закрытие (рекомендуется)
with open("file.txt", "r") as f:
    content = f.read()
```

### Режимы открытия

| Режим | Описание |
|---|---|
| `r` | Чтение (по умолчанию) |
| `w` | Запись (перезапись) |
| `a` | Дозапись в конец |
| `x` | Создание (ошибка если существует) |
| `r+` | Чтение + запись (с начала) |
| `w+` | Чтение + запись (перезапись) |
| `a+` | Чтение + дозапись |
| `b` | Бинарный режим (rb, wb, ab) |
| `t` | Текстовый режим (по умолчанию) |

```python
with open("file.txt", "w", encoding="utf-8") as f:
    f.write("Hello")

with open("file.jpg", "rb") as f:
    data = f.read()
```

## 2. Чтение файлов

```python
# весь файл целиком
with open("file.txt", "r") as f:
    content = f.read()

# построчно в список
with open("file.txt", "r") as f:
    lines = f.readlines()

# построчный итератор (память эффективно)
with open("file.txt", "r") as f:
    for line in f:
        print(line.strip())

# N символов
with open("file.txt", "r") as f:
    chunk = f.read(100)

# readline
with open("file.txt", "r") as f:
    first_line = f.readline()
    second_line = f.readline()
```

## 3. Запись в файлы

```python
with open("file.txt", "w", encoding="utf-8") as f:
    f.write("Строка 1\n")
    f.write("Строка 2\n")

# запись списка строк
lines = ["a\n", "b\n", "c\n"]
with open("file.txt", "w") as f:
    f.writelines(lines)

# дозапись
with open("file.txt", "a") as f:
    f.write("добавлено\n")
```

## 4. Позиция в файле

```python
with open("file.txt", "r") as f:
    print(f.tell())   # текущая позиция

    f.seek(0)         # в начало
    f.seek(10)        # байт 10
    f.seek(0, 2)      # конец файла
    f.seek(-5, 2)     # 5 байт от конца
    f.seek(5, 1)      # 5 от текущей
```

## 5. pathlib (рекомендуется)

```python
from pathlib import Path

path = Path("data/file.txt")

# чтение
content = path.read_text(encoding="utf-8")
content = path.read_bytes()

# запись
path.write_text("Hello", encoding="utf-8")
path.write_bytes(b"data")

# проверки
path.exists()
path.is_file()
path.is_dir()
path.stat().st_size

# имя, расширение, родитель
path.name          # file.txt
path.stem          # file
path.suffix        # .txt
path.parent        # data
path.resolve()     # абсолютный

# создание папок
Path("new/dir").mkdir(parents=True, exist_ok=True)

# обход
for f in Path(".").iterdir():
    print(f)

for py in Path(".").glob("**/*.py"):
    print(py)

for txt in Path(".").rglob("*.txt"):
    print(txt)
```

## 6. os.path

```python
import os

os.path.join("dir", "file.txt")      # dir/file.txt
os.path.exists("file.txt")
os.path.isfile("file.txt")
os.path.isdir("dir")
os.path.basename("dir/file.txt")     # file.txt
os.path.dirname("dir/file.txt")      # dir
os.path.splitext("file.txt")         # ('file', '.txt')
os.path.abspath("file.txt")
os.path.getsize("file.txt")

os.makedirs("a/b/c", exist_ok=True)
os.remove("file.txt")
os.rename("old.txt", "new.txt")
```

## 7. Временные файлы

```python
import tempfile

# временный файл
with tempfile.NamedTemporaryFile(delete=True) as tf:
    tf.write(b"data")
    print(tf.name)

# временная папка
with tempfile.TemporaryDirectory() as td:
    path = Path(td) / "file.txt"
    path.write_text("hello")
```

## 8. Сериализация

### JSON

```python
import json

data = {"name": "Анна", "age": 30}

# запись
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# чтение
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# строка
json_str = json.dumps(data, ensure_ascii=False, indent=2)
data = json.loads(json_str)
```

### Pickle

```python
import pickle

data = {"key": [1, 2, 3]}

with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

with open("data.pkl", "rb") as f:
    data = pickle.load(f)
```

### CSV

```python
import csv

# запись
with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
    writer.writerow(["Анна", 30])
    writer.writerow(["Иван", 25])

# чтение
with open("data.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# DictReader / DictWriter
with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])
```

## 9. Кодировки

```python
with open("file.txt", "r", encoding="utf-8") as f:
    ...

with open("file.txt", "r", encoding="cp1251") as f:
    ...

# обнаружение кодировки
import chardet  # pip install chardet

with open("file.txt", "rb") as f:
    raw = f.read()
    result = chardet.detect(raw)
    print(result["encoding"])
```

## 10. Обработка ошибок

```python
try:
    with open("nope.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("Файл не найден")
except PermissionError:
    print("Нет доступа")
except UnicodeDecodeError:
    print("Ошибка кодировки")

# проверка перед открытием
from pathlib import Path

path = Path("file.txt")
if path.exists() and path.is_file():
    with open(path, "r") as f:
        ...
```

## 11. Полезные функции

```python
# shutil — копирование/перемещение
import shutil

shutil.copy("src.txt", "dst.txt")
shutil.copy2("src.txt", "dst.txt")  # с метаданными
shutil.move("src.txt", "dst.txt")
shutil.copytree("src_dir", "dst_dir")
shutil.rmtree("dir")

# stat
st = Path("file.txt").stat()
print(st.st_size)  # размер
print(st.st_mtime)  # время изменения

# удаление
Path("file.txt").unlink(missing_ok=True)
os.remove("file.txt")
```

## 12. Чтение больших файлов

```python
# построчно — не загружает всё в память
with open("big.txt", "r") as f:
    for line in f:
        process(line)

# чанками
with open("big.txt", "r") as f:
    while chunk := f.read(8192):
        process(chunk)

# mmap — отображение в память
import mmap

with open("big.txt", "r+b") as f:
    with mmap.mmap(f.fileno(), 0) as mm:
        print(mm[:100].decode())
```

## 13. fileinput — обработка нескольких файлов

```python
import fileinput

for line in fileinput.input(files=["a.txt", "b.txt"]):
    print(fileinput.filename(), line.strip())
```
