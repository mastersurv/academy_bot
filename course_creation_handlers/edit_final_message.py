from utils.functions.get_bot_and_db import get_bot_and_db
from utils.functions.files_ids import files_ids
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext
from states_handlers.states import SettingsStates
from blanks.bot_markup import back_to_settings, to_course_creation


async def edit_final_message(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat_id = message.chat.id
    m_id = message.message_id

    text, audio_id, photo_id, video_id, video_note_id, document_id = await files_ids(message=message, bot=bot)
    # print(text, audio_id, photo_id, video_id, video_note_id, document_id)
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

    if any([text, audio_id, photo_id, video_id, video_note_id, document_id]):
        await db.add_final_message(
                course_id=course_id,
                text=text,
                audio_id=audio_id,
                photo_id=photo_id,
                video_id=video_id,
                video_note_id=video_note_id,
                document_id=document_id
            )

        await state.finish()
        course_name = await db.get_course_name(course_id=course_id)
        await bot.send_message(
            chat_id=chat_id,
            text=f"Вы успешно добавили финальное сообщение для курса:\n"
                 f"<b>{course_name}</b>",
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    text="К настройке курса",
                    callback_data=f"course_settings_{course_id}"
                )
            )
        )

    else:
        await bot.send_message(
            chat_id=chat_id,
            text="Отправьте финальное сообщение, это сообщение пользователи будут видеть, когда пройдут весь последний урок курса.\n" \
                 "После отправки можете вернуться к настройке курса\n" \
                 "Доступные форматы:\n" \
                 "1) Текст (поддерживается форматирование)\n" \
                 "2) Фото\n" \
                 "3) Фото с текстом\n" \
                 "4) Голосовое сообщение\n" \
                 "5) Видео\n" \
                 "6) Видеосообщение\n" \
                 "7) PDF-файлы\n",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    text="К настройке курса",
                    callback_data=f"course_settings_{course_id}"
                )
            )
        )