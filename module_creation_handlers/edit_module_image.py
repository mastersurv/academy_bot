from utils.functions.get_bot_and_db import get_bot_and_db

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext

from states_handlers.states import SettingsStates


async def edit_module_image(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat_id = message.chat.id
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
        module_id = data["module_id"]
        mode = data.get("mode")

        if mode == "creation":
            module_name = data["module_name"]
            module_description = data["module_description"]

            await db.add_module(
                course_id=course_id,
                module_id=module_id,
                module_name=module_name,
                module_description=module_description,
                module_image=image_file_id,
            )

            await bot.send_message(
                chat_id=chat_id,
                text=f"Вы успешно добавили модуль - {module_name}\n",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="Продолжить настройку модуля",
                        callback_data=f"module_settings_{course_id}_{module_id}"
                    )
                ).add(
                    InlineKeyboardButton(
                        text="К настройкам курса",
                        callback_data=f"course_settings_{course_id}"
                    )
                )
            )
            await state.finish()

        else:
            await db.update_module_image(course_id=course_id, module_id=module_id, image_file_id=image_file_id)

            await bot.send_message(
                chat_id=chat_id,
                text=f"Новая аватарка модуля успешно установлена",
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="Назад",
                        callback_data=f"module_settings_{course_id}_{module_id}"
                    )
                )
            )

            await SettingsStates.settings.set()