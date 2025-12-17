import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
BACKGROUND_COLOR = (30, 35, 45)
TEXT_COLOR = (200, 210, 225)      # Цвет для ненабранных символов целевого текста
KEY_COLOR = (60, 70, 85)
KEY_PRESSED_COLOR = (150, 170, 200)
ACCENT_COLOR = (70, 150, 255)     # Цвет для правильно набранных символов
TEXT_DISPLAY_COLOR = (230, 240, 255) # Цвет для текущего (следующего) символа
ERROR_COLOR = (255, 100, 100)     # Цвет для ошибочно набранных символов

BASE_WIDTH = 1200
BASE_HEIGHT = 800
MIN_WIDTH = 600
MIN_HEIGHT = 400


class TypingApp:
    def __init__(self):
        # ИНИЦИАЛИЗАЦИЯ RANDOM ГЕНЕРАТОРА ДЛЯ НЕПРЕДСКАЗУЕМЫХ ЧИСЕЛ ПРИ КАЖДОМ ЗАПУСКЕ
        random.seed()

        self.display = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Typing Practice App")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_width = BASE_WIDTH
        self.current_height = BASE_HEIGHT

        # Шрифты
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 20)

        # БАЗОВЫЙ СЛОВАРЬ СЛОВ ДЛЯ ГЕНЕРАЦИИ ПРЕДЛОЖЕНИЙ (английский)
        self.word_pool_english = [
            "the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog",
            "python", "is", "a", "powerful", "programming", "language",
            "problem", "nation", "small", "however", "in", "with", "new", "very", "not", "one",
            "in", "the", "age", "of", "information", "typing", "speed", "matters",
            "learning", "to", "type", "fast", "improves", "productivity",
            "code", "algorithm", "function", "variable", "data", "structure",
            "window", "manager", "linux", "system", "configuration", "shell",
            "application", "interface", "design", "responsive", "layout",
            "network", "connectivity", "service", "status", "check",
            "graphics", "card", "monitor", "refresh", "rate", "performance",
            "processor", "motherboard", "memory", "storage", "optimization",
            "command", "line", "tool", "script", "automation", "task"
        ]
        
        # СЛОВАРЬ СЛОВ ДЛЯ ГЕНЕРАЦИИ ПРЕДЛОЖЕНИЙ (русский)
        self.word_pool_russian = [
            "быстрый", "коричневый", "лиса", "прыгает", "через", "ленивый", "собака",
            "питон", "это", "мощный", "язык", "программирования",
            "проблема", "нация", "маленький", "однако", "в", "с", "новый", "очень", "не", "один",
            "в", "эпоху", "информации", "скорость", "печати", "важна",
            "обучение", "печатать", "быстро", "улучшает", "продуктивность",
            "код", "алгоритм", "функция", "переменная", "данные", "структура",
            "окно", "менеджер", "линукс", "система", "конфигурация", "оболочка",
            "приложение", "интерфейс", "дизайн", "адаптивный", "макет",
            "сеть", "подключение", "сервис", "статус", "проверка",
            "графика", "карта", "монитор", "обновление", "частота", "производительность",
            "процессор", "материнская", "плата", "память", "хранилище", "оптимизация",
            "команда", "строка", "инструмент", "скрипт", "автоматизация", "задача"
        ]
        
        # СИМВОЛЫ ДЛЯ РЕЖИМА "SYMBOLS"
        self.symbols_pool = [
            "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+",
            "[", "]", "{", "}", "|", "\\", ";", ":", "'", '"', ",", ".", "<", ">", "?", "/",
            "~", "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
        ]

        # Текущий сгенерированный текст (будет установлен в next_text)
        self.current_text = ""

        self.show_result_screen = False  # Флаг для показа экрана результатов
        self.result_stats = {}          # Словарь для хранения статистики по окончании теста

        self.typed_text = ""  # Будет содержать только символы, которые пользователь уже набрал
        self.start_time = None
        self.wpm = 0
        self.accuracy = 100

        # Настройки теста
        self.language = "english"
        self.test_type = "time"  # или "words", "quotes", "symbols"
        self.time_limit = 30     # секунды (по умолчанию 30s)
        self.punctuation_enabled = True  # Включена ли пунктуация

        # Виртуальная клавиатура (буквы + пунктуация)
        self.keyboard_layout = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
            [',', '.', '!', '?', ':', ';', '-', "'", '"']
        ]

        self.keys_rect = {}
        self.pressed_keys = set()

        # --- ДОБАВЛЕНО РАНЬШЕ ---
        self.cursor_blink_time = 0
        self.cursor_visible = True
        # --- КОНЕЦ ДОБАВЛЕНИЯ ---

        # Кнопки меню
        self.settings_buttons = []
        self.update_layout()
        self._create_settings_buttons()
        
        # Генерируем начальный текст
        self.next_text()

    def _create_settings_buttons(self):
        """Создаёт кнопки меню."""
        # Позиционируем меню сразу под текстом
        text_y = int(self.current_height * 0.15)
        line_height = int(self.font_medium.get_height() * 1.2)
        # Меню размещаем через примерно 2 строки текста + отступ
        menu_y = text_y + line_height * 2 + 20
        menu_x_start = int(self.current_width * 0.1)
        button_padding = 8
        button_margin = 6

        current_x = menu_x_start

        # Кнопка обновления
        refresh_icon = self.font_small.render("↻", True, TEXT_COLOR)
        refresh_rect = refresh_icon.get_rect(topleft=(current_x, menu_y))
        self.settings_buttons.append({
            'rect': refresh_icon.get_rect(topleft=(current_x, menu_y)).inflate(10, 5),
            'text': "↻",
            'action': 'refresh',
            'color': KEY_COLOR,
            'text_color': TEXT_COLOR
        })
        current_x += refresh_rect.width + button_padding + button_margin

        # Язык (со звездочкой для английского)
        language_text = f"*{self.language}" if self.language == "english" else self.language
        language_label = self.font_small.render(language_text, True, TEXT_DISPLAY_COLOR if self.language == "english" else TEXT_COLOR)
        language_rect = language_label.get_rect(topleft=(current_x, menu_y))
        self.settings_buttons.append({
            'rect': language_rect.inflate(10, 5),
            'text': language_text,
            'action': 'language',
            'color': ACCENT_COLOR if self.language == "english" else KEY_COLOR,
            'text_color': TEXT_DISPLAY_COLOR if self.language == "english" else TEXT_COLOR
        })
        current_x += language_rect.width + button_padding + button_margin

        # Тип теста
        test_types = ["words", "time", "quotes", "symbols"]
        for tt in test_types:
            label = self.font_small.render(tt, True, TEXT_DISPLAY_COLOR if self.test_type == tt else TEXT_COLOR)
            rect = label.get_rect(topleft=(current_x, menu_y))
            self.settings_buttons.append({
                'rect': rect.inflate(10, 5),
                'text': tt,
                'action': 'test_type',
                'value': tt,
                'color': ACCENT_COLOR if self.test_type == tt else KEY_COLOR,
                'text_color': TEXT_DISPLAY_COLOR if self.test_type == tt else TEXT_COLOR
            })
            current_x += rect.width + button_padding + button_margin

        # Время теста
        time_options = [("15s", 15), ("30s", 30), ("1m", 60), ("2m", 120)]
        for to, val in time_options:
            label = self.font_small.render(to, True, TEXT_DISPLAY_COLOR if self.time_limit == val else TEXT_COLOR)
            rect = label.get_rect(topleft=(current_x, menu_y))
            self.settings_buttons.append({
                'rect': rect.inflate(10, 5),
                'text': to,
                'action': 'time_limit',
                'value': val,
                'color': ACCENT_COLOR if self.time_limit == val else KEY_COLOR,
                'text_color': TEXT_DISPLAY_COLOR if self.time_limit == val else TEXT_COLOR
            })
            current_x += rect.width + button_padding + button_margin

        # Кнопка настроек (иконка)
        settings_icon = self.font_small.render("∞", True, TEXT_COLOR)
        settings_rect = settings_icon.get_rect(topleft=(current_x, menu_y))
        self.settings_buttons.append({
            'rect': settings_rect.inflate(10, 5),
            'text': "∞",
            'action': 'settings',
            'color': KEY_COLOR,
            'text_color': TEXT_COLOR
        })
        current_x += settings_rect.width + button_padding + button_margin

        # Пунктуация
        punct_label = self.font_small.render("punctuation", True, TEXT_DISPLAY_COLOR if self.punctuation_enabled else TEXT_COLOR)
        punct_rect = punct_label.get_rect(topleft=(current_x, menu_y))
        self.settings_buttons.append({
            'rect': punct_rect.inflate(10, 5),
            'text': "punctuation",
            'action': 'punctuation',
            'color': ACCENT_COLOR if self.punctuation_enabled else KEY_COLOR,
            'text_color': TEXT_DISPLAY_COLOR if self.punctuation_enabled else TEXT_COLOR
        })

    def generate_random_sentence(self, min_words=5, max_words=12):
        """Генерирует случайное предложение из слов в зависимости от языка."""
        num_words = random.randint(min_words, max_words)
        if self.language == "english":
            sentence_words = [random.choice(self.word_pool_english) for _ in range(num_words)]
        else:  # russian
            sentence_words = [random.choice(self.word_pool_russian) for _ in range(num_words)]
        sentence = " ".join(sentence_words).capitalize()
        return sentence
    
    def generate_symbols_text(self, length=50):
        """Генерирует текст из символов для режима symbols."""
        symbols = [random.choice(self.symbols_pool) for _ in range(length)]
        return " ".join(symbols)

    def update_layout(self):
        self.current_width = max(self.display.get_width(), MIN_WIDTH)
        self.current_height = max(self.display.get_height(), MIN_HEIGHT)

        self.scale = min(self.current_width / BASE_WIDTH, self.current_height / BASE_HEIGHT)

        self.font_large = pygame.font.Font(None, max(int(60 * self.scale), 24))
        self.font_medium = pygame.font.Font(None, max(int(48 * self.scale), 16))
        self.font_small = pygame.font.Font(None, max(int(32 * self.scale), 12))

        self._generate_keyboard_layout()

    def _generate_keyboard_layout(self):
        self.keys_rect = {}

        # МЕНЬШАЯ и ФИКСИРОВАННАЯ клавиатура по ширине
        keyboard_width = 600
        key_width = keyboard_width // 11
        key_height = int(key_width * 0.9)
        key_margin = int(key_width * 0.08)

        # РАСЧЁТ РАЗМЕРОВ КЛАВИАТУРЫ
        # Высота клавиатуры зависит от количества рядов и размеров клавиш
        num_rows = len(self.keyboard_layout)
        total_keyboard_height = num_rows * key_height + (num_rows - 1) * (key_margin * 2)

        # ФИКСИРОВАННЫЙ ОТСТУП ОТ НИЖНЕГО КРАЯ ЭКРАНА
        bottom_margin = 100 # Пикселей от нижнего края экрана до низа клавиатуры

        # РАСЧЁТ X и Y для центрирования по горизонтали и фиксации по вертикали
        keyboard_left = (self.current_width - keyboard_width) // 2
        
        # keyboard_top теперь зависит от текущей высоты экрана
        keyboard_top = self.current_height - total_keyboard_height - bottom_margin

        # Рассчитываем Y-координаты для каждого ряда, начиная с keyboard_top
        row_positions = []
        for i in range(num_rows):
             row_positions.append(keyboard_top + i * (key_height + key_margin * 2))


        for row_idx, row in enumerate(self.keyboard_layout):
            row_width = len(row) * (key_width + key_margin)
            row_left = keyboard_left + (keyboard_width - row_width) // 2

            for col_idx, key in enumerate(row):
                x = row_left + col_idx * (key_width + key_margin)
                y = row_positions[row_idx] # <-- ИСПОЛЬЗУЕМ ВЫЧИСЛЕННУЮ Y-КООРДИНАТУ
                self.keys_rect[key] = pygame.Rect(x, y, key_width, key_height)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.VIDEORESIZE:
            self.update_layout()
            self.settings_buttons.clear()
            self._create_settings_buttons()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # ЛКМ
            mouse_pos = event.pos
            # Проверяем, была ли нажата кнопка меню
            for button in self.settings_buttons:
                if button['rect'].collidepoint(mouse_pos):
                    if button['action'] == 'refresh':
                        self.next_text()
                    elif button['action'] == 'language':
                        self.language = "english" if self.language != "english" else "russian"
                        self.settings_buttons.clear()
                        self._create_settings_buttons()
                        self.next_text()  # Генерируем новый текст на выбранном языке
                    elif button['action'] == 'test_type':
                        self.test_type = button['value']
                        self.settings_buttons.clear()
                        self._create_settings_buttons()
                        self.next_text()
                    elif button['action'] == 'time_limit':
                        self.time_limit = button['value']
                        self.settings_buttons.clear()
                        self._create_settings_buttons()
                        self.next_text()
                    elif button['action'] == 'settings':
                        # Пока что просто обновляем кнопки для обновления состояния
                        self.settings_buttons.clear()
                        self._create_settings_buttons()
                    elif button['action'] == 'punctuation':
                        self.punctuation_enabled = not self.punctuation_enabled
                        self.settings_buttons.clear()
                        self._create_settings_buttons()
                        self.next_text()
                    break

        elif event.type == pygame.KEYDOWN:
            # Если мы на экране результатов, то Enter начинает новый текст
            if self.show_result_screen and event.key == pygame.K_RETURN:
                self.next_text()
                return  # Прерываем дальнейшую обработку

            # ПЕРЕМЕЩАЕМ ПРОВЕРКУ ENTER СЮДА, ВЫШЕ ОСНОВНОЙ ЛОГИКИ ВВОДА
            if event.key == pygame.K_RETURN:
                # Проверяем, если мы закончили набор текста
                if len(self.typed_text) >= len(self.current_text):
                    self._save_results()  # Сохраняем статистику
                    self.show_result_screen = True  # Показываем экран результатов
                else:
                    # Иначе просто переходим к следующему тексту (если не закончили)
                    self.next_text()
            # ПРОВЕРЯЕМ НАЖАТИЕ BACKSPACE ТОЖЕ РАНЬШЕ
            elif event.key == pygame.K_BACKSPACE:
                self.typed_text = self.typed_text[:-1]

            # --- ОСНОВНАЯ ЛОГИКА ВВОДА СИМВОЛОВ ---
            # Проверяем, что пользователь может ввести новый символ
            # (т.е. он ещё не закончил предложение)
            current_pos = len(self.typed_text)

            # ВАЖНО: ПРОДОЛЖАЕМ ОБРАБОТКУ СИМВОЛОВ ТОЛЬКО ЕСЛИ ПРЕДЛОЖЕНИЕ НЕ ЗАКОНЧЕНО
            if current_pos < len(self.current_text):
                key_char = event.unicode  # сохраняем реальный регистр и символ

                if key_char == ' ':
                    # Проверяем, что следующий символ в целевом тексте действительно пробел
                    if self.current_text[current_pos] == ' ':
                        self.typed_text += ' '
                        if self.start_time is None:
                            self.start_time = pygame.time.get_ticks()
                    else:
                        # Если пользователь попытался ввести пробел, а там должен быть другой символ, считаем это ошибкой
                        self.typed_text += ' '  # Можно добавить пробел, но он будет помечен как ошибка
                        if self.start_time is None:
                            self.start_time = pygame.time.get_ticks()

                elif key_char and len(key_char) > 0:
                    # Поддержка всех символов: буквы (включая русские), цифры, пунктуация, символы
                    # Проверяем, что символ допустим для текущего режима
                    is_valid = False
                    
                    if self.test_type == "symbols":
                        # В режиме symbols принимаем все символы из symbols_pool и пробелы
                        is_valid = key_char in self.symbols_pool or key_char == ' '
                    else:
                        # В обычных режимах принимаем буквы (включая русские), цифры, пунктуацию
                        is_valid = (
                            key_char.isalpha() or  # Английские и русские буквы
                            key_char.isdigit() or  # Цифры
                            (key_char in " .,!?:;-'\"" and self.punctuation_enabled) or  # Пунктуация
                            (key_char in " .,!?:;-'\"" and self.test_type == "quotes")  # Пунктуация в цитатах
                        )
                    
                    if is_valid:
                        self.typed_text += key_char
                        if self.start_time is None:
                            self.start_time = pygame.time.get_ticks()

                        # Подсветка клавиш на виртуальной клавиатуре
                        highlight_key = key_char.upper() if key_char.isalpha() and key_char.isascii() else key_char
                        if highlight_key in self.keys_rect:
                            self.pressed_keys.add(highlight_key)

        elif event.type == pygame.KEYUP:
            key_char = event.unicode
            highlight_key = key_char.upper() if key_char.isalpha() else key_char
            if highlight_key in self.pressed_keys:
                self.pressed_keys.discard(highlight_key)

    def next_text(self):
        # Генерируем новое случайное предложение в зависимости от настроек
        if self.test_type == "words":
            num_words = random.randint(10, 20)  # Пример: 10-20 слов
            if self.language == "english":
                sentence_words = [random.choice(self.word_pool_english) for _ in range(num_words)]
            else:  # russian
                sentence_words = [random.choice(self.word_pool_russian) for _ in range(num_words)]
            self.current_text = " ".join(sentence_words).capitalize()
        elif self.test_type == "time":
            # Для временного теста генерируем длинное предложение
            num_words = random.randint(50, 100)
            if self.language == "english":
                sentence_words = [random.choice(self.word_pool_english) for _ in range(num_words)]
            else:  # russian
                sentence_words = [random.choice(self.word_pool_russian) for _ in range(num_words)]
            self.current_text = " ".join(sentence_words).capitalize()
        elif self.test_type == "quotes":
            # Цитаты в зависимости от языка
            if self.language == "english":
                quotes = [
                    "The only way to do great work is to love what you do.",
                    "Life is what happens when you're busy making other plans.",
                    "The future belongs to those who believe in the beauty of their dreams.",
                    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
                    "The only impossible journey is the one you never begin."
                ]
            else:  # russian
                quotes = [
                    "Единственный способ делать великую работу — это любить то, что ты делаешь.",
                    "Жизнь — это то, что происходит, пока ты строишь другие планы.",
                    "Будущее принадлежит тем, кто верит в красоту своих мечтаний.",
                    "Успех — это не финал, неудача — не фатальна: важно мужество продолжать.",
                    "Единственное невозможное путешествие — это то, которое ты никогда не начинаешь."
                ]
            self.current_text = random.choice(quotes)
        elif self.test_type == "symbols":
            # Режим с символами
            # Для временного теста больше символов
            if self.time_limit >= 60:
                self.current_text = self.generate_symbols_text(random.randint(150, 250))
            else:
                self.current_text = self.generate_symbols_text(random.randint(80, 150))

        self.typed_text = ""
        self.start_time = None
        self.pressed_keys.clear()
        self.show_result_screen = False  # Сбрасываем экран результатов при начале нового текста

    def calculate_stats(self):
        if self.start_time is None:
            return 0, 100

        elapsed_seconds = (pygame.time.get_ticks() - self.start_time) / 1000

        # Если тип теста "time", то проверяем, не истекло ли время
        if self.test_type == "time" and elapsed_seconds >= self.time_limit:
            # Автоматически завершаем тест
            self._save_results()
            self.show_result_screen = True
            return 0, 100  # Возвращаем 0, чтобы не обновлять статистику во время отрисовки

        if elapsed_seconds < 1:
            return 0, 100

        words_typed = len(self.typed_text.split())
        wpm = (words_typed / elapsed_seconds) * 60

        current_text = self.current_text
        correct_chars = sum(
            1 for i in range(min(len(self.typed_text), len(current_text)))
            if self.typed_text[i] == current_text[i]
        )

        total_chars = max(len(self.typed_text), 1)
        accuracy = int((correct_chars / total_chars) * 100)

        return int(wpm), min(accuracy, 100)

    def draw(self):
        if self.show_result_screen:
            self._draw_result_screen()
        else:
            self.display.fill(BACKGROUND_COLOR)

            # Заголовок
            title_text = self.font_large.render("Typing Practice", True, ACCENT_COLOR)
            title_rect = title_text.get_rect(center=(self.current_width // 2, int(self.current_height * 0.05)))
            self.display.blit(title_text, title_rect)

            # Целевой текст (текущее сгенерированное предложение)
            target_text = self.current_text
            text_y = int(self.current_height * 0.15)
            self._draw_text_target(target_text, text_y)

            # Меню настроек (под текстом)
            self._draw_settings_menu()

            # Статистика (только если не на экране результатов)
            self.wpm, self.accuracy = self.calculate_stats()
            stats_y = int(self.current_height * 0.48)
            self._draw_stats(stats_y)

            # Клавиатура
            self._draw_keyboard()

            # Инструкция
            instruction_y = int(self.current_height * 0.92)
            instruction_text = self.font_small.render(
                "ENTER - next text | BACKSPACE - delete char",
                True,
                TEXT_COLOR
            )
            instruction_rect = instruction_text.get_rect(center=(self.current_width // 2, instruction_y))
            self.display.blit(instruction_text, instruction_rect)

        # Мигание курсора (только если не на экране результатов)
        if not self.show_result_screen:
            current_time = pygame.time.get_ticks()
            if current_time - self.cursor_blink_time > 500:  # Мигание каждые 500 мс
                self.cursor_blink_time = current_time
                self.cursor_visible = not self.cursor_visible

        pygame.display.flip()

    def _draw_text_target(self, target_text: str, y: int):
        x_start = int(self.current_width * 0.1)
        line_length = self.current_width - int(self.current_width * 0.2)

        current_x = x_start
        current_y = y
        line_height = int(self.font_medium.get_height() * 1.2)

        typed_len = len(self.typed_text)

        for i, char in enumerate(target_text):
            if char == ' ':
                space_width = self.font_medium.size(' ')[0]
                current_x += space_width
                if current_x > x_start + line_length:
                    current_x = x_start
                    current_y += line_height
            else:
                # Определяем цвет символа
                if i < typed_len:
                    if self.typed_text[i] == char:
                        color = ACCENT_COLOR  # Правильно набран
                    else:
                        color = ERROR_COLOR   # Ошибка
                elif i == typed_len:
                    color = TEXT_DISPLAY_COLOR  # Текущий (следующий) символ
                else:
                    color = TEXT_COLOR        # Ещё не набран

                char_surface = self.font_medium.render(char, True, color)
                char_width = char_surface.get_width()

                # ПРОВЕРКА НА ТЕКУЩИЙ СИМВОЛ ДЛЯ РИСОВАНИЯ ПОЛОСЫ ПЕЧАТИ
                if i == typed_len:
                    # Рисуем вертикальную полосу печати слева от текущего символа
                    # Высота полосы = высоте шрифта, ширина = 2 пикселя
                    cursor_height = self.font_medium.get_height()
                    cursor_width = 2
                    cursor_x = current_x - cursor_width // 2  # Центрируем относительно начала символа
                    cursor_y = current_y

                    # Рисуем прямоугольник (полосу)
                    pygame.draw.rect(
                        self.display,
                        TEXT_DISPLAY_COLOR,  # Цвет полосы — такой же, как у текущего символа
                        pygame.Rect(cursor_x, cursor_y, cursor_width, cursor_height),
                        border_radius=1
                    )

                # Рисуем сам символ
                if current_x + char_width > x_start + line_length:
                    current_x = x_start
                    current_y += line_height

                self.display.blit(char_surface, (current_x, current_y))
                current_x += char_width

    def _draw_stats(self, y: int):
        wpm_text = self.font_medium.render(f"WPM: {self.wpm}", True, ACCENT_COLOR)
        accuracy_text = self.font_medium.render(f"Accuracy: {self.accuracy}%", True, ACCENT_COLOR)

        wpm_rect = wpm_text.get_rect(topleft=(int(self.current_width * 0.1), y))
        accuracy_rect = accuracy_text.get_rect(topleft=(int(self.current_width * 0.5), y))

        self.display.blit(wpm_text, wpm_rect)
        self.display.blit(accuracy_text, accuracy_rect)

    def _draw_keyboard(self):
        for key, rect in self.keys_rect.items():
            color = KEY_PRESSED_COLOR if key in self.pressed_keys else KEY_COLOR
            pygame.draw.rect(self.display, color, rect, border_radius=5)
            pygame.draw.rect(self.display, ACCENT_COLOR, rect, 2, border_radius=5)

            key_text = self.font_small.render(key, True, TEXT_COLOR)
            key_text_rect = key_text.get_rect(center=rect.center)
            self.display.blit(key_text, key_text_rect)

    def _save_results(self):
            """Сохраняет статистику по окончании теста."""
            elapsed_seconds = (pygame.time.get_ticks() - self.start_time) / 1000
            words_typed = len(self.typed_text.split())
            wpm = (words_typed / elapsed_seconds) * 60 if elapsed_seconds > 0 else 0
            cpm = (len(self.typed_text) / elapsed_seconds) * 60 if elapsed_seconds > 0 else 0

            correct_chars = sum(
                1 for i in range(min(len(self.typed_text), len(self.current_text)))
                if self.typed_text[i] == self.current_text[i]
            )
            total_chars = max(len(self.typed_text), 1)
            accuracy = int((correct_chars / total_chars) * 100)

            # Получаем текущую дату и время
            from datetime import datetime
            now = datetime.now()
            date_str = now.strftime("%d %b %Y")
            time_str = now.strftime("%H:%M:%S")

            self.result_stats = {
                'wpm': int(wpm),
                'accuracy': accuracy,
                'cpm': int(cpm),
                'words': words_typed,
                'characters': len(self.typed_text),
                'duration': f"{int(elapsed_seconds // 60):02}:{int(elapsed_seconds % 60):02}.{int((elapsed_seconds % 1) * 10):01}",
                'date': date_str,
                'time': time_str
            }

    def _draw_result_screen(self):
        """Рисует экран с результатами."""
        # Фон
        self.display.fill(BACKGROUND_COLOR)

        # Заголовок
        title_text = self.font_large.render("Test Results", True, ACCENT_COLOR)
        title_rect = title_text.get_rect(center=(self.current_width // 2, int(self.current_height * 0.1)))
        self.display.blit(title_text, title_rect)

        # Цвета для цифр
        number_color = TEXT_DISPLAY_COLOR
        label_color = TEXT_COLOR
        error_color = ERROR_COLOR

        # Размеры блоков
        block_width = 200
        block_height = 150
        padding = 20
        start_x = (self.current_width - (block_width * 4 + padding * 3)) // 2
        start_y = int(self.current_height * 0.2)

        # Блоки статистики
        stats_blocks = [
            ("WPM", self.result_stats['wpm'], number_color),
            ("Accuracy", f"{self.result_stats['accuracy']}%", number_color),
            ("CPM", self.result_stats['cpm'], number_color),
            ("Words", self.result_stats['words'], number_color),
            ("Characters", self.result_stats['characters'], number_color),
            ("Duration", self.result_stats['duration'], number_color),
            ("Date", self.result_stats['date'], label_color),
            ("Time", self.result_stats['time'], label_color)
        ]

        # Рисуем блоки
        for idx, (label, value, color) in enumerate(stats_blocks):
            col = idx % 4
            row = idx // 4
            x = start_x + col * (block_width + padding)
            y = start_y + row * (block_height + padding)

            # Фон блока
            pygame.draw.rect(self.display, KEY_COLOR, pygame.Rect(x, y, block_width, block_height), border_radius=8)

            # Название
            label_surface = self.font_small.render(label, True, label_color)
            label_rect = label_surface.get_rect(topleft=(x + 10, y + 10))
            self.display.blit(label_surface, label_rect)

            # Значение
            value_surface = self.font_medium.render(str(value), True, color)
            value_rect = value_surface.get_rect(center=(x + block_width // 2, y + block_height // 2))
            self.display.blit(value_surface, value_rect)

        # Инструкция
        instruction_text = self.font_small.render(
            "Press ENTER to start a new test",
            True,
            TEXT_COLOR
        )
        instruction_rect = instruction_text.get_rect(center=(self.current_width // 2, int(self.current_height * 0.85)))
        self.display.blit(instruction_text, instruction_rect)

        # Подсказка о логине (опционально)
        login_text = self.font_small.render(
            "Login to save test result",
            True,
            TEXT_COLOR
        )
        login_rect = login_text.get_rect(center=(self.current_width // 2, int(self.current_height * 0.9)))
        self.display.blit(login_text, login_rect)

    def _draw_settings_menu(self):
        """Рисует меню настроек под текстом."""
        for button in self.settings_buttons:
            # Рисуем фон кнопки
            pygame.draw.rect(self.display, button['color'], button['rect'], border_radius=5)
            # Рисуем текст
            text_surface = self.font_small.render(button['text'], True, button['text_color'])
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.display.blit(text_surface, text_rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = TypingApp()
    app.run()