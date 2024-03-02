from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext

from utils.functions.get_bot_and_db import get_bot_and_db


async def get_promo_usage_handler(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat = message.chat.id
    tg_id = message.from_user.id
    usage = message.text
    m_id = message.message_id

    async with state.proxy() as data:
        ci = data["course_id"]

    if usage.isdigit():
        new_promo = await db.generate_unique_promocode(course_id=ci)
        course_name = await db.get_course_name(course_id=ci)
        await db.add_promocode(
            promocode=new_promo,
            course_id=ci,
            usages_left=int(usage)
        )

        await bot.send_message(
            chat_id=tg_id,
            text=f"Для курса: <b>{course_name}</b>\n"
                 f"Успешно добавлен {usage}-разовый промокод: <i>{new_promo}</i>",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=f"get_course_promo_{ci}"
                )
            )
        )

        await state.finish()

    else:
        await bot.send_message(
            chat_id=tg_id,
            text="Количество использований должно быть целым числом, попробуйте снова или вернитесь назад",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=f"get_course_promo_{ci}"
                )
            )
        )
