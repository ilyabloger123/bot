from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_settings_main_keyboard() -> ReplyKeyboardMarkup:
    """Получение настроек главной клавиатуры"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔒 Настройки паролей")],
            [KeyboardButton(text="🔔 Уведомления"), KeyboardButton(text="🎨 Внешний вид")],
            [KeyboardButton(text="💾 Автосохранение"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="📤 Экспорт"), KeyboardButton(text="🗑️ Очистить всё")],
            [KeyboardButton(text="◀️ Назад в меню")]
        ],
        resize_keyboard=True
    )

def get_password_settings_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура настроек пароля"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📏 Длина пароля")],
            [KeyboardButton(text="🔤 Количество слов")],
            [KeyboardButton(text="🔣 Разделитель")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )

def get_notification_settings_keyboard(enabled: bool) -> ReplyKeyboardMarkup:
    """Клавиатула настроек уведомлений"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"{'❌ Отключить уведомления'if enabled else '✅ Включить уведомления'}")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )

def get_appearance_settings_keyboard(current_theme: str) -> ReplyKeyboardMarkup:
    """Клавиатура настроек темы"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"{'☀️ Светлая'if current_theme == "dark" else '🌑 Тёмная'}")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )

def get_export_options_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура выбора формата экспорта"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📄 JSON"), KeyboardButton(text="📝 CSV")],
            [KeyboardButton(text="📋 Текст")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )

def get_stats_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура статистики"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔄 Сбросить статистику")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )

def get_confirm_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура подтверждения"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Да"), KeyboardButton(text="❌ Нет")]
        ],
        resize_keyboard=True
    )

def get_autosave_keyboard(enabled: bool) -> ReplyKeyboardMarkup:
    """Клавиатура автосохранения"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"{'❌ Отключить автосохранение' if enabled else '✅ Включить автосохранение'}")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )

def get_password_strength_inline_keyboard() -> InlineKeyboardMarkup:
    """Инлайн клавиатура для выбора сложности пароля"""
    keyboard = [
        [InlineKeyboardButton(text="🔒 Низкая (8 символов)", callback_data="strength_low")],
        [InlineKeyboardButton(text="🔐 Средняя (12 символов)", callback_data="strength_medium")],
        [InlineKeyboardButton(text="🛡️ Высокая (16 символов)", callback_data="strength_high")],
        [InlineKeyboardButton(text="⚡️ Очень высокая (20+ символов)", callback_data="strength_very_high")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_export_inline_keyboard() -> InlineKeyboardMarkup:
    """Инлайн клавиатура для экспорта"""
    keyboard = [
        [
            InlineKeyboardButton(text="📄 JSON", callback_data="export_json"),
            InlineKeyboardButton(text="📝 CSV", callback_data="export_CSV"),
        ],
        [
            InlineKeyboardButton(text="📋 Текст", callback_data="export_text"),
            InlineKeyboardButton(text="🔐 Зашифрованный", callback_data="export_encrypted"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

