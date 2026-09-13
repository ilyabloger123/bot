from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from services.password_generator import PasswordGenerator

router = Router()
password_generator = PasswordGenerator()

@router.callback_query(lambda c: c.data.startswith("strength_"))
async def process_password_strength(callback: CallbackQuery):
    """Обработка выбора сложности пароля"""
    strength = callback.data.replace("strength_", "")
    lengths = {
        "weak":8,
        "medium":12,
        "strong":16,
        "very_strong":20
    }
    if strength in lengths:
        length = lengths[strength]
        password = password_generator.generate_password(length=length)
        await callback.message.edit_text(
            f"🔐 **Пароль ({strength.replace("_", " ")}):**\n\n"
            f"`{password}`\n\n"
            f"📊 Длина: {length} символов",
            parse_mode="Markdown"
        )
    elif strength == "custom":
        await callback.message.edit_text(
            "⚙️ **Настройка пароля**\n\n"
            "Отправьте желаемую длину пароля (от 8 до 32)"
        )
        await callback.answer()

@router.callback_query(lambda c: c.data.startswith("memorable_"))
async def process_memorable_password(callback: CallbackQuery):
    """Обработка запоминающихся паролей"""
    if callback.data == "memorable_examples":
        examples = [
            "sunset-ocean-mountain-breeze",
            "keyboard-dragon-flower-galaxy",
            "coffee-tiger-rainbow-wizard"
        ]
        text = "🧠 **Примеры запоминающихся паролей:**\n\n"
        for example in examples:
            words = example.replace("_", " ")
            text += f"`{example}`\n"
            text += f"💭 Можно запомнить как: {words}\n\n"
            await callback.message.edit_text(text, parse_mode="Markdown")
            await callback.answer()
            return

    if callback.data.startswith("memorable_"):
        try:
            word_count = int(callback.data.replace("memorable_", ""))
            password = password_generator.generate_memorable_password(word_count=word_count)
            await callback.message.edit_text(
                f"🧠 **Запоминающийся пароль ({word_count} слова):**\n\n"
                f"`{password}`\n\n"
                f"💭 **Совет:** Составьте историю: __{password.replace('_', ' ')}__",
                parse_mode="Markdown"
            )
        except ValueError:
            pass
    elif callback.data.startswith("separator_"):
        separator = callback.data.replace("separator_", "")
        password = password_generator.generate_memorable_password(separator=separator)
        separator_name = {
            "-":"Дефиз",
            "_":"Нижнее подчёркивание",
            ".":"Точка"
        }.get(separator, f"{separator}")
        await callback.message.edit_text(
            f"🧠 **Запоминающийся пароль (Разделитель: {separator_name})**\n\n"
            f"`{password}`",
            parse_mode="Markdown"
        )
    await callback.answer()

