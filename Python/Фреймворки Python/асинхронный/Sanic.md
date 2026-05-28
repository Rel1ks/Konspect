# Sanic

**Sanic** — асинхронный веб-фреймворк, похожий на Flask, но полностью async. Поддерживает HTTP/2, WebSocket, middleware.

## 1. Установка

```bash
pip install sanic
```

## 2. Минимальное приложение

```python
from sanic import Sanic
from sanic.response import text

app = Sanic("MyApp")

@app.route("/")
async def hello(request):
    return text("Hello, World!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

## 3. Маршруты

```python
@app.get("/users")
@app.post("/users")
@app.put("/users/<id>")
@app.delete("/users/<id>")
@app.patch("/users/<id>")

# динамические с типом
@app.get("/users/<user_id:int>")
@app.get("/posts/<year:int>/<slug:str>")

# regex
@app.get("/api/<version:[A-Za-z0-9.]+>")
```

## 4. Request

```python
@app.post("/data")
async def handler(request):
    method = request.method
    path = request.path
    url = request.url

    name = request.args.get("name")
    names = request.args.getlist("name")
    form_data = request.form.get("field")
    json_data = request.json
    body = request.body

    user_agent = request.headers.get("User-Agent")
    token = request.token
    session = request.cookies.get("session")
    ip = request.ip
```

## 5. Response

```python
from sanic.response import text, html, json, file, redirect, raw, empty

return text("Hello", status=201)
return html("<h1>Привет</h1>")
return json({"name": "Анна"})
return file("/path/to/file.pdf")
return redirect("/new-url")
return raw(b"binary")
return empty(status=204)
```

## 6. Blueprints

```python
from sanic import Blueprint

users = Blueprint("users", url_prefix="/users")

@users.get("/")
async def list_users(request):
    return json([{"id": 1, "name": "Анна"}])

app.blueprint(users)
```

## 7. Middleware

```python
@app.middleware("request")
async def log_request(request):
    print(f"{request.method} {request.path}")

@app.middleware("response")
async def add_headers(request, response):
    response.headers["X-Server"] = "Sanic"
```

## 8. WebSocket

```python
@app.websocket("/ws")
async def feed(request, ws):
    while True:
        data = await ws.recv()
        if data is None:
            break
        await ws.send(f"Эхо: {data}")
```

## 9. Статика и конфиг

```python
app.static("/static", "./static")
app.config.DB_HOST = "localhost"
app.config.RESPONSE_TIMEOUT = 60
```

## 10. Sanic vs Flask vs FastAPI

| | Sanic | Flask | FastAPI |
|---|---|---|---|
| Async | Нативный | Через дополнения | Нативный |
| OpenAPI | Через sanic-ext | Через flasgger | Встроен |
| Скорость | Очень высокая | Средняя | Высокая |
| WebSocket | Встроен | Нет | Через Starlette |
| Blueprints | Да | Да | APIRouter |
| Популярность | Средняя | Высокая | Высокая |
