from utils.functions.get_bot_and_db import get_bot_and_db
from utils.functions.files_ids import files_ids

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext

from states_handlers.states import SettingsStates


async def edit_lesson_material(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat_id = message.chat.id
    m_id = message.message_id

    text, audio_id, photo_id, video_id, video_note_id, document_id = files_ids(message=message, bot=bot)

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

        if mode == "creation":
            lesson_name = data["lesson_name"]

            await db.add_lesson(
                course_id=course_id,
                module_id=module_id,
                lesson_id=lesson_id,
                lesson_name=lesson_name,
                text=text,
                audio_id=audio_id,
                photo_id=photo_id,
                video_id=video_id,
                video_note_id=video_note_id,
                document_id=document_id
            )

            await bot.send_message(
                chat_id=chat_id,
                text=f"Вы успешно добавили урок - {lesson_name}\nы",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="Продолжить настройку урока",
                        callback_data=f"lesson_settings_{course_id}_{module_id}_{lesson_id}"
                    )
                ).add(
                    InlineKeyboardButton(
                        text="К настройкам модуля",
                        callback_data=f"module_settings_{course_id}_{module_id}"
                    )
                )
            )
            await state.finish()

        else:
            db.update_lesson_material(
                course_id=course_id,
                module_id=module_id,
                lesson_id=lesson_id,
                text=text,
                audio_id=audio_id,
                photo_id=photo_id,
                video_id=video_id,
                video_note_id=video_note_id,
                document_id=document_id
            )

            await bot.send_message(
                chat_id=chat_id,
                text=f"Новый материал успешно установлен",
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="назад",
                        callback_data=f"lesson_settings_{course_id}_{module_id}"
                    )
                )
            )

            await SettingsStates.settings.set()