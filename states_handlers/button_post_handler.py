from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext

from config import easycourses_channel


async def button_post_handler(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    tg_id = message.from_user.id
    m_id = message.message_id

    await bot.copy_message(
        chat_id=easycourses_channel,
        from_chat_id=tg_id,
        message_id=m_id,
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text="Перейти к боту",
                url="https://t.me/courses_Bbot"
            )
        )
    )

    await state.finish()

    await bot.send_message(
        chat_id=tg_id,
        text="Пост успешно отправлен в канал\n"
             "ВАЖНО: если до этого вы что-либо делали, например загружали материалы в урок и вдруг резко захотелось нажать /admin,"
             "то состояние сбросилось, новый путь только через /start"
    )