# Glob Module in Python

**glob** — поиск файлов по шаблону (wildcard). Встроенный модуль.

## 1. Базовое использование

```python
import glob

# все .txt файлы в текущей папке
glob.glob("*.txt")

# все .py во всех вложенных папках
glob.glob("**/*.py", recursive=True)
```

## 2. glob()

```python
# список файлов (по алфавиту)
txt_files = glob.glob("*.txt")

# вложенные папки
glob.glob("src/**/*.py", recursive=True)

# несколько символов
glob.glob("data/*.csv")
glob.glob("data/*.txt")
glob.glob("data/*.*")

# один символ
glob.glob("data/file_?.txt")   # file_1.txt, file_a.txt

# диапазон символов
glob.glob("data/[abc]*.txt")   # a*, b*, c*
glob.glob("data/[0-9]*.txt")   # начинающиеся с цифры
glob.glob("data/[!0-9]*.txt")  # НЕ цифра
```

## 3. iglob()

```python
# итератор (память эффективно)
for f in glob.iglob("data/*.csv"):
    process(f)
```

## 4. Шаблоны

| Шаблон | Описание | Пример |
|---|---|---|
| `*` | Любые символы (кроме `/`) | `*.txt` |
| `**` | Любая вложенность (recursive) | `**/*.py` |
| `?` | Один любой символ | `file_?.txt` |
| `[abc]` | Один из символов | `[0-9]*` |
| `[!abc]` | Любой кроме | `[!0-9]*` |
| `[a-z]` | Диапазон | `[a-f]*` |

## 5. pathlib — Glob

```python
from pathlib import Path

# аналогично glob(), но возвращает Path
p = Path(".")

for f in p.glob("*.txt"):
    print(f.name, f.suffix, f.stat().st_size)

# рекурсивно
for f in p.rglob("*.py"):
    print(f.relative_to(p))
```

## 6. pathlib vs glob

```python
# glob модуль
import glob
glob.glob("src/**/*.py", recursive=True)

# pathlib
from pathlib import Path
Path("src").rglob("*.py")
# или
Path("src").glob("**/*.py")
```

## 7. Примеры

```python
import glob
from pathlib import Path

# все изображения
extensions = ["*.jpg", "*.png", "*.gif"]
images = []
for ext in extensions:
    images.extend(glob.glob(f"images/**/{ext}", recursive=True))

# найти все README
for readme in Path(".").rglob("README*"):
    print(readme)

# последний изменённый файл
files = glob.glob("logs/*.log")
latest = max(files, key=os.path.getmtime)

# фильтр по размеру
big_files = [
    f for f in Path(".").rglob("*")
    if f.is_file() and f.stat().st_size > 10 * 1024 * 1024
]
```
