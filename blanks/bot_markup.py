from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Вернуться в меню",
        callback_data="back-to-menu"
    )
)