from utils.functions.get_bot_and_db import get_bot_and_db

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext

from states_handlers.states import SettingsStates
from blanks.bot_markup import back_to_settings


async def edit_course_image(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat_id = message.chat.id
    tg_id = message.from_user.id
    m_id = message.message_id
    image_file_id = message.photo[-1]["file_id"]

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
            course_name = data["course_name"]
            course_description = data["course_description"]
            new_promocode = await db.generate_unique_promocode(course_id=course_id)

            await db.add_course(
                course_id=course_id,
                owner_id=tg_id,
                course_name=course_name,
                course_description=course_description,
                course_image_id=image_file_id,
                promocode=new_promocode
            )

            await bot.send_message(
                chat_id=chat_id,
                text=f"Вы успешно добавили курс - {course_name}\nВот промокод к курсу - ",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="Продолжить настройку курса",
                        callback_data=f"course_settings_{course_id}"
                    )
                ).add(
                    InlineKeyboardButton(
                        text="К списку курсов",
                        callback_data="created_courses"
                    )
                )
            )
            await state.finish()

        else:
            await db.update_course_image(course_id=course_id, image_file_id=image_file_id)

            await bot.send_message(
                chat_id=chat_id,
                text=f"Новая аватарка курса успешно установлена",
                parse_mode="html",
                reply_markup=back_to_settings
            )

            await SettingsStates.settings.set()