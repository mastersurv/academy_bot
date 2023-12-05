from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from getting_data import get_courses, get_course_modules, get_module_lessons
from create_bot import bot

token_from_bot = bot._token  # TODO: Получение токена нового бота


async def generate_courses_keyboard() -> InlineKeyboardMarkup:
	courses = await get_courses(token_from_bot)
	keyboard = InlineKeyboardMarkup()

	for course_id, course_name in courses:
		callback_data = f'course_{course_id}'
		button = InlineKeyboardButton(course_name, callback_data=callback_data)
		keyboard.add(button)

	return keyboard


async def generate_modules_keyboard(course_id: int) -> InlineKeyboardMarkup:
	modules = await get_course_modules(token_from_bot, course_id)
	keyboard = InlineKeyboardMarkup()

	for module_id, module_name in modules:
		callback_data = f'module_{module_id}'  # TODO сверить с ТЗ колбэк дату
		button = InlineKeyboardButton(module_name, callback_data=callback_data)
		keyboard.add(button)
	keyboard.add(InlineKeyboardButton("Назад", callback_data="back_courses"))

	return keyboard


async def generate_lessons_keyboard(course_id: int, module_id: int) -> InlineKeyboardMarkup:
	lessons = await get_module_lessons(token_from_bot, course_id, module_id)
	keyboard = InlineKeyboardMarkup()

	for lesson_id, lesson_name in lessons:
		callback_data = f'lesson_{lesson_id}'
		button = InlineKeyboardButton(lesson_name, callback_data=callback_data)
		keyboard.add(button)
	keyboard.add(InlineKeyboardButton("Назад", callback_data="back_modules"))

	return keyboard