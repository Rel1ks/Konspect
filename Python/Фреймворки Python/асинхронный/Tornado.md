# Tornado

**Tornado** — асинхронный веб-фреймворк и библиотека для работы с сетью. Разработан в FriendFeed (позже Facebook).

## 1. Установка

```bash
pip install tornado
```

## 2. Минимальное приложение

```python
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, World!")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
```

## 3. RequestHandler

### HTTP-методы

```python
class ItemHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.write(f"GET item {id}")

    def post(self, id):
        self.write(f"POST item {id}")

    def put(self, id):
        self.write(f"PUT item {id}")

    def delete(self, id):
        self.write(f"DELETE item {id}")

    def patch(self, id):
        self.write(f"PATCH item {id}")
```

### Request

```python
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument("name", "гость")
        names = self.get_query_arguments("name")

        # POST
        email = self.get_body_argument("email")

        # заголовки
        agent = self.request.headers.get("User-Agent")

        # путь
        path = self.request.path
        uri = self.request.uri

        # куки
        session = self.get_cookie("session")

        # JSON
        import json
        data = json.loads(self.request.body)
```

### Response

```python
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Текст")
        self.write({"key": "value"})

        self.set_status(201)
        self.set_status(404, reason="Не найдено")

        self.set_header("Content-Type", "application/json")
        self.set_cookie("session", "abc123")
        self.clear_cookie("old_cookie")

        self.redirect("/new-url")

        self.finish()
```

## 4. Маршруты

```python
app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/about", AboutHandler),
    (r"/users/([0-9]+)", UserHandler),            # группа
    (r"/posts/(?P<year>[0-9]{4})", PostHandler),   # именованная
])

# именованные
app = tornado.web.Application([
    tornado.web.URLSpec(r"/", MainHandler, name="home"),
    tornado.web.URLSpec(r"/users/(\d+)", UserHandler, name="user"),
])
# self.reverse_url("home")
```

## 5. Шаблоны

```python
app = tornado.web.Application([
    (r"/", MainHandler),
], template_path="templates")
```

```html
{% extends "base.html" %}
{% block title %}Главная{% end %}
{% block content %}
<h1>{{ title }}</h1>
<ul>
    {% for user in users %}
    <li>{{ user }}</li>
    {% end %}
</ul>
{% end %}
```

```python
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html", title="Главная", users=["Анна", "Борис"])
```

## 6. Асинхронные хендлеры

```python
import asyncio

class AsyncHandler(tornado.web.RequestHandler):
    async def get(self):
        result = await self.fetch_data()
        self.write(result)

    async def fetch_data(self):
        await asyncio.sleep(1)
        return {"data": "result"}
```

## 7. Асинхронный HTTP-клиент

```python
from tornado.httpclient import AsyncHTTPClient

async def fetch_url(url):
    client = AsyncHTTPClient()
    response = await client.fetch(url)
    return response.body

async def main():
    urls = ["https://example.com", "https://httpbin.org/get"]
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
```

## 8. WebSocket

```python
import tornado.websocket

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        self.clients.add(self)

    def on_message(self, message):
        for client in self.clients:
            client.write_message(f"Эхо: {message}")

    def on_close(self):
        self.clients.remove(self)

    def check_origin(self, origin):
        return True

app = tornado.web.Application([
    (r"/ws", WebSocketHandler),
])
```

## 9. Запуск

```python
# простой
app.listen(8888)
tornado.ioloop.IOLoop.current().start()

# несколько процессов
server = tornado.httpserver.HTTPServer(app)
server.bind(8888)
server.start(4)
tornado.ioloop.IOLoop.current().start()
```

## 10. Настройки

```python
app = tornado.web.Application([
    (r"/", MainHandler),
],
    debug=True,
    cookie_secret="secret-key",
    autoreload=True,
    xsrf_cookies=True,
    compress_response=True,
    static_path="static",
    template_path="templates",
)
```

## 11. Tornado vs FastAPI vs aiohttp

| | Tornado | FastAPI | aiohttp |
|---|---|---|---|
| Возраст | Старый (2009) | Новый (2018) | Средний |
| OpenAPI | Нет | Встроен | Нет |
| WebSocket | Встроен | Через Starlette | Встроен |
| Производительность | Высокая | Высокая | Высокая |
| Шаблоны | Свои | Jinja2 | Нет |
| Популярность | Снижается | Растёт | Стабильная |
