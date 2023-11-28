from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_courses():
    # Код для получения списка курсов из базы данных
    # Возвращаем список курсов в формате (id, name)
    courses = [(1, 'Course 1'), (2, 'Course 2'), (3, 'Course 3')]
    return courses


# Функция для генерации InlineKeyboardMarkup с кнопками для курсов
async def generate_courses_keyboard():
    courses = await get_courses()
    keyboard = InlineKeyboardMarkup(row_width=2)

    for course_id, course_name in courses:
        callback_data = f'course_{course_id}'
        button = InlineKeyboardButton(course_name, callback_data=callback_data)
        keyboard.add(button)

    return keyboard