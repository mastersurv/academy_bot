from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.functions.get_bot_and_db import get_bot_and_db


async def generate_courses_keyboard(courses_ids_list: list) -> InlineKeyboardMarkup:
    bot, db = get_bot_and_db()
    keyboard = InlineKeyboardMarkup()

    for num, course_id in enumerate(courses_ids_list):
        course_name = await db.get_course_name(course_id=course_id)
        callback_data = f'course_{course_id}'
        button = InlineKeyboardButton(f"{num + 1}. {course_name}", callback_data=callback_data)
        keyboard.add(button)
    keyboard.add(
        InlineKeyboardButton(text="Назад", callback_data="menu")
    )
    return keyboard