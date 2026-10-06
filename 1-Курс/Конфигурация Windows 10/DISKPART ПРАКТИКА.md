# DISKPART: Управление дисками

## Введение
**DISKPART** — консольная утилита Windows для работы с дисками, разделами и томами.  
Позволяет гибко выполнять задачи и автоматизировать их скриптами.  
**Внимание:** ошибки приводят к потере данных.

## Практические шаги (на примере USB-флешки)

**Подготовка**
- Вставьте чистый USB (данные удалятся)
- Запустите CMD от имени администратора
- `diskpart`

**Шаг 1: Выбор диска**
```
list disk
select disk 2
clean
```

**Шаг 2: Структура (UEFI)**
```
convert gpt
create partition primary size=1000
```

**Шаг 3: Форматирование**
```
format fs=fat32 quick
assign letter=Z
active
```

**Шаг 4: Выход**
```
exit
```

## Цель практики
Освоить:
- очистку и конвертацию (GPT/MBR)
- создание и форматирование разделов
- назначение букв

## Сценарий тренировок (симуляция DISKPART)

**Диски в системе:**
- Диск 0: 120 ГБ (MBR, нераспределён)
- Диск 1: 500 ГБ (MBR, нераспределён)
- Диск 2: 60 ГБ (съёмный, активен)

**Задания:**
1. Очистить Диск 0 → `select disk 0` → `clean` → `convert mbr`
2. Создать основной раздел 50 ГБ → `create partition primary size=51200`
3. Форматировать NTFS «System» → `format fs=ntfs label="System" quick`
4. Присвоить C: → `assign letter=C`
5. Создать расширенный → `create partition extended`
6. Логический 30 ГБ → `create partition logical size=30720`
7. Форматировать FAT32 «Data» D: → `format fs=fat32 label="Data" quick` → `assign letter=D`
8. `list partition`
9. Диск 1 → GPT → `select disk 1` → `convert gpt`
10. Том 100 ГБ E: NTFS «Work» → `create partition primary size=102400` → `format fs=ntfs label="Work" quick` → `assign letter=E`
11. Сжать E на 20 ГБ → `shrink desired=20480`
12. Новый том F: NTFS «Backup» → `create partition primary size=...` → `format fs=ntfs label="Backup" quick` → `assign letter=F`
13. `detail volume` (на E)
14. Удалить F → `select volume F` → `delete volume`
15. Расширить E +20 ГБ → `select volume E` → `extend size=20480`
16. Диск 0 → GPT (после проверки)
17. Активировать раздел → `active`
18. `list disk` + `list volume`

## Итоги
Освоены команды: `list`, `select`, `clean`, `convert`, `create`, `format`, `assign`, `shrink`, `extend`, `delete`.

**Применение:**
- полная очистка накопителей
- подготовка загрузочных флешек
- исправление невидимых дисков