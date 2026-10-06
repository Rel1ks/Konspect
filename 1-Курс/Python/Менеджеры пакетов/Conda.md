# Conda — менеджер пакетов и окружений

**Conda** — кроссплатформенный менеджер пакетов и окружений. Не ограничивается Python, работает с любыми языками (R, C++, Node.js и др.).

## 1. Установка

```bash
# Miniconda (минимальная)
# https://docs.anaconda.com/miniconda/

# Anaconda (полная — много предустановленных пакетов)
# https://www.anaconda.com/download

# проверка
conda --version
```

## 2. Управление окружениями

```bash
# создать окружение с Python 3.12
conda create -n my-env python=3.12

# создать с указанием пакетов
conda create -n my-env python=3.12 requests flask

# создать из файла
conda env create -f environment.yml

# активировать
conda activate my-env

# деактивировать
conda deactivate

# копировать окружение
conda create -n new-env --clone my-env

# удалить окружение
conda remove -n my-env --all

# список окружений
conda env list
conda info --envs
```

## 3. Управление пакетами

```bash
# установка
conda install requests
conda install "requests>=2.31.0"
conda install -n my-env requests  # в конкретное окружение

# установка из определённого канала
conda install -c conda-forge numpy

# удаление
conda remove requests

# обновление
conda update requests
conda update --all  # все пакеты
conda update conda  # сам conda

# список в текущем окружении
conda list
conda list -n my-env

# поиск пакета
conda search requests
conda search "requests>=2.31"

# информация о пакете
conda show requests
```

## 4. Каналы (channels)

```bash
# основные каналы:
#   defaults  — канал по умолчанию
#   conda-forge — сообщество (самый популярный)
#   bioconda — биоинформатика
#   pytorch — PyTorch

# установка с указанием канала
conda install -c conda-forge numpy

# приоритет каналов (.condarc)
conda config --add channels conda-forge
conda config --set channel_priority strict

# просмотр настроек
conda config --show channels
```

### .condarc

```yaml
# %USERPROFILE%\.condarc
channels:
  - conda-forge
  - defaults
channel_priority: strict
auto_activate_base: false
envs_dirs:
  - C:\Users\user\.conda\envs
pkgs_dirs:
  - C:\Users\user\.conda\pkgs
```

## 5. environment.yml

Файл для воспроизводимого окружения.

```yaml
name: my-project
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.12
  - requests>=2.31
  - numpy>=1.24
  - flask>=3.0
  - pip
  - pip:
    - private-package==1.0
    - -r requirements.txt
```

```bash
# создать окружение из файла
conda env create -f environment.yml

# обновить из файла
conda env update -f environment.yml

# экспорт текущего окружения
conda env export > environment.yml
conda env export --no-builds > environment.yml  # без номеров сборки
```

## 6. Conda vs pip

| Возможность | Conda | pip |
|---|---|---|
| Не только Python | Да (C, R, и т.д.) | Только Python |
| Зависимости | Разрешение конфликтов | Линейная установка |
| Бинарные пакеты | Да | Через wheel |
| Виртуальные окружения | Встроенные | Через venv |
| Версии Python | Управляет | Не управляет |
| Оффлайн-установка | Через tarball | Через wheel |
| Каналы | conda-forge, defaults и др. | PyPI |

## 7. Conda + pip

Conda и pip можно использовать вместе, но с осторожностью.

```bash
# установка pip в conda-окружение (уже есть)
conda activate my-env

# conda-пакеты
conda install numpy

# pip-пакеты (только то, чего нет в conda)
pip install private-package
```

```yaml
# environment.yml с pip
dependencies:
  - python=3.12
  - numpy
  - pip
  - pip:
    - package-not-in-conda
    - -r requirements.txt
```

## 8. Управление версиями Python

```bash
# создать окружение с конкретной версией
conda create -n py311 python=3.11
conda create -n py312 python=3.12

# обновить Python в окружении
conda install -n my-env python=3.12

# список доступных версий
conda search python
```

## 9. Conda в CI/CD

```yaml
# GitHub Actions
- name: Setup conda
  uses: conda-inc/setup-miniconda@v3
  with:
    python-version: "3.12"
    environment-file: environment.yml

- name: Run tests
  shell: bash -l {0}
  run: |
    conda activate my-project
    pytest
```

## 10. Полезные команды

```bash
# информация о conda
conda info

# очистка кеша
conda clean --all
conda clean --tarballs
conda clean --packages

# сравнение окружений
conda compare -n env1 -n env2

# переименовать окружение
conda rename -n old-name new-name

# список пакетов в кеше
conda list --explicit

# восстановить окружение из explicit-списка
conda create -n my-env --file packages.txt
```

## 11. Mamba — быстрая альтернатива Conda

**Mamba** — переписанный на C++ conda, значительно быстрее.

```bash
# установка через conda
conda install -c conda-forge mamba

# использование (те же команды, что и conda)
mamba create -n my-env python=3.12
mamba install numpy
mamba env create -f environment.yml
```

## 12. Conda vs uv vs Poetry

| Возможность | Conda | uv | Poetry |
|---|---|---|---|
| Скорость | Медленный | **Очень быстрый** | Средний |
| Не только Python | **Да** | Нет | Нет |
| Бинарные пакеты | **Да** | Нет | Нет |
| Версии Python | **Управляет** | Управляет | Через pyenv |
| Каналы | conda-forge и др. | PyPI | PyPI |
| Lock-файл | environment.yml | uv.lock | poetry.lock |
| Научные пакеты | Лучший выбор | Средне | Средне |
