from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext
from states_handlers.states import SettingsStates


async def test_keyboard_handler(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat_id = message.chat.id
    m_id = message.message_id
    test_keyboard = list(map(lambda x: x.strip().lower().capitalize(), message.text.split("\n")))

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
        test_question = data["test_question"]
        data["test_keyboard"] = test_keyboard

    keyboard = InlineKeyboardMarkup()
    for num, elem in enumerate(test_keyboard):
        keyboard.add(
            InlineKeyboardButton(
                text=elem,
                callback_data=f"choose_answer_{num}_{course_id}_{module_id}_{lesson_id}"
            )
        )

    await bot.send_message(
        chat_id=chat_id,
        text=f"Выберите ВЕРНЫЙ вариант ответа.\n<b>{test_question}</b>",
        parse_mode="html",
        reply_markup=keyboard
    )

    await SettingsStates.settings.set()