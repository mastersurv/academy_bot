from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext
from states_handlers.states import SettingsStates


async def edit_lesson_description(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat_id = message.chat.id
    m_id = message.message_id
    lesson_description = message.text

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
        lesson_id = data["lesson_id"]
        mode = data.get("mode")

        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text="К настройкам курса",
                callback_data=f"module_settings_{course_id}_{module_id}"
            )
        )

        if mode == "creation":
            data["lesson_description"] = lesson_description

            text = "Отправьте материал к уроку, доступные форматы:\n" \
                   "1) Текст (поддерживается форматирование)\n" \
                   "2) Фото\n" \
                   "3) Фото с текстом\n" \
                   "4) Голосовое сообщение\n" \
                   "5) Видео\n" \
                   "6) Видеосообщение\n" \
                   "7) PDF-файлы\n"

            await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=keyboard
            )
            await SettingsStates.lesson_material.set()

        else:
            await db.update_lesson_description(course_id=course_id, module_id=module_id, lesson_id=lesson_id, new_description=lesson_description)

            await bot.send_message(
                chat_id=chat_id,
                text=f"Новое описание урока: <br>{lesson_description}</br> успешно установлено",
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="назад",
                        callback_data=f"lesson_settings_{course_id}_{module_id}_{lesson_id}"
                    )
                )
            )

            await SettingsStates.settings.set()