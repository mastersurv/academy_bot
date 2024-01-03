from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def generate_multi_keyboard(course_id=None, module_id=None, lesson_id=None, test_id=None, answer=None):
	keyboard = InlineKeyboardMarkup()

	if answer:
		# Возвращаем только кнопку "Далее"
		return [("Далее", f"next_{test_id + 1}")]

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
