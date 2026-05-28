# Pyramid

**Pyramid** — минималистичный веб-фреймворк. Растёт от простого к сложному: от одного файла до крупного приложения.

## 1. Установка

```bash
pip install pyramid
```

## 2. Минимальное приложение

```python
from pyramid.config import Configurator
from pyramid.response import Response
from wsgiref.simple_server import make_server

def hello(request):
    return Response("Hello, World!")

if __name__ == "__main__":
    config = Configurator()
    config.add_route("hello", "/")
    config.add_view(hello, route_name="hello")
    app = config.make_wsgi_app()
    server = make_server("0.0.0.0", 6543, app)
    server.serve_forever()
```

## 3. Маршруты (routes)

```python
# простой маршрут
config.add_route("home", "/")
config.add_route("about", "/about")
config.add_route("contact", "/contact")

# динамические сегменты
config.add_route("user", "/users/{id}")
config.add_route("post", "/posts/{year}/{slug}")

# с регулярным выражением
config.add_route("api", "/api/{version:\\d+}.{format:\\w+}")
```

### Просмотры (views)

```python
# функция
def home(request):
    return Response("Главная")

# с параметрами
def user_detail(request):
    user_id = request.matchdict["id"]
    return Response(f"Пользователь {user_id}")

# несколько методов
from pyramid.view import view_config

@view_config(route_name="api", request_method="GET")
def api_get(request):
    return Response("GET")

@view_config(route_name="api", request_method="POST")
def api_post(request):
    return Response("POST")
```

## 4. Request и Response

### Request

```python
def view(request):
    # метод
    method = request.method  # GET, POST и т.д.

    # URL
    path = request.path
    url = request.url
    params = request.params  # GET + POST

    # GET-параметры
    q = request.GET.get("q")
    page = request.GET.get("page", 1)

    # POST-данные
    name = request.POST.get("name")

    # JSON
    import json
    data = request.json_body

    # заголовки
    user_agent = request.headers.get("User-Agent")

    # куки
    session_id = request.cookies.get("session")

    # тело запроса
    body = request.body  # bytes
    text = request.text  # str
```

### Response

```python
from pyramid.response import Response

# простой
def view(request):
    return Response("Привет!")

# с заголовками
def view(request):
    return Response(
        "JSON",
        status=200,
        headers={
            "Content-Type": "application/json",
            "X-Custom": "value",
        },
    )

# JSON
from pyramid.response import Response
import json

def view(request):
    data = {"name": "Анна", "age": 25}
    return Response(
        json.dumps(data, ensure_ascii=False),
        content_type="application/json",
    )
```

## 5. Шаблоны (Chameleon, Jinja2)

### Chameleon (по умолчанию)

```bash
pip install pyramid_chameleon
```

```python
config.include("pyramid_chameleon")
config.add_route("home", "/")

@view_config(route_name="home", renderer="templates/home.pt")
def home(request):
    return {"title": "Главная", "users": ["Анна", "Борис"]}
```

```html
<!-- templates/home.pt -->
<!DOCTYPE html>
<html>
<head><title tal:content="title">Заголовок</title></head>
<body>
    <h1>${title}</h1>
    <ul>
        <li tal:repeat="user users">${user}</li>
    </ul>
</body>
</html>
```

### Jinja2

```bash
pip install pyramid_jinja2
```

```python
config.include("pyramid_jinja2")
config.add_jinja2_search_path("templates")

@view_config(route_name="home", renderer="home.jinja2")
def home(request):
    return {"title": "Главная", "users": ["Анна", "Борис"]}
```

```html
<!-- templates/home.jinja2 -->
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <ul>
        {% for user in users %}
        <li>{{ user }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

## 6. Статические файлы

```python
# myapp/static/
config.add_static_view("static", "myapp:static", cache_max_age=3600)

# в шаблоне:
# <link rel="stylesheet" href="/static/style.css">
```

## 7. Сессии

```python
from pyramid.session import SignedCookieSessionFactory

my_session_factory = SignedCookieSessionFactory("secret-key")
config = Configurator(session_factory=my_session_factory)

def view(request):
    # чтение
    user_id = request.session.get("user_id")

    # запись
    request.session["user_id"] = 42

    # удаление
    del request.session["user_id"]

    # очистка
    request.session.clear()
```

## 8. Аутентификация и авторизация

```python
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

authn_policy = AuthTktAuthenticationPolicy("secret")
authz_policy = ACLAuthorizationPolicy()

config = Configurator(
    authentication_policy=authn_policy,
    authorization_policy=authz_policy,
)

# вьюха с проверкой
@view_config(route_name="profile", permission="view")
def profile(request):
    return Response(f"Профиль пользователя {request.authenticated_userid}")

# логин
def login(request):
    headers = remember(request, "username")
    return HTTPFound(location="/", headers=headers)

# логаут
def logout(request):
    headers = forget(request)
    return HTTPFound(location="/", headers=headers)
```

## 9. SQLAlchemy + Pyramid

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# настройка
engine = create_engine("sqlite:///db.sqlite")
Session = sessionmaker(bind=engine)

# в запросе
def view(request):
    session = Session()
    try:
        users = session.query(User).all()
        return {"users": users}
    finally:
        session.close()
```

### Пакет pyramid_retry + pyramid_tm (транзакции)

```bash
pip install pyramid_tm
```

```python
config.include("pyramid_tm")

# автоматический коммит/откат транзакций SQLAlchemy
```

## 10. Структура проекта (скэффолд)

```bash
pip install pyramid-cookiecutter-starter
cookiecutter gh:Pylons/pyramid-cookiecutter-starter
```

```
myproject/
├── setup.py
├── development.ini
├── production.ini
├── myproject/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   └── default.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── templates/
│   │   └── mytemplate.pt
│   └── static/
│       ├── css/
│       └── js/
└── tests/
    └── __init__.py
```

```python
# myproject/__init__.py
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("pyramid_chameleon")
    config.add_static_view("static", "static", cache_max_age=3600)
    config.add_route("home", "/")
    config.scan()
    return config.make_wsgi_app()
```

## 11. Запуск

```bash
# разработка
python app.py

# или через pserve
pip install pyramid[waitress]
pserve development.ini --reload
```

```ini
# development.ini
[app:main]
use = egg:myproject
pyramid.reload_templates = true
pyramid.debug_authorization = true

[server:main]
use = egg:waitress#main
host = 0.0.0.0
port = 6543
```

## 12. Pyramid vs Flask vs Django

| | Pyramid | Flask | Django |
|---|---|---|---|
| Размер | Минимальный | Микро | Полноценный |
| ORM | Любая | Любая | Свой |
| Админка | Нет | Нет | Встроена |
| Гибкость | Высокая | Высокая | Средняя |
| Порог входа | Средний | Низкий | Средний |
| Подходит для | Любого размера | Маленькие/средние | Большие |
