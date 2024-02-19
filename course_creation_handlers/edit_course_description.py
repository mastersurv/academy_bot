from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.dispatcher.dispatcher import FSMContext
from states_handlers.states import SettingsStates
from blanks.bot_markup import back_to_settings, to_course_creation


async def edit_course_description(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat_id = message.chat.id
    m_id = message.message_id
    course_description = message.text

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
            data["course_description"] = course_description

            await bot.send_message(
                chat_id=chat_id,
                text="Отправьте превью курса\n(банер, плакат, аватар):"
                     "\n\n<b>Важно:</b> Для сохранения курса завершите данный шаг",
	            parse_mode='html',
                reply_markup=to_course_creation
            )
            await SettingsStates.course_image.set()

        else:
            await db.update_course_description(course_id=course_id, new_description=course_description)

            await bot.send_message(
                chat_id=chat_id,
                text=f"Новое описание курса: <b>{course_description}</b> успешно установлено",
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup().add(
					InlineKeyboardButton(text='Назад', callback_data=f'course_settings_{course_id}'))
			)

            await SettingsStates.settings.set()
