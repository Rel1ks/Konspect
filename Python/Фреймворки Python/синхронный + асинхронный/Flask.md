# Flask

**Flask** — микро-фреймворк. Минимальный, гибкий, с огромным количеством расширений.

## 1. Установка

```bash
pip install flask
```

## 2. Минимальное приложение

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
```

## 3. Маршруты

```python
@app.route("/")
@app.route("/about")
@app.route("/contact")

# методы
@app.route("/users", methods=["GET", "POST"])
@app.get("/users")
@app.post("/users")
```

### Динамические сегменты

```python
@app.route("/users/<int:user_id>")
def get_user(user_id):
    return f"User {user_id}"

@app.route("/posts/<int:year>/<slug>")
def get_post(year, slug):
    return f"{year}: {slug}"

# конвертеры
# string (по умолч.), int, float, path (со слешами), uuid
@app.route("/files/<path:subpath>")
def show_file(subpath):
    return f"File: {subpath}"
```

## 4. Request

```python
from flask import request

@app.route("/search")
def search():
    name = request.args.get("name", "гость")
    page = request.args.get("page", 1, type=int)
    return f"Привет, {name}!"

@app.post("/data")
def data():
    # form
    username = request.form["username"]
    password = request.form.get("password")

    # JSON
    json_data = request.get_json()

    # заголовки
    user_agent = request.headers.get("User-Agent")

    # куки
    session = request.cookies.get("session")

    # URL
    path = request.path
    full_path = request.full_path
    url = request.url
    method = request.method

    return "OK"
```

## 5. Response

```python
from flask import make_response, jsonify, redirect, abort

# строка
return "Hello"

# кортеж
return "Not Found", 404
return "Created", 201, {"X-Custom": "value"}

# make_response
resp = make_response("Hello")
resp.status_code = 200
resp.headers["X-Custom"] = "value"
resp.set_cookie("key", "value", max_age=3600)
return resp

# JSON
return jsonify({"name": "Анна", "age": 25})

# редирект
return redirect("/new-url")
return redirect(url_for("index"))

# ошибка
abort(404)
abort(403, description="Доступ запрещён")
```

## 6. Шаблоны (Jinja2)

```python
from flask import render_template

@app.route("/profile/<name>")
def profile(name):
    return render_template("profile.html", name=name, age=25)
```

```html
<!-- templates/profile.html -->
<!DOCTYPE html>
<html>
<head><title>{{ name }}</title></head>
<body>
    <h1>Привет, {{ name }}!</h1>
    <p>Возраст: {{ age }}</p>

    {% if age >= 18 %}
        <p>Взрослый</p>
    {% else %}
        <p>Ребёнок</p>
    {% endif %}

    <ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
</body>
</html>
```

### Фильтры

```html
{{ text|upper }}
{{ text|lower }}
{{ text|capitalize }}
{{ text|truncate(50) }}
{{ date|formatdatetime }}
{{ number|round(2) }}
{{ list|length }}
{{ html|safe }}
```

### Статические файлы

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<script src="{{ url_for('static', filename='app.js') }}"></script>
<img src="{{ url_for('static', filename='logo.png') }}">
```

## 7. URL building

```python
from flask import url_for

with app.test_request_context():
    print(url_for("index"))           # /
    print(url_for("get_user", user_id=42))  # /users/42
    print(url_for("static", filename="style.css"))  # /static/style.css
```

## 8. Session и Flash

```python
from flask import session, flash

app.secret_key = "secret-key-123"

@app.route("/login")
def login():
    session["user_id"] = 1
    session["username"] = "anna"
    flash("Вы вошли в систему", "success")
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.clear()
    return redirect(url_for("index"))

@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Необходимо войти", "error")
        return redirect(url_for("login"))
    return f"Профиль {session['username']}"
```

## 9. Blueprints

```python
from flask import Blueprint

# blog/__init__.py
blog = Blueprint("blog", __name__, url_prefix="/blog",
                 template_folder="templates", static_folder="static")

@blog.route("/")
def list_posts():
    return "Список постов"

@blog.route("/<int:post_id>")
def post_detail(post_id):
    return f"Пост {post_id}"

# app.py
from blog import blog
app.register_blueprint(blog)
app.register_blueprint(admin, url_prefix="/admin")
```

## 10. Обработка ошибок

```python
from flask import render_template

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500

# кастомный
class APIError(Exception):
    def __init__(self, message, status=400):
        self.message = message
        self.status = status

@app.errorhandler(APIError)
def handle_api_error(error):
    return {"error": error.message}, error.status
```

## 11. Middleware (before/after request)

```python
@app.before_request
def before_request():
    print(f"Запрос: {request.method} {request.path}")

@app.after_request
def after_request(response):
    response.headers["X-Server"] = "Flask"
    return response

@app.teardown_request
def teardown(error):
    db.close()
```

## 12. Расширения

```bash
pip install flask-sqlalchemy    # ORM
pip install flask-migrate       # миграции
pip install flask-login         # аутентификация
pip install flask-wtf           # формы
pip install flask-mail          # email
pip install flask-restful       # REST API
pip install flask-cors          # CORS
pip install flask-admin         # админка
pip install flask-socketio      # WebSocket
```

### Flask-SQLAlchemy

```python
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))

    def __repr__(self):
        return f"<User {self.username}>"

with app.app_context():
    db.create_all()
```

### Flask-Login

```python
from flask_login import LoginManager, login_user, login_required, current_user

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    user = User.query.filter_by(username=request.form["username"]).first()
    if user and check_password(user.password, request.form["password"]):
        login_user(user)
        return redirect(url_for("profile"))
    return "Ошибка входа"

@app.route("/profile")
@login_required
def profile():
    return f"Привет, {current_user.username}!"
```

### Flask-Migrate

```python
from flask_migrate import Migrate

migrate = Migrate(app, db)
```

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 13. Конфигурация

```python
app = Flask(__name__)

# напрямую
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

# из объекта
class Config:
    SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"

app.config.from_object(Config)

# из файла
app.config.from_pyfile("config.py")

# из переменных окружения
app.config.from_prefixed_env("FLASK_")

# FLASK_SECRET_KEY → app.config["SECRET_KEY"]
```

## 14. CLI

```python
import click
from flask.cli import with_appcontext

@app.cli.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()
    click.echo("База данных создана")
```

```bash
flask init-db
flask routes  # список маршрутов
flask shell   # интерактивная оболочка
```

## 15. Тестирование

```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200

def test_json(client):
    response = client.post("/data", json={"key": "value"})
    assert response.json["status"] == "ok"
```

## 16. Flask vs Django vs FastAPI

| | Flask | Django | FastAPI |
|---|---|---|---|
| Размер | Микро | Полноценный | Микро |
| ORM | Через расширения | Свой | Через расширения |
| Админка | flask-admin | Встроена | Нет |
| Async | Через дополнения | 3.1+ | Нативный |
| OpenAPI | flasgger | DRF | Автоматически |
| Простота | Очень высокая | Средняя | Высокая |
