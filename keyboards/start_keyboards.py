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
