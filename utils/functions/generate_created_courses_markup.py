from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.functions.get_bot_and_db import get_bot_and_db


async def generate_created_courses_keyboard(tg_id: int, analytics=None) -> InlineKeyboardMarkup:
    bot, db = get_bot_and_db()
    keyboard = InlineKeyboardMarkup()
    courses_ids = await db.get_created_courses_ids(tg_id=tg_id)

    course_part = "analytic" if analytics else "settings"

    for num, course_id in enumerate(courses_ids):
        course_name = await db.get_course_name(course_id=course_id)
        callback_data = f'course_{course_part}_{course_id}'
        button = InlineKeyboardButton(f"{num + 1}. {course_name.title()}", callback_data=callback_data)
        keyboard.add(button)

    return keyboard