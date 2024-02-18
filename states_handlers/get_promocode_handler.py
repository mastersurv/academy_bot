from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.dispatcher.dispatcher import FSMContext

from blanks.bot_markup import to_menu

from utils.functions.get_bot_and_db import get_bot_and_db


async def get_promocode_handler(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat = message.chat.id
    tg_id = message.from_user.id
    promocode = message.text # TODO сделать генерацию промокодом при добавлении курса
    promocodes_dict = await db.get_promocodes_dict()
    print(promocodes_dict)
    m_id = message.message_id

    try:
        await bot.edit_message_reply_markup(
            chat_id=chat,
            message_id=m_id - 1,
            reply_markup=InlineKeyboardMarkup()
        )
    except:
        pass

    if promocode in promocodes_dict:
        await db.add_course_to_user(tg_id=tg_id, course_id=promocodes_dict[promocode])
        course_name = await db.get_course_name(course_id=promocodes_dict[promocode])
        await bot.send_message(
            chat_id=chat,
            text=f"Курс: <b>{course_name}</b> успешно добавлен в вашу библиотеку",
            parse_mode="html",
            reply_markup=to_menu
        )

    else:
        await bot.send_message(
            chat_id=chat,
            text=f"Промокода <b>{promocode}</b> не существует",
            parse_mode="html",
            reply_markup=to_menu
        )

    await state.finish()