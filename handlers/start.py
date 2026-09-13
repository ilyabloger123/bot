from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main_menu import get_main_keyboard

router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    """Обработчик комманды /start"""
    welcome_text = (
        'Добро пожаловать в менеджер паролей\n\n'
        'Я помогу вам:\n'
        '• Генерировать безопасные пароли\n'
        '• Сохранять пароли для сайтов\n'
        '• Управлять вашими паролями\n\n'
        'Выберите действие из меню ниже:'
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())
