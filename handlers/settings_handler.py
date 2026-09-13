import json
import sqlite3
from datetime import datetime
from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from models.user_settings import SettingsDatabase, UserSettings
from keyboards.settings_keyboards import (
    get_settings_main_keyboard,
    get_password_settings_keyboard,
    get_notification_settings_keyboard,
    get_appearance_settings_keyboard,
    get_export_options_keyboard,
    get_confirm_keyboard,
    get_stats_keyboard
)
from keyboards.main_menu import get_main_keyboard
from services.storage import PasswordStorage


router = Router()
settings_db = SettingsDatabase()
password_storage = PasswordStorage()

class SettingsStates(StatesGroup):
    """Состояния для настроек"""
    waiting_for_password_length = State()
    waiting_for_word_count = State()
    waiting_for_separator = State()
    waiting_for_export_format = State()
    waiting_for_confirm_clear = State()
    waiting_for_theme = State()
    waiting_for_language = State()


@router.message(Command('settings'))
@router.message(F.text == '⚙️ Настройки')
async def settings_main_handler(message: Message, state: FSMContext):
    """Главное меню настроек"""
    if state:
        await state.clear()

    user_id = message.from_user.id
    settings = settings_db.get_settings(user_id)

    await message.answer(
        f"️**⚙️ Настройки пользователя**\n\n"
        f"**👤 Пользователь:** {message.from_user.full_name}\n"
        f"**📊 Текущие настройки:**\n"
        f"* Длина пароля: {settings.default_password_length}\n"
        f"* Количество слов: {settings.default_word_count}\n"
        f"* Разделитель: {settings.default_separator}\n"
        f"* Автосохранение: {'✅'if settings.auto_save else '❌'}\n"
        f"* Уведомления: {'✅'if settings.notification_enabled else '❌'}\n"
        f"* Тема: {'Светлая'if settings.theme == 'light' else 'Тёмная'}\n"
        f"**Выберите раздел настроек:**\n",
        reply_markup=get_settings_main_keyboard(),
        parse_mode="Markdown"
    )

@router.message(F.text == '🔒 Настройки паролей')
async def password_settings_handler(message: Message):
    """Меню настроек паролей"""

    user_id = message.from_user.id
    settings = settings_db.get_settings(user_id)

    await message.answer(
        f"🔐 **Настройки генерации паролей**\n\n"
        f"📏 **Длина пароля**:{settings.default_password_length}\n"
        f"🔤 **Количество слов**:{settings.default_word_count}\n"
        f"🔣 **Разделитель**:{settings.default_separator}\n"
        f"Что вы хотите изменить?",
        reply_markup=get_password_settings_keyboard(),
        parse_mode="Markdown"
    )

@router.message(F.text == '📏 Длина пароля')
async def change_password_length(message: Message, state: FSMContext):
    """Изменение длины пароля"""
    await message.answer(
        "📏 **Введите желаемую длину пароля** (от 8 до 32):\n\n"
        "Рекомендации:"
        "8-12 - Средняя безопасность"
        "13-18 - Высокая безопасность"
        "19-32 - Очень высокая безопасность",
        parse_mode="Markdown"
    )
    await state.set_state(SettingsStates.waiting_for_password_length)

@router.message(SettingsStates.waiting_for_password_length)
async def process_password_length(message: Message, state: FSMContext):
    """Обработка новой длины пароля"""
    try:
        length = int(message.text.strip())
        if length < 8:
            await message.answer("❌ Длина должна быть не менее 8 символов. Используйте значение 8-32")
            return
        elif length > 32:
            await message.answer("❌ Длина должна быть не больше 32 символов. Используйте значение 8-32")
            return

        user_id = message.from_user.id
        settings_db.update_settings(user_id, default_password_length=length)
        await message.answer(f"✅ Длина пароля изменена на **{length}** символов", parse_mode="Markdown")
        await state.clear()
        await password_settings_handler(message)
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число")

@router.message(F.text == '🔤 Количество слов')
async def change_word_count(message: Message, state: FSMContext):
    """Изменение количества слов для запоминающихся паролей"""
    await message.answer(
        "🔤 **Введите количество слов** для запоминающегося пароля(от 2 до 6)\n\n"
        "Рекомендации:\n"
        "2-3 слова - легко запомнить\n"
        "4 - оптимально\n"
        "5-6 слов - максимальная безопасность",
        parse_mode="Markdown"
    )
    await state.set_state(SettingsStates.waiting_for_word_count)

@router.message(SettingsStates.waiting_for_word_count)
async def process_word_count(message: Message, state: FSMContext):
    """Обработка нового количества слов"""
    try:
        count = int(message.text.strip())
        if count < 2:
            await message.answer("❌ Количество должно быть не менее 2 слов. Используйте значение 2-6")
            return
        if count < 2:
            await message.answer("❌ Количество должна быть не более 6 слов. Используйте значение 2-6")
            return
        user_id = message.from_user.id
        settings_db.update_settings(user_id, default_word_count=count)
        await message.answer(f"✅ Количество слов изменено на **{count}**", parse_mode="Markdown")
        await state.clear()
        await password_settings_handler(message)
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число")

@router.message(F.text == '🔣 Разделитель')
async def change_separator(message: Message, state: FSMContext):
    """Изменение разделителя для запоминающихся паролей"""
    await message.answer(
        "🔣 Введите разделитель для запоминающегося пароля\n\n"
        "Популярные варианты:\n"
        "* '-' (дефис)\n"
        "* '_' (нижнее подчёркивание)\n"
        "* '.' (точка)\n"
        "* '|' (вертикальная черта)\n\n"
        "Можно использовать любой символ кроме пробела"
        # parse_mode="Markdown"
    )
    await state.set_state(SettingsStates.waiting_for_separator)

@router.message(SettingsStates.waiting_for_separator)
async def process_separator(message: Message, state: FSMContext):
    """Обработка нового разделителя"""
    separator = message.text.strip()
    if not separator or len(separator) > 1:
        await message.answer("❌ Пожалуйста, введите 1 символ (не пробел)")
        return
    user_id = message.from_user.id
    settings_db.update_settings(user_id, default_separator=separator)
    separator_names = {
        "-" : "дефис",
        "_" : "нижнее подчёркивание",
        "." : "точка",
        "|" : "вертикальная черта"
    }
    separator_name = separator_names.get(separator, f"символ {separator}")
    await message.answer(
        f"✅ Разделитель изменился на **{separator_name}**!",
        parse_mode="Markdown"
    )
    await state.clear()
    await password_settings_handler(message)

@router.message(F.text == "🔔 Уведомления")
async def notifications_settings_handler(message: Message):
    """Меню настроек уведомлений"""
    user_id = message.from_user.id
    settings = settings_db.get_settings(user_id)
    status = "✅ Включены" if settings.notification_enabled else "❌ Отключены"
    await message.answer(
        f"🔔 **Настройка уведомлений**\n\n"
        f"Текущий статус: {status}\n\n"
        f"Выберите действие:",
        reply_markup=get_notification_settings_keyboard(settings.notification_enabled),
        parse_mode="Markdown"
    )

@router.message(F.text == "✅ Включить уведомления")
async def enable_notifications(message: Message):
    """Включение уведомлений"""
    user_id = message.from_user.id
    settings_db.update_settings(user_id, notification_enabled=True)
    await message.answer(
        "✅ Уведомления включены!\n"
        "Теперь вы будете получать оповещения о важных событиях.",
        reply_markup=get_settings_main_keyboard()
    )

@router.message(F.text == "❌ Отключить уведомления")
async def disable_notifications(message: Message):
    """Отключение уведомлений"""
    user_id = message.from_user.id
    settings_db.update_settings(user_id, notification_enabled=False)
    await message.answer(
        "🔕 Уведомления отключены.",
        reply_markup=get_settings_main_keyboard()
    )

@router.message(F.text == "🎨 Внешний вид")
async def appearance_settings_handler(message: Message):
    """Меню настроек внешнего вида"""
    user_id = message.from_user.id
    settings = settings_db.get_settings(user_id)
    current_theme = "Светлая" if settings.theme == "light" else "Тёмная"
    await message.answer(
        f"🎨 **Настройки внешнего вида**\n\n"
        f"Текущая тема: {current_theme}\n\n"
        f"Выберите тему:",
        reply_markup=get_appearance_settings_keyboard(settings.theme),
        parse_mode="Markdown"
    )

@router.message(F.text == "☀️ Светлая")
async def set_light_theme(message: Message):
    """Установка светлой темы"""
    user_id = message.from_user.id
    settings_db.update_settings(user_id, theme="light")
    await message.answer(
        "☀️ Установлена светлая тема!",
        reply_markup=get_settings_main_keyboard()
    )


@router.message(F.text == "🌑 Тёмная")
async def set_dark_theme(message: Message):
    """Установка тёмной темы"""
    user_id = message.from_user.id
    settings_db.update_settings(user_id, theme="dark")
    await message.answer(
        "🌑 Установлена тёмная тема!",
        reply_markup=get_settings_main_keyboard()
    )

@router.message(F.text == "💾 Автосохранение")
async def auto_save_settings_handler(message: Message):
    """Настройка автосохранения"""
    user_id = message.from_user.id
    settings = settings_db.get_settings(user_id)
    if settings.auto_save:
        settings_db.update_settings(user_id, auto_save=False)
        new_status = "отключено"
    else:
        settings_db.update_settings(user_id, auto_save=True)
        new_status = "включено"

    await message.answer(
        f"Автосохранение паролей **{new_status}**!",
        parse_mode="Markdown"
    )
    await settings_main_handler(message, None)

@router.message(F.text == "📊 Статистика")
async def statistics_handler(message: Message):
    """Показ статистики пользователя"""
    user_id = message.from_user.id
    stats = settings_db.get_stats(user_id)
    passwords = password_storage.load_user_passwords(user_id)

    settings = settings_db.get_settings(user_id)

    days_active = 0
    if settings.created_at:
        days_active = (datetime.now() - datetime.strptime(
            settings.created_at.split()[0], "%Y-%m-%d"
        )).days
    await message.answer(
        f"📊 **Ваша статистика**\n\n"
        f"🔐 **Сгенерировано паролей**:{stats.get("generated")}\n"
        f"💾 **Сохранено паролей**:{stats.get("saved")}\n"
        f"📁 **Количество паролей в хранилище**:{len(passwords)}\n"
        f"📅 **Дней с нами**:{days_active}\n"
        f"⏰ **Последняя активность**:{stats.get("last_activities")}\n\n"
        f"Продолжайте в том же духе!",
        reply_markup=get_stats_keyboard(),
        parse_mode="Markdown"
    )

@router.message(F.text == "🔄 Сбросить статистику")
async def reset_statistics_handler(message: Message, state: FSMContext):
    """Сброс статистики"""
    await message.answer(
        "⚠️ **Вы уверены что хотите сбросить статистику**?\n\n"
        "Это действие нельзя отменить.",
        reply_markup=get_confirm_keyboard(),
        parse_mode="Markdown"
    )
    await state.set_state(SettingsStates.waiting_for_confirm_clear)

@router.message(SettingsStates.waiting_for_confirm_clear)
async def confirm_reset_statistics(message: Message, state: FSMContext):
    """Подтверждение сброса статистик"""
    if message.text == "✅ Да":
        user_id = message.from_user.id
        with sqlite3.connect(settings_db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE user_stats
                SET passwords_generated=0, saved_passwords_state=0
                WHERE user_id = ?
            """, (user_id,))
            conn.commit()

        await message.answer(
            "✅ Статистика успешно сброшена!",
            reply_markup=get_settings_main_keyboard()
        )
    else:
        await message.answer(
            "Сброс статистики отменён",
            reply_markup=get_settings_main_keyboard()
        )
    await state.clear()

@router.message(F.text == "◀️ Назад")
async def back_handler(message: Message, state: FSMContext):
    await message.answer(
        "Возвращаемся в меню настроек",
        reply_markup=get_settings_main_keyboard()
    )
    await state.clear()

@router.message(F.text == "◀️ Назад в меню")
async def back_to_main_handler(message: Message, state: FSMContext):
    await message.answer(
        "Возвращаемся в главное меню",
        reply_markup=get_main_keyboard()
    )
    await state.clear()
