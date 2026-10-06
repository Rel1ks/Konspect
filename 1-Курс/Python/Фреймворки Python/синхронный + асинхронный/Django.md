# Django

**Django** — полноценный веб-фреймворк «всё включено». ORM, админка, аутентификация, формы, миграции.

## 1. Установка

```bash
pip install django
django-admin --version
```

## 2. Создание проекта

```bash
django-admin startproject mysite
cd mysite
python manage.py runserver
```

### Структура

```
mysite/
├── manage.py          # CLI-инструмент
├── mysite/
│   ├── __init__.py
│   ├── settings.py    # настройки проекта
│   ├── urls.py        # корневые URL
│   ├── asgi.py
│   └── wsgi.py
└── db.sqlite3
```

## 3. Приложения

```bash
python manage.py startapp blog
```

```
blog/
├── migrations/
│   └── __init__.py
├── __init__.py
├── admin.py       # настройка админки
├── apps.py        # конфигурация приложения
├── models.py      # модели БД
├── tests.py       # тесты
└── views.py       # логика (контроллеры)
```

### Регистрация приложения

```python
# mysite/settings.py
INSTALLED_APPS = [
    ...
    "blog",
]
```

## 4. Модели (ORM)

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
```

### Типы полей

```python
CharField, TextField, IntegerField, FloatField, BooleanField
DateField, DateTimeField, TimeField, DurationField
EmailField, URLField, SlugField, FileField, ImageField
ForeignKey, ManyToManyField, OneToOneField
DecimalField, JSONField, UUIDField
```

### Миграции

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py sqlmigrate blog 0001
python manage.py migrate blog 0001  # откат
```

## 5. Админка

```python
# blog/admin.py
from django.contrib import admin
from .models import Post, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "is_published", "created_at"]
    list_filter = ["is_published", "created_at", "tags"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["author"]

admin.site.register(Tag)
```

## 6. Views

### Function-based views (FBV)

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post

def post_list(request):
    posts = Post.objects.filter(is_published=True)
    return render(request, "blog/post_list.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, "blog/post_detail.html", {"post": post})

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", slug=post.slug)
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form})
```

### Class-based views (CBV)

```python
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

class PostDetailView(DetailView):
    model = Post
    slug_field = "slug"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

## 7. URLs

```python
# mysite/urls.py
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
]

# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
]
```

## 8. Шаблоны

```html
<!-- blog/templates/blog/base.html -->
<!DOCTYPE html>
<html>
<head><title>{% block title %}Блог{% endblock %}</title></head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

```html
<!-- blog/templates/blog/post_list.html -->
{% extends "base.html" %}

{% block content %}
<h1>Посты</h1>
{% for post in posts %}
    <article>
        <h2><a href="{% url 'post_detail' slug=post.slug %}">{{ post.title }}</a></h2>
        <p>{{ post.created_at|date:"d.m.Y" }}</p>
        <p>{{ post.content|truncatewords:30 }}</p>
    </article>
{% empty %}
    <p>Нет постов</p>
{% endfor %}

<div class="pagination">
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">←</a>
    {% endif %}
    <span>{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span>
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">→</a>
    {% endif %}
</div>
{% endblock %}
```

### Статические файлы

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/main.js' %}"></script>
<img src="{% static 'images/logo.png' %}">
```

## 9. Формы

```python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "slug", "content", "tags", "is_published"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 10}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 5:
            raise forms.ValidationError("Слишком короткий заголовок")
        return title
```

## 10. Аутентификация

```python
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# встроенные URL
# path("accounts/", include("django.contrib.auth.urls")),

# логин
def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user:
            login(request, user)
            return redirect("post_list")
    return render(request, "registration/login.html")

# защита
@login_required
def profile(request):
    return render(request, "profile.html")
```

## 11. REST API (Django REST Framework)

```bash
pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = ["rest_framework"]

# serializers.py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "slug", "content", "created_at", "author"]

# views.py
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("posts", PostViewSet)
urlpatterns += router.urls
```

## 12. Настройки

```python
# mysite/settings.py
DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# PostgreSQL
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "mydb",
#         "USER": "user",
#         "PASSWORD": "password",
#         "HOST": "localhost",
#         "PORT": 5432,
#     }
# }

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True
```

## 13. Middleware

```python
# settings.py
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

## 14. Django ORM — запросы

```python
# создание
Post.objects.create(title="Новый пост", ...)

# чтение
Post.objects.all()
Post.objects.filter(is_published=True)
Post.objects.exclude(is_published=True)
Post.objects.get(id=1)
Post.objects.get_or_create(title="...")

# цепочки
Post.objects.filter(author=user).exclude(tags__name="draft")

# связанные поля
Post.objects.select_related("author")  # ForeignKey
Post.objects.prefetch_related("tags")  # ManyToMany

# агрегация
from django.db.models import Count, Sum, Avg
Post.objects.aggregate(total=Count("id"))

# аннотация
authors = User.objects.annotate(post_count=Count("post"))
```

## 15. Django vs Flask vs FastAPI

| | Django | Flask | FastAPI |
|---|---|---|---|
| Размер | Полноценный | Микро | Микро |
| ORM | Свой | Любая | Любая |
| Админка | Встроена | Нет | Нет |
| REST API | DRF | Вручную | Встроен |
| Async | 3.1+ | Через дополнения | Нативный |
| Порог входа | Высокий | Низкий | Средний |
| Для чего | Большие проекты | Маленькие/средние | API, микросервисы |
