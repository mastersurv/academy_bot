from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.functions.get_bot_and_db import get_bot_and_db


async def generate_lessons_keyboard(course_id: int, module_id: int) -> InlineKeyboardMarkup:
    bot, db = get_bot_and_db()
    lessons = await db.get_module_lessons(course_id=course_id, module_id=module_id)
    keyboard = InlineKeyboardMarkup()

    for num, lessons_tuple in enumerate(lessons):
        lesson_id, lesson_name = lessons_tuple
        callback_data = f'lesson_{module_id}_{lesson_id}'
        button = InlineKeyboardButton(text=f"{num + 1}. {lesson_name}", callback_data=callback_data)
        keyboard.add(button)
    keyboard.add(InlineKeyboardButton("Назад", callback_data="back_modules"))

    return keyboard