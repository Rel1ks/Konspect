# WinGet (Windows Package Manager)

**WinGet** — это официальный менеджер пакетов для Windows 10 и Windows 11, разработанный Microsoft. Предназначен для установки, обновления, удаления и управления приложениями через командную строку.

---

## Содержание

- [[#Что такое WinGet|Что такое WinGet]]
- [[#Требования к системе|Требования к системе]]
- [[#Установка WinGet|Установка WinGet]]
- [[#Основные команды|Основные команды]]
- [[#Поиск пакетов|Поиск пакетов]]
- [[#Установка приложений|Установка приложений]]
- [[#Обновление приложений|Обновление приложений]]
- [[#Удаление приложений|Удаление приложений]]
- [[#Экспорт и импорт конфигурации|Экспорт и импорт конфигурации]]
- [[#Источники пакетов|Источники пакетов]]
- [[#Настройки WinGet|Настройки WinGet]]
- [[#Манифесты пакетов|Манифесты пакетов]]
- [[#Практические примеры|Практические примеры]]
- [[#Устранение неполадок|Устранение неполадок]]

---

## Что такое WinGet

WinGet — это инструмент командной строки, который позволяет:

- **Искать** приложения по названию, издателю или тегам
- **Устанавливать** приложения из централизованного репозитория
- **Обновлять** установленные приложения до последних версий
- **Удалять** приложения
- **Экспортировать** список установленных приложений
- **Импортировать** конфигурацию для массового развёртывания
- **Валидировать** и создавать манифесты пакетов

WinGet использует репозиторий **winget-pkgs** на GitHub, где хранятся манифесты всех поддерживаемых приложений.

> [!INFO]
> WinGet является частью **App Installer** в Windows 10/11 и может быть обновлён через Microsoft Store.

---

## Требования к системе

| Компонент | Минимальные требования |
|-----------|------------------------|
| **ОС** | Windows 10 версии 1709 и новее, Windows 11 |
| **App Installer** | Версия 1.4.21091.0 или новее |
| **PowerShell** | Версия 5.1 или новее (рекомендуется) |
| **.NET** | .NET Framework 4.7.2 или новее |

> [!TIP]
> Для полноценной работы рекомендуется Windows 10 версии 2004 или новее.

---

## Установка WinGet

### Проверка наличия

WinGet предустановлен в большинстве современных версий Windows 10/11. Проверьте наличие:

```powershell
winget --version
```

### Установка через Microsoft Store

1. Откройте **Microsoft Store**
2. Найдите **App Installer**
3. Установите или обновите приложение

### Ручная установка

1. Перейдите на страницу релизов: [GitHub App Installer](https://github.com/microsoft/winget-cli/releases)
2. Скачайте файл `.msixbundle`
3. Установите командой:

```powershell
Add-AppxPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle
```

### Установка в Windows Server

Для Windows Server требуется дополнительная настройка:

```powershell
# Включить службу App Installer
Install-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe
```

---

## Основные команды

### Общая структура

```powershell
winget <команда> [параметры] [аргументы]
```

### Сводная таблица команд

| Команда | Описание |
|---------|----------|
| `winget search` | Поиск приложений |
| `winget install` | Установка приложения |
| `winget upgrade` | Обновление приложения |
| `winget uninstall` | Удаление приложения |
| `winget list` | Список установленных приложений |
| `winget show` | Показать информацию о пакете |
| `winget export` | Экспорт списка приложений |
| `winget import` | Импорт конфигурации |
| `winget source` | Управление источниками |
| `winget validate` | Проверка манифеста |
| `winget settings` | Настройки WinGet |
| `winget --version` | Версия WinGet |

### Глобальные параметры

| Параметр | Описание |
|----------|----------|
| `--help`, `-h` | Показать справку |
| `--version`, `-v` | Показать версию |
| `--info` | Показать информацию о системе |
| `--disable-interactivity` | Отключить интерактивные запросы |
| `--accept-source-agreements` | Автоматически принимать соглашения |
| `--accept-package-agreements` | Автоматически принимать лицензионные соглашения |

---

## Поиск пакетов

### Базовый поиск

```powershell
# Поиск по названию
winget search firefox

# Поиск по издателю
winget search --publisher Mozilla

# Точный поиск по названию
winget search --exact firefox
```

### Расширенный поиск

```powershell
# Поиск по тегам
winget search --tag browser

# Поиск с фильтрацией по ID
winget search --id Mozilla

# Поиск только по источнику winget
winget search firefox --source winget
```

### Параметры команды search

| Параметр | Описание |
|----------|----------|
| `<query>` | Поисковый запрос |
| `--id` | Фильтр по ID пакета |
| `--name` | Фильтр по имени |
| `--publisher` | Фильтр по издателю |
| `--tag` | Фильтр по тегам |
| `--exact` | Точное совпадение |
| `--source` | Источник для поиска |
| `--count` | Показать количество результатов |

> [!NOTE]
> По умолчанию WinGet показывает первые 10 результатов. Используйте `--count` для отображения количества всех найденных пакетов.

---

## Установка приложений

### Базовая установка

```powershell
# Установка по ID
winget install Mozilla.Firefox

# Установка по имени
winget install "Firefox"

# Установка с подтверждением соглашений
winget install Mozilla.Firefox --accept-package-agreements
```

### Установка определённой версии

```powershell
# Установка конкретной версии
winget install Mozilla.Firefox --version 115.0.1

# Установка конкретной архитектуры
winget install Mozilla.Firefox --architecture x64
```

### Интерактивная и автоматическая установка

```powershell
# Автоматическая установка без запросов
winget install Mozilla.Firefox --silent

# Принудительная установка
winget install Mozilla.Firefox --force

# Установка без перезапуска
winget install Mozilla.Firefox --disable-interactivity
```

### Параметры команды install

| Параметр | Описание |
|----------|----------|
| `<id>` или `<name>` | ID или имя пакета |
| `--version` | Конкретная версия |
| `--source` | Источник пакета |
| `--architecture` | Архитектура (x86, x64, arm64) |
| `--installer-type` | Тип установщика (msi, exe, msix) |
| `--silent` | Тихая установка |
| `--interactive` | Интерактивная установка |
| `--force` | Принудительная установка |
| `--accept-package-agreements` | Принять лицензионное соглашение |
| `--accept-source-agreements` | Принять соглашение источника |
| `--location` | Путь установки |
| `--log` | Путь к файлу лога |
| `--override` | Передача параметров установщику |
| `--constraint` | Установка по ограничениям (например, по версии) |

> [!WARNING]
> Некоторые приложения требуют интерактивной установки даже с флагом `--silent`.

---

## Обновление приложений

### Проверка доступных обновлений

```powershell
# Показать все доступные обновления
winget upgrade

# Проверить обновление конкретного приложения
winget upgrade Mozilla.Firefox
```

### Выполнение обновления

```powershell
# Обновить все приложения
winget upgrade --all

# Обновить конкретное приложение
winget upgrade Mozilla.Firefox

# Тихое обновление
winget upgrade --all --silent

# Обновление с исключением
winget upgrade --all --exclude Mozilla.Firefox
```

### Параметры команды upgrade

| Параметр | Описание |
|----------|----------|
| `--all` | Обновить все приложения |
| `<id>` | Обновить конкретное приложение |
| `--source` | Источник для обновления |
| `--silent` | Тихий режим |
| `--interactive` | Интерактивный режим |
| `--force` | Принудительное обновление |
| `--exclude` | Исключить приложение из обновления |
| `--accept-package-agreements` | Принять соглашения |
| `--accept-source-agreements` | Принять соглашения источника |

> [!TIP]
> Рекомендуется регулярно выполнять `winget upgrade --all` для поддержания актуальности приложений.

---

## Удаление приложений

### Базовое удаление

```powershell
# Удаление по ID
winget uninstall Mozilla.Firefox

# Удаление по имени
winget uninstall "Firefox"
```

### Параметры команды uninstall

| Параметр | Описание |
|----------|----------|
| `<id>` или `<name>` | ID или имя пакета |
| `--source` | Источник пакета |
| `--purge` | Полное удаление (если поддерживается) |
| `--accept-source-agreements` | Принять соглашения источника |

> [!CAUTION]
> WinGet не удаляет пользовательские данные приложений, если это не поддерживается установщиком.

---

## Экспорт и импорт конфигурации

### Экспорт списка приложений

```powershell
# Экспорт в JSON
winget export -o installed-apps.json

# Экспорт в YAML
winget export -o installed-apps.yaml

# Экспорт с указанием источника
winget export -o apps.json --include-versions
```

### Импорт конфигурации

```powershell
# Импорт из файла
winget import -i installed-apps.json

# Импорт с автоматическим принятием соглашений
winget import -i installed-apps.yaml --accept-package-agreements --accept-source-agreements

# Импорт в тихом режиме
winget import -i apps.json --silent
```

### Формат файла экспорта (JSON)

```json
{
  "$schema": "https://aka.ms/winget-manifest.installschema.1.0.0.json",
  "Packages": [
    {
      "PackageIdentifier": "Mozilla.Firefox",
      "Version": "115.0.1",
      "Channel": "stable"
    },
    {
      "PackageIdentifier": "Google.Chrome",
      "Version": "116.0.5845.96"
    }
  ]
}
```

> [!TIP]
> Используйте экспорт/импорт для быстрого развёртывания стандартного набора приложений на новых компьютерах.

---

## Источники пакетов

WinGet поддерживает несколько источников пакетов:

| Источник | Описание |
|----------|----------|
| `winget` | Официальный репозиторий Microsoft (по умолчанию) |
| `msstore` | Microsoft Store |
| Пользовательские | Сторонние репозитории |

### Управление источниками

```powershell
# Показать все источники
winget source list

# Добавить источник
winget source add <name> <url>

# Обновить источники
winget source update

# Обновить конкретный источник
winget source update winget

# Удалить источник
winget source remove <name>

# Восстановить источники по умолчанию
winget source reset --force
```

### Параметры команды source

| Параметр | Описание |
|----------|----------|
| `list` | Показать источники |
| `add` | Добавить источник |
| `update` | Обновить источник |
| `remove` | Удалить источник |
| `reset` | Сброс к настройкам по умолчанию |
| `--name` | Имя источника |
| `--argument` | URL или путь к источнику |
| `--type` | Тип источника (Microsoft.Rest, Microsoft.PreIndexed) |

> [!NOTE]
> По умолчанию WinGet использует прединдексированный источник для ускорения поиска.

---

## Настройки WinGet

### Просмотр настроек

```powershell
# Показать текущие настройки
winget settings

# Открыть файл настроек
winget settings --open
```

### Файл настроек

Настройки хранятся в:
```
%LOCALAPPDATA%\Packages\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe\LocalState\settings.json
```

### Пример файла settings.json

```json
{
  "$schema": "https://aka.ms/winget-settings.schema.json",
  "visual": {
    "progressBar": "accent",
    "useAnsiColor": true
  },
  "experimentalFeatures": {
    "experimentalCmd": true,
    "directMSI": true,
    "dependencies": true
  },
  "installBehavior": {
    "preferences": {
      "architecture": ["x64", "x86"],
      "scope": ["machine"]
    }
  },
  "source": {
    "autoUpdateIntervalInMinutes": 60
  }
}
```

### Параметры настроек

| Раздел | Параметр | Описание |
|--------|----------|----------|
| `visual` | `progressBar` | Стиль прогресс-бара (accent, rainbow, retro) |
| `visual` | `useAnsiColor` | Использовать ANSI-цвета |
| `experimentalFeatures` | `experimentalCmd` | Экспериментальные команды |
| `experimentalFeatures` | `directMSI` | Прямая установка MSI |
| `experimentalFeatures` | `dependencies` | Автоматическая установка зависимостей |
| `installBehavior.preferences` | `architecture` | Предпочтительная архитектура |
| `installBehavior.preferences` | `scope` | Область установки (user/machine) |
| `source` | `autoUpdateIntervalInMinutes` | Интервал автообновления источников |

> [!TIP]
> Для применения изменений после редактирования settings.json перезапустите терминал.

---

## Манифесты пакетов

### Структура манифеста

Манифесты хранятся в репозитории [winget-pkgs](https://github.com/microsoft/winget-pkgs) и определяют метаданные пакета.

### Версии схемы манифеста

| Версия | Формат |
|--------|--------|
| 1.0.0 | Один файл YAML |
| 1.1.0 | Разделённые файлы (singleton, installer, locale) |
| 1.2.0+ | Дополнительные возможности |

### Пример манифеста (версия 1.0.0)

```yaml
PackageIdentifier: Mozilla.Firefox
PackageVersion: 115.0.1
PackageLocale: ru-RU
Publisher: Mozilla
PackageName: Mozilla Firefox
License: MPL 2.0
ShortDescription: Быстрый и безопасный веб-браузер
Description: |
  Mozilla Firefox — это свободный браузер с открытым исходным кодом.
  Обеспечивает быстрый и безопасный веб-сёрфинг.
Tags:
  - browser
  - web
  - mozilla
Homepage: https://www.mozilla.org/firefox/
Installers:
  - Architecture: x64
    InstallerType: exe
    InstallerUrl: https://download.mozilla.org/firefox-115.0.1-win64.exe
    InstallerSha256: ABC123...
    InstallerSwitches:
      Silent: /S
      SilentWithProgress: /S
  - Architecture: x86
    InstallerType: exe
    InstallerUrl: https://download.mozilla.org/firefox-115.0.1-win32.exe
    InstallerSha256: DEF456...
```

### Создание и валидация манифеста

```powershell
# Создать новый манифест
winget create -n

# Валидировать манифест
winget validate --manifest <путь_к_манифесту>

# Отправить манифест в репозиторий
winget submit --manifest <путь_к_манифесту>
```

### Параметры команды validate

| Параметр | Описание |
|----------|----------|
| `--manifest` | Путь к файлу манифеста |
| `--verbose` | Подробный вывод |

> [!NOTE]
> Для отправки пакетов в winget-pkgs требуется учётная запись GitHub и соблюдение правил репозитория.

---

## Практические примеры

### Сценарий 1: Первоначальная настройка нового ПК

```powershell
# Обновить источники
winget source update

# Установить базовый набор приложений
winget install Mozilla.Firefox Google.Chrome 7zip.7zip VideoLAN.VLC --silent --accept-package-agreements

# Обновить все приложения
winget upgrade --all --silent
```

### Сценарий 2: Массовое развёртывание

```powershell
# На эталонном ПК: экспортировать конфигурацию
winget export -o company-standard.json

# На новых ПК: импортировать и установить
winget import -i company-standard.json --silent --accept-package-agreements --accept-source-agreements
```

### Сценарий 3: Поиск и установка по критериям

```powershell
# Найти все браузеры
winget search --tag browser

# Установить конкретную версию
winget install Mozilla.Firefox --version 115.0.1 --architecture x64

# Установить в определённую папку
winget install Git.Git --location "C:\Tools\Git"
```

### Сценарий 4: Автоматизация через PowerShell

```powershell
# Скрипт для установки набора приложений
$apps = @(
    "Mozilla.Firefox",
    "Google.Chrome",
    "7zip.7zip",
    "VideoLAN.VLC",
    "Notepad++.Notepad++"
)

foreach ($app in $apps) {
    Write-Host "Установка $app..."
    winget install $app --silent --accept-package-agreements
}

Write-Host "Готово!"
```

### Сценарий 5: Проверка установленных версий

```powershell
# Показать все установленные приложения
winget list

# Экспортировать в CSV для анализа
winget export -o installed.json
# Затем обработать в PowerShell:
# Get-Content installed.json | ConvertFrom-Json | Select-Object -ExpandProperty Packages
```

### Сценарий 6: Обновление с исключением критичных приложений

```powershell
# Обновить всё, кроме конкретных приложений
winget upgrade --all --exclude Oracle.JavaRuntimeEnvironment Adobe.Acrobat.Reader.64-bit
```

---

## Устранение неполадок

### WinGet не найден

**Проблема:** Команда `winget` не распознаётся.

**Решение:**
```powershell
# Проверить наличие App Installer
Get-AppxPackage Microsoft.DesktopAppInstaller

# Переустановить из Microsoft Store
# Или установить вручную с GitHub Releases
```

### Ошибка 0x80070005 (Отказано в доступе)

**Проблема:** Недостаточно прав для установки.

**Решение:**
```powershell
# Запустить терминал от имени администратора
# Или установить для текущего пользователя
winget install <app> --scope user
```

### Ошибка хэша установщика

**Проблема:** Хэш установщика не совпадает.

**Решение:**
```powershell
# Обновить источники
winget source update

# Принудительная установка (не рекомендуется)
winget install <app> --force
```

### Приложение не обновляется

**Проблема:** WinGet не видит доступное обновление.

**Решение:**
```powershell
# Обновить источники
winget source update

# Проверить конкретное приложение
winget show <app>

# Удалить и установить заново
winget uninstall <app>
winget install <app>
```

### Медленный поиск или установка

**Проблема:** Долгая обработка команд.

**Решение:**
```powershell
# Сбросить источники
winget source reset --force

# Обновить источники
winget source update
```

### Ошибки при импорте

**Проблема:** Не удаётся импортировать конфигурацию.

**Решение:**
```powershell
# Проверить формат файла
# Убедиться в корректности JSON/YAML
# Использовать --accept-package-agreements --accept-source-agreements
winget import -i file.json --accept-package-agreements --accept-source-agreements
```

---

**Теги:** #windows #winget #package-manager #администрирование #автоматизация
