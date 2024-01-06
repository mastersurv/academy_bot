from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from get_bot_and_db import get_bot_and_db


async def generate_multi_keyboard(course_id=None, module_id=None, lesson_id=None, test_id=None, answer=None):
	bot, db = get_bot_and_db()
	keyboard = InlineKeyboardMarkup()

	if answer:
		test_number = await db.get_test_numbers(course_id=course_id, module_id=module_id, lesson_id=lesson_id)
		if test_id < test_number:
			return "Далее", f"next_{test_id + 1}"
		else:
			lesson_number = await db.get_lessons_numbers(course_id=course_id, module_id=module_id)
			if lesson_id < lesson_number:
				# lesson_name = await db.get_lesson_name(course_id=course_id, module_id=module_id, lesson_id=lesson_id + 1)
				return "Следующий урок", f"lesson_{course_id}_{module_id}_{lesson_id + 1}"  # TODO f"{lesson_id + 1}. {lesson_name}
			else:
				module_number = await db.get_modules_numbers(course_id=course_id)
				if module_id < module_number:
					module_name = await db.get_module_name(course_id=course_id, module_id=module_id + 1)
					return f"{module_id + 1}. {module_name}", f"module_{course_id}_{module_id}"
				else:
					return "К окончанию курса", f"finish_message_{course_id}_{module_id}_{lesson_id}"

	if test_id is not None:
		# Клавиатура для теста
		keyboard.add(
			InlineKeyboardButton(
				text="Следующий вопрос",
				callback_data=f"next_question_{test_id + 1}"
			)
		).add(
			InlineKeyboardButton(
				text="Назад",
				callback_data=f"back_to_lesson_{lesson_id - 1}"
			)
		)

	elif lesson_id is not None:
		# Клавиатура для урока
		keyboard.add(
			InlineKeyboardButton(
				text="Следующий урок",
				callback_data=f"next_lesson_{lesson_id + 1}"
			)
		).add(
			InlineKeyboardButton(
				text="Назад",
				callback_data=f"back_to_module_{module_id - 1}"
			)
		)

	elif module_id is not None:
		# Клавиатура для модуля
		keyboard.add(
			InlineKeyboardButton(
				text="Следующий модуль",
				callback_data=f"next_module_{module_id + 1}"
			)
		).add(
			InlineKeyboardButton(
				text="Назад",
				callback_data=f"back_to_course_{course_id - 1}"
			)
		)

	elif course_id is not None:
		# Клавиатура для курса
		keyboard.add(
			InlineKeyboardButton(
				text="Начать курс",
				callback_data=f"start_course_{course_id}"
			)
		)

	return keyboard
