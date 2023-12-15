from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.functions.get_bot_and_db import get_bot_and_db


async def generate_modules_keyboard(course_id: int) -> InlineKeyboardMarkup:
    bot, db = get_bot_and_db()
    modules = await db.get_course_modules(course_id=course_id)
    keyboard = InlineKeyboardMarkup()

    for num, module_tuple in enumerate(modules):
        module_id, module_name = module_tuple
        callback_data = f'module_settings_{course_id}_{module_id}'
        button = InlineKeyboardButton(text=f"{num + 1}. {module_name.title()}", callback_data=callback_data)
        keyboard.add(button)
    keyboard.add(InlineKeyboardButton("Назад", callback_data=f"course_settings_{course_id}"))

    return keyboard