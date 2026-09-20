from logging import exception

from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from services.password_generator import PasswordGenerator
from services.storage import PasswordStorage
from keyboards.main_menu import (
    get_main_keyboard,
    get_password_types_keyboard
)

router = Router()
password_generator = PasswordGenerator()
storage = PasswordStorage()

class PasswordStates(StatesGroup):
    waiting_for_site_to_delete = State()
    waiting_for_password_to_save = State()
    choosing_password_type = State()
    waiting_for_password_options = State()
    waiting_for_password_to_search = State()

@router.message(F.text=="🔐 Сгенерировать пароль")
@router.message(Command("generate"))
async def generate_password_main_handler(message: types.Message, state: FSMContext):
    """Меню выбора типа пароля"""
    message_text = (
        '🔐 **Выберите тип пароля:**\n\n'
        '🔢 **Стандартный** - случайные символы (более безопасный) - \n'
        '🧠 **Запоминающийся** - слова через разделитель (легче запомнить)\n'
        '⚙️ **Настроить** - выбрать параметры генерации'
    )
    await message.answer(message_text, parse_mode="Markdown", reply_markup=get_password_types_keyboard())
    await state.set_state(PasswordStates.choosing_password_type)

@router.message(PasswordStates.choosing_password_type)
async def handle_password_type_selection(message: types.Message, state: FSMContext):
    """Обработка выбора типа пароля"""
    if message.text == "🔢 Стандартный пароль":
        password = password_generator.generate_password(length=16)
        await message.answer(
            f"🔢 **Стандартный пароль:**\n\n"
            f"`{password}`\n\n"
            f"📊 **Длина:** 16 символов\n"
            f"🔡 **Символы:** буквы, цифры, спецсимволы\n\n"
            f"💡 **Чтобы сохранить, нажмите '💾 Сохранить пароль'**",
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()

    elif message.text == "🧠 Запоминающийся пароль":
        password = password_generator.generate_memorable_password(word_count=4, separator="-")
        await message.answer(
            f"🧠 **Запоминающийся пароль:**\n\n"
            f"`{password}`\n\n"
            f"📊 **Длина:** {len(password)} символов\n"
            f"🔤 **Структура:** 4 слова через дефис\n"
            f"💭 **Пример запоминания:** можно представить историю с этими словами\n\n"
            f"💡 **Чтобы сохранить, нажмите '💾 Сохранить пароль'**",
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()

    elif message.text == "⚙️ Настроить":
        await message.answer(
            "⚙️ **Настройка генерации пароля**\n\n"
            "Введите параметр в формате:\n"
            "тип:длина:разделитель\n\n"
            "**Примеры:**\n"
            "\\* `стандартный:12`\n"
            "\\* `запоминающийся:5:\\-`\n"
            "\\* `запоминающийся:3:\\_`",
            parse_mode="Markdown"
        )
        await state.set_state(PasswordStates.waiting_for_password_options)

    elif message.text == "◀️ Назад":
        await message.answer(
            "Возвращаемся в главное меню...",
            reply_markup=get_main_keyboard()
        )
        await state.clear()
    else:
        await message.answer(
            "Пожалуйста, выберите тип пароля из меню ниже:",
            reply_markup=get_password_types_keyboard()
        )

@router.message(PasswordStates.waiting_for_password_options)
async def handle_custom_password_options(message: types.Message, state: FSMContext):
    """Обработка кастомных параметров пароля"""
    try:
        parts = message.text.split(":")
        if len(parts) < 2:
            await message.answer(
                "❌ Неверный формат. Используйте: 'тип:длина' или 'тип:длина:разделитель'"
            )
            return
        password_type = parts[0].strip().lower()
        length = int(parts[1].strip())

        if password_type == "стандартный" or password_type == "standard":
            if length < 8:
                await message.answer("⚠️ Минимальная длина пароля - 8 символов")
                length = 8
            elif length > 32:
                await message.answer("⚠️ Максимальная длина пароля - 32 символа")
                length = 32
            password = password_generator.generate_password(length=length)
            await message.answer(
                f"🔢 **Кастомный стандартный пароль:**\n\n"
                f"`{password}`\n\n"
                f"📊 **Длина:** {length} символов\n"
                f"🔡 **Символы:** буквы, цифры, спецсимволы"
                f"💡 **Чтобы сохранить, нажмите '💾 Сохранить пароль'**",
                reply_markup=get_main_keyboard(),
                parse_mode="Markdown"
            )
        elif password_type == "запоминающийся" or password_type == "memorable":
            if length < 2:
                await message.answer("⚠️ Минимальное количевство слов - 2")
                length = 2
            elif length > 6:
                await message.answer("⚠️ Максимальное количевство слов - 6")
                length = 6

            separator = "-"
            if len(parts) > 2:
                separator = parts[2].strip()
                if not separator or len(separator) > 1:
                    separator = "-"
                    await message.answer("⚠️ Разделитель должен быть одним символом. Использую '-'")

            password = password_generator.generate_memorable_password(
                word_count=length,
                separator=separator
            )

            separator_name = {
                "-": "дефис",
                "_": "нижнее подчёркивание",
                ".": "точка",
                "|": "вертикальная черта"
            }.get(separator, f"символ {separator}")
            await message.answer(
                f"🧠 **Кастомный запоминающийся пароль:**\n\n"
                f"`{password}`\n\n"
                f"📊 **Количество слов:** {length}\n"
                f"🔤 **Разделитель:** {separator_name}\n"
                f"💭 **Совет:** составьте придложение из этих слов\n\n"
                f"💡 **Чтобы сохранить, нажмите '💾 Сохранить пароль'**",
                reply_markup=get_main_keyboard(),
                parse_mode="Markdown"
            )

        else:
            await message.answer("❌ Неверный тип пароля. Используйте 'стандартный' или 'запоминающийся'")
            return

        await state.clear()

    except ValueError:
        await message.answer("❌ Длина должна быть числом")

    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")
        await state.clear()

@router.message(F.text=="📋 Мои пароли")
@router.message(Command("list"))
async def list_passwords_handler(message: types.Message):
    """Показать все пароли"""
    passwords = storage.load_user_passwords(message.from_user.id)
    if not passwords:
        await message.answer("📭 У вас нет сохраненных паролей")
        return
    response = "**🔐 Ваши сохраненные пароли:**\n\n"
    for site, password in passwords.items():
        response += f"🌐 **{site}**: `{password}`\n"
    await message.answer(response, parse_mode="Markdown")

@router.message(F.text=="🔍 Найти пароль")
async def search_password_handler(message: types.Message, state: FSMContext):
    """Найти пароль"""
    passwords = storage.load_user_passwords(message.from_user.id)
    if not passwords:
        await message.answer("**У вас нет сохранённых паролей!**", parse_mode="Markdown")
        return
    await message.answer(
        "Для поиска сайта введите часть стоки URL\n"
        "Например:yout для youtube.com"
    )
    await state.set_state(PasswordStates.waiting_for_password_to_search)

@router.message(PasswordStates.waiting_for_password_to_search)
async def proccess_password_search(message: types.Message, state: FSMContext):
    """Обработка поиска паролей"""
    passwords = storage.load_user_passwords(message.from_user.id)
    response = "Результаты поиска:\n\n"
    counter = 0
    query = message.text
    for k, v in passwords.items():
        if query.lower() in k.lower():
            response += f"{k}: `{v}`\n"
            counter += 1
    if response == "Результаты поиска:\n\n":
        response = "По вашему запросу ничего не найдено"
    if counter > 15:
        response = "**Слишком много совпадений! Уточните запрос.**"
    await state.clear()
    await message.answer(response, parse_mode="Markdown")

@router.message(F.text=="❌ Удалить пароль")
async def delete_password_handler(message: types.Message, state: FSMContext):
    """Начало процесса удаления паролей"""
    passwords = storage.load_user_passwords(message.from_user.id)
    if not passwords:
        await message.answer("📭 У вас нет паролей для удаления")
        return
    sites_list = "\n".join([f"• {site}" for site in passwords.keys()])
    await message.answer(
        f"📋 **Ваши сайты:**\n{sites_list}\n\n"
        f"📝 **Для удаления отправьте название сайта:**\n"
        f"Например: `gmail.com`",
        parse_mode="Markdown"
    )
    await state.set_state(PasswordStates.waiting_for_site_to_delete)

@router.message(PasswordStates.waiting_for_site_to_delete)
async def process_site_deletion(message: types.Message, state: FSMContext):
    """Обработка удаления пароля по сайту"""
    site = message.text.strip()
    if storage.delete_password(message.from_user.id, site):
        await message.answer(f"✅ Пароль для **{site}** удален!", parse_mode="Markdown")
    else:
        await message.answer("❌ Сайт не найден в вашем списке. Попробуйте ещё раз.")

@router.message(F.text=="💾 Сохранить пароль")
async def save_password_handler(message: types.Message, state: FSMContext):
    """Начало процесса сохранения пароля"""
    await message.answer(
        "**💾 Сохранение пароля:**\n\n"
        "Отправьте пароль в формате:\n"
        "'сайт:пароль'\n\n"
        "Пример: 'gmail.com:qWeRtY12345.'",
        parse_mode="Markdown"
    )
    await state.set_state(PasswordStates.waiting_for_password_to_save)

@router.message(PasswordStates.waiting_for_password_to_save)
async def process_password_saving(message: types.Message, state: FSMContext):
    """Обработка сохранения пароля"""
    try:
        if ":" not in message.text:
            await message.answer("❌ Неверный формат. Используйте: 'сайт:пароль'")
            return
        site, password = message.text.split(":", 1)
        site = site.strip()
        password = password.strip()
        if not site or not password:
            await message.answer("❌ Неверный формат. Используйте: 'сайт:пароль'")
            return
        if storage.save_user_passwords(message.from_user.id, site, password):
            await message.answer(f"✅ Пароль для **{site}** успешно сохранён!", parse_mode="Markdown")
        else:
            await message.answer("❌ Ошибка при сохранении пароля")
        await state.clear()
    except Exception as e:
        await message.answer("❌ Ошибка при обработке запроса")
        await state.clear()

@router.message(lambda message: ":" in message.text and len(message.text.split(":")) == 2)
async def direct_save_password_handler(message: types.Message):
    """Прямое сохранение пароля в формате: сайт:пароль"""
    try:
        site, password = message.text.split(":", 1)
        site = site.strip()
        password = password.strip()
        if not site or not password:
            await message.answer("❌ Неверный формат. Используйте: 'сайт:пароль'")
            return
        if storage.save_user_passwords(message.from_user.id, site, password):
            await message.answer(f"✅ Пароль для **{site}** успешно сохранён!", parse_mode="Markdown")
        else:
            await message.answer("❌ Ошибка при сохранении пароля")
    except Exception as e:
        await message.answer("❌ Ошибка при обработке запроса")

@router.message(Command("check"))
async def check_password_strength(message: types.Message):
    """Проверка силы пароля"""
    if len(message.text.split()) < 2:
        await message.answer(
            "**Проверка силы пароля**\n\n"
            "Отправьте комманду в формате:\n"
            "/check ваш_пароль\n\n"
            "Пример: /check My_Password123!",
            parse_mode="Markdown"
        )
        return
    password = message.text.split(" ", 1)[1]
    result = password_generator.check_password_strength(password)
    feedback_text = "\n".join(result["feedback"]) if result["feedback"] else "✅ Все критерии выполнены"
    await message.answer(
        f"🔍 **Анализ пароля:**\n\n"
        f"📊 **Сила:** {result['strength']}\n"
        f"📏 **Длина:** {result['length']} символов\n"
        f"🎯 **Оценка:** {result['score']}\n\n"
        f"📋 **Характеристики:**\n"
        f"{'✅'if result['has_upper'] else '❌'} Заглавные буквы\n"
        f"{'✅'if result['has_lower'] else '❌'} Строчные буквы\n"
        f"{'✅'if result['has_digit'] else '❌'} Цифры\n"
        f"{'✅'if result['has_special'] else '❌'} Спецсимволы\n"
        f"💡 **Рекомендации:**\n{feedback_text}",
        parse_mode="Markdown"
    )
