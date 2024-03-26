from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.functions.get_bot_and_db import get_bot_and_db


async def generate_multi_keyboard(course_id=None, module_id=None, lesson_id=None, test_id=None, answer=None):
	bot, db = get_bot_and_db()
	keyboard = InlineKeyboardMarkup()

	if answer:
		test_number = await db.get_test_numbers(course_id=course_id, module_id=module_id, lesson_id=lesson_id)
		if test_id < test_number - 1:
			return "Далее", f"test_{course_id}_{module_id}_{lesson_id}_{test_id + 1}"
		else:
			lesson_number = await db.get_lessons_numbers(course_id=course_id, module_id=module_id)
			if lesson_id < lesson_number:
				return f"Следующий урок", f"lesson_{course_id}_{module_id}_{lesson_id + 1}"
			else:
				module_number = await db.get_modules_numbers(course_id=course_id)
				if module_id < module_number:
					return f"Следующий модуль", f"module_{course_id}_{module_id + 1}"
				else:
					return "К окончанию курса", f"finish_message_{course_id}"

	if test_id is not None:
		test_answers_list = await db.get_test_answers(course_id=course_id, module_id=module_id, lesson_id=lesson_id,
		                                              test_id=test_id)

		keyboard = InlineKeyboardMarkup()
		for i, (answer_id, answer_text) in enumerate(test_answers_list):
			keyboard.add(
				InlineKeyboardButton(
					text=answer_text,
					callback_data=f"answer_{course_id}_{module_id}_{lesson_id}_{test_id}_{i}"
				)
			)

		keyboard.add(
			InlineKeyboardButton(
				text="Назад",
				callback_data=f"lesson_{course_id}_{module_id}_{lesson_id}"
			)
		)
		return keyboard

	if lesson_id:
		# Клавиатура для урока
		has_next_lesson = await db.check_next_lesson(course_id, module_id, lesson_id)
		has_next_module = await db.check_next_module(course_id, module_id)
		test_id = await db.get_test_id_in_lesson(course_id, module_id, lesson_id)
		print(test_id)
		if test_id is not None:
			keyboard.add(
				InlineKeyboardButton(
					text="Приступить к заданию",
					callback_data=f"test_{course_id}_{module_id}_{lesson_id}_{test_id}"
				)
			)
		elif has_next_lesson:
			next_lesson_id = await db.get_next_lesson_in_module(course_id, module_id, lesson_id)
			if next_lesson_id:
				keyboard.add(
					InlineKeyboardButton(
					text="Следующий урок",
						callback_data=f"lesson_{course_id}_{module_id}_{next_lesson_id}"
					)
				)

		elif has_next_module:
			next_module_id = await db.get_next_module(course_id, module_id)
			if next_module_id:
				print('here')
				# lesson_name = await db.get_lesson_name(course_id=course_id, module_id=module_id,
				# 									   lesson_id=lesson_id + 1)
				module_name = await db.get_module_name(course_id=course_id, module_id=next_module_id)
				keyboard.add(
					InlineKeyboardButton(
						text=f"{module_name}",
						callback_data=f"module_{course_id}_{next_module_id}"
					)
				)

		else:
			keyboard.add(
				InlineKeyboardButton(
					text="К окончанию курса",
					callback_data=f"finish_message_{course_id}"
				)
			)

		keyboard.add(
			InlineKeyboardButton(
				text="Назад",
				callback_data=f"module_{course_id}_{module_id}"
			)
		)

	elif module_id is not None:
		# Клавиатура для модуля
		has_next_module = await db.check_next_module(course_id, module_id)
		if has_next_module:
			next_module_id = await db.get_next_module(course_id, module_id)
			if next_module_id:
				keyboard.add(
					InlineKeyboardButton(
						text="Следующий модуль",
						callback_data=f"module_{course_id}_{next_module_id}"
					)
				)
		keyboard.add(
			InlineKeyboardButton(
				text="Назад",
				callback_data=f"course_{course_id}"
			)
		)

	elif course_id is not None:
		# Клавиатура для курса
		keyboard.add(
			InlineKeyboardButton(
				text="Начать курс",
				callback_data=f"course_{course_id}"
			)
		)

	return keyboard
