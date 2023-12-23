from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.functions.get_bot_and_db import get_bot_and_db


async def generate_lessons_keyboard(course_id: int, module_id: int, passing=None) -> InlineKeyboardMarkup:
    bot, db = get_bot_and_db()
    lessons = await db.get_module_lessons(course_id=course_id, module_id=module_id)
    keyboard = InlineKeyboardMarkup()

    for num, lessons_tuple in enumerate(lessons):
        lesson_id, lesson_name = lessons_tuple
        callback_data = f'lesson_{course_id}_{module_id}_{lesson_id}' if passing else f'lesson_settings_{course_id}_{module_id}_{lesson_id}'
        button = InlineKeyboardButton(text=f"{num + 1}. {lesson_name}", callback_data=callback_data)
        keyboard.add(button)
    end_callback = f"course_{course_id}" if passing else f"module_settings_{course_id}_{course_id}"
    keyboard.add(InlineKeyboardButton("Назад", callback_data=end_callback))

    return keyboard