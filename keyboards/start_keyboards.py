from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


# def get_start_keyboard():
#     keyboard = InlineKeyboardMarkup(row_width=1)
#     keyboard.add(
#         InlineKeyboardButton("telegram channel", url="https://t.me/xrenator"),
#         InlineKeyboardButton("Руководство по боту", url="https://chat.openai.com/")
#     )
#     return keyboard


def get_base_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(
        KeyboardButton("Я здесь впервые"),
        KeyboardButton("Я знаю, что я хочу")
    )
    return keyboard


def first_look_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Подобрать курс", callback_data="catalog"),
        InlineKeyboardButton("Помощь в создании",
                             url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUIcmlja3JvbGw%3D"),
        InlineKeyboardButton("Назад", callback_data="back_to_start")
    )
    return keyboard


def i_known_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Подобрать курс", callback_data="catalog"),
        InlineKeyboardButton("Создание курса", callback_data="base_menu"),
        InlineKeyboardButton("Назад", callback_data="back_to_start")
    )
    return keyboard
