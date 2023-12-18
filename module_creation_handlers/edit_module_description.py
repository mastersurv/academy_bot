from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext
from states_handlers.states import SettingsStates



async def edit_module_description(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat_id = message.chat.id
    m_id = message.message_id
    module_description = message.text

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

        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text="К настройкам курса",
                callback_data=f"course_settings_{course_id}"
            )
        )

        if mode == "creation":
            data["module_description"] = module_description

            await bot.send_message(
                chat_id=chat_id,
                text="Отправьте превью модуля\n(банер, плакат, аватар):",
                reply_markup=keyboard
            )
            await SettingsStates.module_image.set()

        else:
            await db.update_module_description(course_id=course_id, module_id=module_id, new_description=module_description)

            await bot.send_message(
                chat_id=chat_id,
                text=f"Новое описание модуля: <br>{module_description}</br> успешно установлено",
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="назад",
                        callback_data=f"module_settings_{course_id}_{module_id}"
                    )
                )
            )

            await SettingsStates.settings.set()