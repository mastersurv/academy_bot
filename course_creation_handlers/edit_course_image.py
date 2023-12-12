from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.types import Message
from aiogram.dispatcher.dispatcher import FSMContext
from states_handlers.states import SettingsStates
from blanks.bot_markup import back_to_settings
import os


async def edit_course_image(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat_id = message.chat.id
    m_id = message.message_id
    new_image = message.photo[-1]

    async with state.proxy() as data:
        bot_token = data["bot_token"]

    await new_image.download(f"courses_avatars/{bot_token}")

    with open(bot_token, "rb") as new_image:
        db.update_course_image(bot_token=bot_token, new_image=new_image.read())

    os.remove(f"courses_avatars/{bot_token}")

    await bot.delete_message(
        chat_id=chat_id,
        message_id=m_id - 1
    )

    await bot.send_message(
        chat_id=chat_id,
        text=f"Новая аватарка курса успешно установлена",
        parse_mode="html",
        reply_markup=back_to_settings
    )

    await SettingsStates.settings.set()