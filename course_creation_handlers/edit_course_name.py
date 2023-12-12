from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.types import Message
from aiogram.dispatcher.dispatcher import FSMContext
from states_handlers.states import SettingsStates
from blanks.bot_markup import back_to_settings


async def edit_course_name(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat_id = message.chat.id
    m_id = message.message_id
    new_name = message.text

    async with state.proxy() as data:
        bot_token = data["bot_token"]
    db.update_course_name(bot_token=bot_token, new_name=new_name)

    await bot.delete_message(
        chat_id=chat_id,
        message_id=m_id - 1
    )

    await bot.send_message(
        chat_id=chat_id,
        text=f"Новое название курса: <br>{new_name}</br> успешно установлено",
        parse_mode="html",
        reply_markup=back_to_settings
    )

    await SettingsStates.settings.set()