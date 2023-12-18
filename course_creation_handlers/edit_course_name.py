from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.dispatcher.dispatcher import FSMContext
from states_handlers.states import SettingsStates
from blanks.bot_markup import back_to_settings, to_course_creation


async def edit_course_name(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat_id = message.chat.id
    m_id = message.message_id
    course_name = message.text

    try:
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=m_id - 1,
            reply_markup=InlineKeyboardMarkup()
        )
    except:
        pass

    async with state.proxy() as data:
        course_id = data["course_id"]
        mode = data.get("mode")

        if mode == "creation":
            data["course_name"] = course_name

            await bot.send_message(
                chat_id=chat_id,
                text="Введите описание курса:",
                reply_markup=to_course_creation
            )
            await SettingsStates.course_description.set()

        else:
            await db.update_course_name(course_id=course_id, new_name=course_name)

            await bot.send_message(
                chat_id=chat_id,
                text=f"Новое название курса: <br>{course_name}</br> успешно установлено",
                parse_mode="html",
                reply_markup=back_to_settings
            )

            await SettingsStates.settings.set()