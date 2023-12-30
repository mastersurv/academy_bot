from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext
from states_handlers.states import SettingsStates


async def test_question_handler(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat_id = message.chat.id
    m_id = message.message_id
    test_question = message.text

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
        data["test_question"] = test_question

    await bot.send_message(
        chat_id=chat_id,
        text="Теперь отправьте варианты ответа, они будут в виде кнопок, прикреплённых к сообщению, отправлять в формате:\n"
             "ответ1\n"
             "ответ2\n"
             "ВАЖНО: обязательно каждый отдельный ответ с красной строки",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text="К настройкам курса",
                callback_data=f"lesson_settings_{course_id}_{module_id}_{lesson_id}"
            )
        )
    )

    await SettingsStates.test_keyboard.set()