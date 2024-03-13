from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext

from blanks.bot_markup import owners_keyboard

from config import owners_ID


async def admin_handler(message: Message, state: FSMContext):
    tg_id = message.from_user.id

    if tg_id in owners_ID:
        bot, db = get_bot_and_db()

        await bot.send_message(
            chat_id=tg_id,
            text="Админка",
            reply_markup=owners_keyboard
        )

