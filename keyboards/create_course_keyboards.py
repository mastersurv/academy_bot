from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_course_kb():
	keyboard = InlineKeyboardMarkup(row_width=1)
	keyboard.add(
		InlineKeyboardButton("Приступить к созданию", callback_data="start_create"),
		InlineKeyboardButton("Назад", callback_data="back_to_create")
	)
	return keyboard


def back_to_start_create():
	keyboard = InlineKeyboardMarkup()
	keyboard.add(
		InlineKeyboardButton("Назад", callback_data="create_course")
	)
	return keyboard


def back_to_name_course():
	keyboard = InlineKeyboardMarkup()
	keyboard.add(
		InlineKeyboardButton("Назад", callback_data="back_to_name")
	)
	return keyboard


def back_to_short_description():
	keyboard = InlineKeyboardMarkup()
	keyboard.add(
		InlineKeyboardButton("Назад", callback_data="back_to_short_description")
	)
	return keyboard
