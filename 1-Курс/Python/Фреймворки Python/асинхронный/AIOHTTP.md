# AIOHTTP

**aiohttp** — асинхронный HTTP-клиент и сервер на asyncio.

## 1. Установка

```bash
pip install aiohttp
```

## 2. Клиент

### Простой GET-запрос

```python
import aiohttp
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    html = await fetch("https://example.com")
    print(len(html))

asyncio.run(main())
```

### HTTP-методы

```python
async with session.get(url, params=params, headers=headers)
async with session.post(url, data=data, json=json_data)
async with session.put(url, data=data)
async with session.patch(url, data=data)
async with session.delete(url)
async with session.head(url)
async with session.options(url)
```

### Параметры запроса

```python
async with session.get("https://api.example.com/search", params={
    "q": "python",
    "page": 1,
    "limit": 10,
}) as response:
    data = await response.json()
```

### Заголовки

```python
headers = {
    "User-Agent": "MyApp/1.0",
    "Authorization": "Bearer token123",
}

async with session.get(url, headers=headers) as response:
    ...
```

### POST JSON

```python
data = {"name": "Анна", "age": 25}

async with session.post("https://api.example.com/users", json=data) as response:
    result = await response.json()
```

### POST form-data

```python
async with session.post("https://api.example.com/login", data={
    "username": "admin",
    "password": "secret",
}) as response:
    ...

# файл
async with session.post("https://api.example.com/upload", data={
    "file": open("photo.jpg", "rb"),
}) as response:
    ...
```

### Параметры ClientSession

```python
async with aiohttp.ClientSession(
    base_url="https://api.example.com",  # базовый URL
    headers={"Authorization": "Bearer token"},
    timeout=aiohttp.ClientTimeout(total=30),
    cookies={"session": "abc123"},
) as session:
    async with session.get("/users") as resp:
        ...
    async with session.get("/posts") as resp:
        ...
```

## 3. Обработка ответа

```python
async with session.get(url) as response:
    # статус
    print(response.status)
    print(response.ok)  # True если 200-399

    # заголовки
    print(response.headers)
    print(response.headers.get("Content-Type"))

    # тело
    text = await response.text()          # str
    json = await response.json()          # dict/list
    bytes = await response.read()         # bytes

    # чанками
    async for chunk in response.content.iter_chunks():
        print(len(chunk))
```

## 4. Несколько запросов

```python
async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch(session, url))
        return await asyncio.gather(*tasks)

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

urls = [f"https://api.example.com/page/{i}" for i in range(100)]
results = asyncio.run(fetch_all(urls))
```

### Semaphore (ограничение конкурентности)

```python
async def fetch_all(urls, limit=10):
    sem = asyncio.Semaphore(limit)

    async def bounded_fetch(url):
        async with sem:
            async with session.get(url) as response:
                return await response.text()

    async with aiohttp.ClientSession() as session:
        tasks = [bounded_fetch(url) for url in urls]
        return await asyncio.gather(*tasks)
```

## 5. Таймауты

```python
from aiohttp import ClientTimeout, ClientSession

# глобальный таймаут
timeout = ClientTimeout(total=30, connect=10, sock_read=20)

async with ClientSession(timeout=timeout) as session:
    ...

# на конкретный запрос
async with session.get(url, timeout=ClientTimeout(total=5)) as resp:
    ...
```

## 6. Сериализация ошибок

```python
import aiohttp
import async_timeout

async def fetch_with_retry(url, retries=3):
    for i in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    return await response.json()
        except aiohttp.ClientError as e:
            print(f"Попытка {i+1}: {e}")
            await asyncio.sleep(1)
    raise Exception(f"Не удалось загрузить {url}")
```

## 7. Сервер

### Минимальный сервер

```python
from aiohttp import web

async def hello(request):
    return web.Response(text="Hello, World!")

app = web.Application()
app.router.add_get("/", hello)

if __name__ == "__main__":
    web.run_app(app, port=8080)
```

### Маршруты

```python
async def home(request):
    return web.Response(text="Главная")

async def about(request):
    return web.Response(text="О нас")

async def user(request):
    user_id = request.match_info["id"]
    return web.Response(text=f"Пользователь {user_id}")

async def post(request):
    year = request.match_info["year"]
    slug = request.match_info["slug"]
    return web.Response(text=f"Пост {year}/{slug}")

app.router.add_get("/", home)
app.router.add_get("/about", about)
app.router.add_get("/users/{id}", user)
app.router.add_get("/posts/{year}/{slug}", post)
app.router.add_post("/api/data", handler)
```

### Request

```python
async def handler(request):
    # метод
    method = request.method

    # URL
    path = request.path
    query = request.query  # GET параметры
    q = request.query.get("q")

    # заголовки
    agent = request.headers.get("User-Agent")

    # тело
    data = await request.post()      # form-data
    json = await request.json()      # JSON
    text = await request.text()      # str
    body = await request.read()      # bytes

    # match_info
    user_id = request.match_info.get("id")

    # куки
    session = request.cookies.get("session")
```

### Response

```python
from aiohttp import web
import json

# текст
return web.Response(text="Привет")
return web.Response(body=b"bytes")

# JSON
return web.json_response({"name": "Анна", "age": 25})

# статус и заголовки
return web.Response(
    text="Создано",
    status=201,
    headers={"X-Custom": "value"},
)

# файл
return web.FileResponse(path="photo.jpg")

# поток
resp = web.StreamResponse()
resp.headers["Content-Type"] = "text/plain"
await resp.prepare(request)
await resp.write(b"chunk1")
await resp.write(b"chunk2")
await resp.write_eof()
```

### Статические файлы

```python
app.router.add_static("/static", path="./static", name="static")
```

### Middleware

```python
@web.middleware
async def logger(request, handler):
    print(f"Запрос: {request.method} {request.path}")
    try:
        response = await handler(request)
        print(f"Ответ: {response.status}")
        return response
    except Exception as e:
        print(f"Ошибка: {e}")
        raise

app = web.Application(middlewares=[logger])
```

### CORS

```python
from aiohttp import web

@web.middleware
async def cors_middleware(request, handler):
    response = await handler(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

app = web.Application(middlewares=[cors_middleware])
```

### WebSocket

```python
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            await ws.send_str(f"Эхо: {msg.data}")
        elif msg.type == aiohttp.WSMsgType.CLOSED:
            break

    return ws

app.router.add_get("/ws", websocket_handler)
```

## 8. Тестирование

```bash
pip install pytest-aiohttp
```

```python
import pytest
from aiohttp import web

async def handler(request):
    return web.json_response({"ok": True})

@pytest.fixture
def app():
    app = web.Application()
    app.router.add_get("/test", handler)
    return app

@pytest.mark.asyncio
async def test_handler(aiohttp_client):
    client = await aiohttp_client(app)
    resp = await client.get("/test")
    assert resp.status == 200
    data = await resp.json()
    assert data["ok"] is True
```

## 9. aiohttp vs requests

| | requests | aiohttp |
|---|---|---|
| Синхронный | Да | Нет |
| Асинхронный | Нет | Да |
| Конкурентность | ThreadPoolExecutor | asyncio |
| Сервер | Нет | Встроен |
| WebSocket | Нет | Да |
| Простота | Очень простой | Средняя |
