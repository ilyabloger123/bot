from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Основная клавиатура"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔐 Сгенерировать пароль")],
            [KeyboardButton(text="📋 Мои пароли"), KeyboardButton(text="🔍 Найти пароль")],
            [KeyboardButton(text="💾 Сохранить пароль"), KeyboardButton(text="❌ Удалить пароль")],
            [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )


def get_password_types_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора типа пароля"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔢 Стандартный пароль"), KeyboardButton(text="🧠 Запоминающийся пароль")],
            [KeyboardButton(text="⚙️ Настроить"), KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите тип пароля..."
    )


def get_settings_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура настроек"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="🔄 Экспорт паролей")],
            [KeyboardButton(text="🗑️ Очистить всё")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )


def get_yes_no_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура Да/Нет"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Да"), KeyboardButton(text="❌ Нет")]
        ],
        resize_keyboard=True
    )


def get_password_strength_keyboard() -> InlineKeyboardMarkup:
    """Инлайн клавиатура для выбора сложности пароля"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔒 Слабый (8 симв.)",
                callback_data="strength_weak"
            ),
            InlineKeyboardButton(
                text="🔐 Средний (12 симв.)",
                callback_data="strength_medium"
            )
        ],
        [
            InlineKeyboardButton(
                text="🛡️ Сильный (16 симв.)",
                callback_data="strength_strong"
            ),
            InlineKeyboardButton(
                text="⚡ Очень сильный (20 симв.)",
                callback_data="strength_very_strong"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎛️ Настроить",
                callback_data="strength_custom"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_memorable_options_keyboard() -> InlineKeyboardMarkup:
    """Инлайн клавиатура для запоминающихся паролей"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="3 слова",
                callback_data="memorable_3"
            ),
            InlineKeyboardButton(
                text="4 слова",
                callback_data="memorable_4"
            ),
            InlineKeyboardButton(
                text="5 слов",
                callback_data="memorable_5"
            )
        ],
        [
            InlineKeyboardButton(
                text="Разделитель: -",
                callback_data="separator_-"
            ),
            InlineKeyboardButton(
                text="Разделитель: _",
                callback_data="separator__"
            ),
            InlineKeyboardButton(
                text="Разделитель: .",
                callback_data="separator_."
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Примеры",
                callback_data="memorable_examples"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
