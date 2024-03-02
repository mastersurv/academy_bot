from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.dispatcher.dispatcher import FSMContext

from blanks.bot_markup import to_menu

from utils.functions.get_bot_and_db import get_bot_and_db


async def get_promocode_handler(message: Message, state: FSMContext):  # Triggered when user send promocode
    bot, db = get_bot_and_db()
    chat = message.chat.id
    tg_id = message.from_user.id
    promocode = message.text
    promocodes_dict = await db.get_promocodes_dict()
    n_promocode_dict = await db.get_n_promocodes_dict()
    chat_promocodes_dict = await db.get_chat_promocodes_dict() # TODO

    m_id = message.message_id

    try:
        await bot.edit_message_reply_markup(
            chat_id=chat,
            message_id=m_id - 1,
            reply_markup=InlineKeyboardMarkup()
        )
    except Exception as e:
        print(e)

    if promocode in promocodes_dict:
        # await db.add_course_to_user(tg_id=tg_id, course_id=promocodes_dict[promocode])
        await db.add_user_course(tg_id=tg_id, course_id=promocodes_dict[promocode])
        course_name = await db.get_course_name(course_id=promocodes_dict[promocode])
        await bot.send_message(
            chat_id=chat,
            text=f"Курс: <b>{course_name}</b> успешно добавлен в вашу библиотеку",
            parse_mode="html",
            reply_markup=to_menu
        )

    elif promocode in n_promocode_dict:
        await db.minus_usage(promocode=promocode)
        await db.add_user_course(tg_id=tg_id, course_id=n_promocode_dict[promocode])
        course_name = await db.get_course_name(course_id=n_promocode_dict[promocode])
        await bot.send_message(
            chat_id=chat,
            text=f"Курс: <b>{course_name}</b> успешно добавлен в вашу библиотеку",
            parse_mode="html",
            reply_markup=to_menu
        )

        usage_left = await db.get_usage_remain(promocode=promocode) # TODO get_usage_remain(promocode) - сколько использований у промокода

        if usage_left == 0:
            creator_id = await db.get_creator_id(course_id=n_promocode_dict[promocode]) # TODO get_creator_id(course_id)
            await bot.send_message(
                chat_id=creator_id,
                text=f"У промокода: {promocode} закончились использования.\n"
                     f"Чтобы создать новый перейдите в меню, выберите Промокоды -> Курс -> Создать n-промокод"
            )

            await db.delete_promocode(promocode=promocode) # TODO delete_promocode(promocode)

    elif promocode in chat_promocodes_dict:
        chat_id, chat_title = await db.get_chat_id_and_title(promocode=promocode) # TODO get_chat_id_and_title
        is_member = await bot.get_chat_member(chat_id, tg_id)

        # creators_ids = await self.db.get_creators_ids()
        # if tg_id in creators_ids:
        #     keyboard = admin_menu
        if is_member.status == "member" or is_member.status == "creator" or is_member.status == "administrator":
            await db.add_user_course(tg_id=tg_id, course_id=chat_promocodes_dict[promocode])
            course_name = await db.get_course_name(course_id=chat_promocodes_dict[promocode])
            await bot.send_message(
                chat_id=chat,
                text=f"Курс: <b>{course_name}</b> успешно добавлен в вашу библиотеку",
                parse_mode="html",
                reply_markup=to_menu
            )
        else:
            await bot.send_message(
                chat_id=chat,
                text=f"Вы не являетесь участником группы: <b>{chat_title}</b>, поэтому данный промокод для вас не действует",
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