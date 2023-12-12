from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.types import Message
from aiogram.dispatcher.dispatcher import FSMContext
from states_handlers.states import SettingsStates
from blanks.bot_markup import back_to_settings


async def edit_course_description(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat_id = message.chat.id
    m_id = message.message_id
    new_description = message.text

    async with state.proxy() as data:
        bot_token = data["bot_token"]
    db.update_course_description(bot_token=bot_token, new_description=new_description)

    await bot.delete_message(
        chat_id=chat_id,
        message_id=m_id - 1
    )

    await bot.send_message(
        chat_id=chat_id,
        text=f"Новое описание курса: <br>{new_description}</br> успешно установлено",
        parse_mode="html",
        reply_markup=back_to_settings
    )

    await SettingsStates.settings.set()