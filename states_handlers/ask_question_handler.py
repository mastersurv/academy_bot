from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.dispatcher.dispatcher import FSMContext

from blanks.bot_markup import to_menu

from utils.functions.get_bot_and_db import get_bot_and_db
from config import group_id


async def ask_question_handler(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat = message.chat.id
    tg_id = message.from_user.id
    m_id = message.message_id

    try:
        await bot.edit_message_reply_markup(
            chat_id=chat,
            message_id=m_id - 1,
            reply_markup=InlineKeyboardMarkup()
        )
    except:
        pass

    try:
        message_to_chat = await bot.copy_message(
            chat_id=group_id,
            from_chat_id=tg_id,
            message_id=m_id,
            reply_to_message_id=await db.get_post_id(tg_id=tg_id)
        )
        await db.add_user_message(tg_id=tg_id, message_id=message_to_chat.message_id)

    except Exception as e:
        pass

    await bot.send_message(
        chat_id=chat,
        text="Ожидайте, сообщение с ответом придёт в этот чат",
        reply_markup=to_menu
    )

    await state.finish()