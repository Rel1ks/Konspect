# FastAPI

**FastAPI** — современный асинхронный веб-фреймворк. Автоматическая документация OpenAPI, валидация через Pydantic, высокая производительность.

## 1. Установка

```bash
pip install fastapi
pip install uvicorn  # ASGI-сервер
```

## 2. Минимальное приложение

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```bash
# или через командную строку
uvicorn main:app --reload
```

## 3. Маршруты

```python
@app.get("/")
@app.post("/")
@app.put("/")
@app.delete("/")
@app.patch("/")
@app.options("/")
@app.head("/")
```

### Параметры пути

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/posts/{year}/{slug}")
async def get_post(year: int, slug: str):
    return {"year": year, "slug": slug}

# предопределённые значения (enum)
from enum import Enum

class Genre(str, Enum):
    fiction = "fiction"
    non_fiction = "non-fiction"

@app.get("/books/{genre}")
async def get_books(genre: Genre):
    return {"genre": genre.value}
```

## 4. Параметры запроса

```python
@app.get("/search")
async def search(q: str, page: int = 1, limit: int = 10):
    return {"q": q, "page": page, "limit": limit}

# необязательные
@app.get("/items")
async def get_items(q: str | None = None, skip: int = 0):
    return {"q": q, "skip": skip}
```

### Валидация Query

```python
from fastapi import Query

@app.get("/items")
async def get_items(
    q: str = Query(None, min_length=3, max_length=50),
    page: int = Query(1, ge=1),
    sort: str = Query("name", pattern="^(name|price|date)$"),
):
    return {"q": q, "page": page}
```

## 5. Body (тело запроса)

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None
    tags: list[str] = []

@app.post("/items")
async def create_item(item: Item):
    return {"name": item.name, "price": item.price}

# вложенные модели
class User(BaseModel):
    name: str
    age: int

class Order(BaseModel):
    user: User
    items: list[Item]
    total: float

@app.post("/orders")
async def create_order(order: Order):
    return order
```

### Несколько body-параметров

```python
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(ge=1, le=10),
):
    return {"item_id": item_id, **item.dict()}
```

## 6. Формы и файлы

```python
from fastapi import Form, File, UploadFile

@app.post("/login")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}

# файл
@app.post("/upload")
async def upload(file: UploadFile = File()):
    content = await file.read()
    return {
        "filename": file.filename,
        "size": len(content),
        "content_type": file.content_type,
    }

# несколько файлов
@app.post("/upload-multiple")
async def upload_multiple(files: list[UploadFile] = File()):
    return [f.filename for f in files]
```

## 7. Response

```python
from fastapi.responses import (
    JSONResponse, HTMLResponse, PlainTextResponse,
    RedirectResponse, FileResponse, StreamingResponse,
)
from fastapi import status

# по умолчанию — JSON
return {"key": "value"}

# явно
return JSONResponse(content={"key": "value"}, status_code=201)

# HTML
return HTMLResponse("<h1>Привет</h1>")

# редирект
return RedirectResponse("/new-url")

# файл
return FileResponse("report.pdf")

# стриминг
from typing import AsyncIterator

async def generate():
    for i in range(10):
        yield f"chunk {i}\n"

return StreamingResponse(generate(), media_type="text/plain")

# статусы
from fastapi import status

@app.post("/", status_code=status.HTTP_201_CREATED)
async def create():
    return {"created": True}
```

### Response model

```python
class UserOut(BaseModel):
    id: int
    name: str
    email: str

class UserIn(BaseModel):
    name: str
    email: str
    password: str

@app.post("/users", response_model=UserOut)
async def create_user(user: UserIn):
    # password не попадёт в ответ
    return {"id": 1, **user.dict()}
```

## 8. Path и Query параметры — валидация

```python
from fastapi import Path, Query

@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(ge=1, le=1000, description="ID товара"),
    q: str | None = Query(None, max_length=10),
):
    return {"item_id": item_id}

# metadata
@app.get("/search")
async def search(
    q: str = Query(
        default=...,
        min_length=3,
        title="Поисковый запрос",
        description="Что ищем",
        alias="search-query",
        deprecated=False,
    ),
):
    return {"q": q}
```

## 9. Dependency Injection (DI)

```python
from fastapi import Depends, Header, HTTPException

# функция-зависимость
async def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Header(...)):
    if token != "secret":
        raise HTTPException(status_code=401)
    return {"id": 1, "name": "Анна"}

@app.get("/profile")
async def profile(
    user: dict = Depends(get_current_user),
    db = Depends(get_db),
):
    return user

# класс-зависимость
class Pagination:
    def __init__(self, skip: int = Query(0), limit: int = Query(10)):
        self.skip = skip
        self.limit = limit

@app.get("/items")
async def list_items(pagination: Pagination = Depends()):
    return {"skip": pagination.skip, "limit": pagination.limit}
```

## 10. Middleware

```python
import time

@app.middleware("http")
async def add_process_time(request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    response.headers["X-Process-Time"] = str(process_time)
    return response

# CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 11. Обработка ошибок

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id == 0:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "missing"},
        )
    return {"item_id": item_id}

# кастомные
class CustomException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

@app.exception_handler(CustomException)
async def custom_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )
```

## 12. WebSocket

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Эхо: {data}")

@app.websocket("/ws/{room}")
async def websocket_room(websocket: WebSocket, room: str):
    await websocket.accept()
    await websocket.send_text(f"Подключены к комнате {room}")
```

## 13. Фоновые задачи

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    print(f"Отправка {email}: {message}")

@app.post("/notify")
async def notify(email: str, tasks: BackgroundTasks):
    tasks.add_task(send_email, email, "Hello")
    return {"message": "Email будет отправлен"}
```

## 14. Роутеры (APIRouter)

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def list_users():
    return [{"id": 1, "name": "Анна"}]

@router.post("/")
async def create_user():
    return {"created": True}

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id}

# регистрация
app.include_router(router)
app.include_router(admin_router, prefix="/admin")
```

## 15. Lifecycle (startup/shutdown)

```python
@app.on_event("startup")
async def startup():
    print("Запуск приложения")
    app.state.db = await create_connection()

@app.on_event("shutdown")
async def shutdown():
    print("Остановка приложения")
    await app.state.db.close()

# или через lifespan (Python 3.12+)
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup")
    yield
    print("Shutdown")

app = FastAPI(lifespan=lifespan)
```

## 16. Документация

FastAPI автоматически генерирует OpenAPI-документацию.

```python
app = FastAPI(
    title="My API",
    description="Описание API",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI
    redoc_url="/redoc",      # ReDoc
    openapi_url="/openapi.json",
)
```

## 17. Тестирование

```bash
pip install pytest httpx
```

```python
from fastapi.testclient import TestClient

def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_create_item():
    client = TestClient(app)
    response = client.post("/items", json={"name": "Item", "price": 10.0})
    assert response.status_code == 200
```

## 18. FastAPI vs Flask vs Django

| | FastAPI | Flask | Django |
|---|---|---|---|
| Async | Встроен | Через дополнения | 3.1+ |
| OpenAPI | Автоматически | Вручную | DRF |
| Валидация | Pydantic | Вручную | DRF/forms |
| Скорость | Очень высокая | Средняя | Средняя |
| ORM | Любая | Любая | Свой ORM |
| Админка | Нет | Нет | Встроена |
| Размер проекта | Любой | Маленький/средний | Большой |
