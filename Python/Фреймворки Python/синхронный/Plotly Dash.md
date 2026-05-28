# Plotly Dash

**Dash** — фреймворк для создания интерактивных веб-дашбордов на Python. Основан на Flask, React и Plotly.

## 1. Установка

```bash
pip install dash
pip install pandas  # для работы с данными
```

## 2. Минимальное приложение

```python
from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Hello Dash"),
    html.P("Мой первый дашборд"),
])

if __name__ == "__main__":
    app.run(debug=True)
```

## 3. Компоненты

### HTML-компоненты (`dash.html`)

```python
from dash import html

html.Div([
    html.H1("Заголовок"),
    html.H2("Подзаголовок"),
    html.P("Абзац текста"),
    html.Br(),
    html.Hr(),
    html.A("Ссылка", href="https://example.com"),
    html.Img(src="/assets/logo.png"),
    html.Button("Кнопка", id="btn"),
    html.Ul([
        html.Li("Элемент 1"),
        html.Li("Элемент 2"),
    ]),
    html.Div(style={"color": "red", "fontSize": 20}),
])
```

### Core-компоненты (`dash.dcc`)

```python
from dash import dcc

dcc.Dropdown(
    options=[
        {"label": "Москва", "value": "msk"},
        {"label": "СПб", "value": "spb"},
    ],
    value="msk",
    id="city-dropdown",
)

dcc.Slider(min=0, max=10, step=1, value=5, id="slider")
dcc.RangeSlider(min=0, max=10, step=0.5, value=[3, 7])

dcc.Input(type="text", placeholder="Введите имя", id="name-input")
dcc.Textarea(placeholder="Текст...", style={"width": "100%"})

dcc.Checklist(
    options=["A", "B", "C"],
    value=["A"],
    id="checklist",
)

dcc.RadioItems(
    options=["option1", "option2", "option3"],
    value="option1",
)

dcc.DatePickerSingle(date="2024-01-15", id="date-picker")
dcc.DatePickerRange(start_date="2024-01-01", end_date="2024-12-31")

dcc.Loading(id="loading", children=[html.Div(id="output")])
```

## 4. Callbacks — реактивность

```python
from dash import Dash, html, dcc, Input, Output, callback

app = Dash(__name__)

app.layout = html.Div([
    dcc.Input(id="input", type="text", value=""),
    html.Div(id="output"),
])

@callback(
    Output("output", "children"),
    Input("input", "value"),
)
def update_output(value):
    if not value:
        return "Введите текст"
    return f"Вы ввели: {value}"

if __name__ == "__main__":
    app.run(debug=True)
```

## 5. Несколько входов и выходов

```python
@callback(
    Output("output-text", "children"),
    Output("output-graph", "figure"),
    Input("dropdown", "value"),
    Input("slider", "value"),
)
def update(dropdown_value, slider_value):
    text = f"Выбрано: {dropdown_value}, слайдер: {slider_value}"
    fig = {
        "data": [{"x": [1, 2, 3], "y": [slider_value, 5, 3]}],
        "layout": {"title": f"График для {dropdown_value}"},
    }
    return text, fig
```

## 6. Графики Plotly

```python
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# через plotly.express
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

# через graph_objects
fig = go.Figure()
fig.add_trace(go.Scatter(x=[1,2,3], y=[4,5,6], mode="lines", name="Линия"))
fig.add_trace(go.Bar(x=["A","B","C"], y=[10,20,15], name="Столбцы"))
fig.update_layout(title="График", xaxis_title="X", yaxis_title="Y")

# в дашборде
app.layout = html.Div([
    dcc.Graph(figure=fig)
])
```

### Типы графиков

```python
px.scatter()       # точечный
px.line()          # линейный
px.bar()           # столбчатый
px.histogram()     # гистограмма
px.box()           # ящик с усами
px.pie()           # круговая
px.heatmap()       # тепловая карта
px.density_heatmap() # плотность
px.area()          # площадь
px.sunburst()      # солнечная диаграмма
px.treemap()       # дерево
px.choropleth()    # географическая карта
```

## 7. State — только чтение без триггера

```python
from dash import State

@callback(
    Output("result", "children"),
    Input("submit-btn", "n_clicks"),
    State("name-input", "value"),
    State("age-input", "value"),
    prevent_initial_call=True,
)
def on_click(n_clicks, name, age):
    if not name or not age:
        return "Заполните все поля"
    return f"{name}, {age} лет"
```

## 8. Dash DataTable

```python
from dash import dash_table

df = pd.DataFrame({
    "Город": ["Москва", "СПб", "Казань"],
    "Население": [12_000_000, 5_400_000, 1_300_000],
})

app.layout = html.Div([
    dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": c, "id": c} for c in df.columns],
        page_size=10,
        sort_action="native",
        filter_action="native",
        editable=True,
        row_selectable="single",
    )
])
```

## 9. Макет (layout)

```python
from dash import html

# строки и колонки (Bootstrap-like)
app.layout = html.Div([
    html.Div(className="row", children=[
        html.Div(className="six columns", children=[
            html.H3("Колонка 1"),
        ]),
        html.Div(className="six columns", children=[
            html.H3("Колонка 2"),
        ]),
    ]),
])
```

### Использование Dash Bootstrap

```bash
pip install dash-bootstrap-components
```

```python
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Дашборд"), width=12),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Фильтры"),
                dbc.CardBody([
                    dcc.Dropdown(id="dropdown"),
                ]),
            ]),
        ], width=4),
        dbc.Col([
            dcc.Graph(id="graph"),
        ], width=8),
    ]),
])
```

## 10. Callback контекст

```python
from dash import callback_context

@callback(
    Output("output", "children"),
    Input("btn-1", "n_clicks"),
    Input("btn-2", "n_clicks"),
)
def on_click(btn1, btn2):
    ctx = callback_context
    if not ctx.triggered:
        return "Нажмите кнопку"
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "btn-1":
        return "Нажата кнопка 1"
    return "Нажата кнопка 2"
```

## 11. Паттерн для больших приложений

```
app/
├── app.py
├── assets/
│   └── style.css
├── components/
│   ├── __init__.py
│   ├── header.py
│   └── filters.py
├── callbacks/
│   ├── __init__.py
│   ├── main_callbacks.py
│   └── graph_callbacks.py
└── data/
    └── data_loader.py
```

```python
# app.py
from dash import Dash

app = Dash(__name__)
app.layout = create_layout()

from callbacks import register_callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
```

## 12. Деплой

```bash
# Gunicorn (Linux)
gunicorn app:server

# Waitress (Windows)
pip install waitress
waitress-serve --port=8080 app:server
```

```python
# app.py — server нужен для деплоя
server = app.server
```
