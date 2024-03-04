from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.dispatcher import FSMContext


async def set_group_handler(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    tg_id = message.from_user.id
    chat_id = message.chat.id
    chat_type = message.chat.type

    print(f"Файл get_promo_usage_handler.py проверка chat_type: {chat_type}")
    if chat_type in ["group", "supergroup"]:
        courses_ids = await db.get_courses_ids(tg_id=tg_id)
        keyboard = InlineKeyboardMarkup()
        for ci in courses_ids:
            course_name = await db.get_course_name(course_id=ci)
            keyboard.add(
                InlineKeyboardButton(
                    text=f"{course_name}",
                    callback_data=f"set_group_{ci}"
                )
            )

        await bot.send_message(
            chat_id=chat_id,
            text="Выберите курс, к которому хотите привязать группу",
            reply_markup=keyboard
        )