from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_course_kb():
	keyboard = InlineKeyboardMarkup(row_width=1)
	keyboard.add(
		InlineKeyboardButton("Приступить к созданию", callback_data="start_create"),
		InlineKeyboardButton("Назад", callback_data="back_to_create")
	)
	return keyboard