from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.functions.get_bot_and_db import get_bot_and_db


async def generate_modules_keyboard(course_id: int, passing=None) -> InlineKeyboardMarkup:
    bot, db = get_bot_and_db()
    modules = await db.get_course_modules(course_id=course_id)

    keyboard = InlineKeyboardMarkup()

    for num, module_tuple in enumerate(modules):
        module_id, module_name = module_tuple
        callback_data = f'module_{course_id}_{module_id}' if passing else f'module_settings_{course_id}_{module_id}'
        button = InlineKeyboardButton(text=f"{num + 1}. {module_name}", callback_data=callback_data)
        keyboard.add(button)

    end_callback = f"course_creation" if passing is None else f"menu"
    # end_callback = "library"
    keyboard.add(InlineKeyboardButton("Назад", callback_data=end_callback))

    return keyboard