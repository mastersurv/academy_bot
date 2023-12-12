from aiogram import Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.dispatcher import FSMContext


from utils.functions.get_bot_and_db import get_bot_and_db

from utils.functions.generate_courses_markup import generate_courses_keyboard
from utils.functions.generate_modules_markup import generate_modules_keyboard

from states_handlers.states import SettingsStates, MenuStates
from blanks.bot_markup import (
    menu,
    to_menu,
    bot_settings_mp,
    modules_settings_mp,
    lessons_settings_mp,
    back_to_modules,
    back_to_lessons,
    back_to_settings
)


async def constructor_callback_handler(call: CallbackQuery, state: FSMContext):
    bot, db = get_bot_and_db()
    chat = call.message.chat.id
    tg_id = call.message.from_user.id
    callback = call.data
    m_id = call.message.message_id

    if callback == "menu":
        creators_ids = await db.get_creators_ids()
        if tg_id in creators_ids:
            menu.add(
                InlineKeyboardButton(
                    text="Создание курсов",
                    callback_data="creation_courses"
                ))

        try:
            await bot.edit_message_text(
                chat_id=chat,
                message_id=m_id,
                text="<b>Меню</b>",
                parse_mode="html",
                reply_markup=menu
            )
        except:
            pass

    elif callback == "library":
        courses_ids = await db.get_courses_ids(tg_id=tg_id)
        if len(courses_ids) == 0:
            try:
                await bot.edit_message_text(
                    chat_id=chat,
                    text="К сожалению у вас нет доступа ни к одному курсу",
                    reply_markup=to_menu
                )
            except:
                pass

        else:
            keyboard = await generate_courses_keyboard(courses_ids_list=courses_ids)
            await bot.edit_message_text(
                chat_id=chat,
                text="<b>Список ваших курсов:</b>",
                parse_mode="html",
                reply_markup=keyboard.add(InlineKeyboardButton(text="Меню", callback_data="menu"))
            )

    elif callback == "get_course":
        await MenuStates.promocode.set()
        try:
            await bot.edit_message_text(
                chat_id=chat,
                text="Чтобы получить доступ к курсам, у вас должен быть промокод, отправьте его нам и по кнопке 'Мои курсы' у вас появятся курсы",
                reply_markup=to_menu
            )
        except:
            pass

    elif callback == "buy_subscription":
        # TODO - генератор клавиатуры с ценами и ниже отслеживать subscription_{price}
        pass

    elif callback == "ask_question":
        await MenuStates.ask_question.set()
        try:
            await bot.edit_message_text(
                chat_id=chat,
                text="Отправьте вопрос, который вас интересует и мы вам ответим в ближайшее время",
                reply_markup=to_menu
            )
        except:
            pass

    if callback[:10] == "choose_bot" or callback == "back_to_bot_settings":
        bot_token = callback.split("_")[2]
        with state.proxy() as data:
            data["bot_token"] = bot_token
        await SettingsStates.settings.set()
        bot_info = await Bot(bot_token).me

        await bot.edit_message_text(
            chat_id=chat,
            message_id=m_id,
            text=f"Настройки бота: @{bot_info.username}",
            reply_markup=bot_settings_mp
        )

    elif callback[:11] == "edit_course":
        mode = callback.split("_")[2]
        async with state.proxy() as data:
            bot_token = data["bot_token"]
        try:
            await bot.edit_message_reply_markup(
                chat_id=chat,
                message_id=m_id,
                reply_markup=back_to_settings
            )
        except:
            pass

        text = "Текст"
        if mode == "name":
            course_name = db.get_course_name(bot_token=bot_token)
            text = f"Введите новое название курса.\nНынешнее название: <br>{course_name}</br>"
            await SettingsStates.course_name.set()
        elif mode == "description":
            course_description = db.get_course_description(bot_token=bot_token)
            text = f"Введите новое описание курса.\nНынешнее описание: <pre>{course_description}</pre>"
            await SettingsStates.course_description.set()
        elif mode == "image":
            text = f"Отправьте в бота новую аватарку курса."
            await SettingsStates.course_image.set()
        try:
            await bot.edit_message_text(
                chat_id=chat,
                text=text,
                message_id=m_id,
                parse_mode="html"
            )
        except:
            pass

    elif callback == "modules_settings":
        async with state.proxy() as data:
            bot_token = data["bot_token"]

        modules_markup = await generate_modules_keyboard(bot_token=bot_token)
        modules_markup.add(
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_to_bot_settings"
            )
        )

        try:
            await bot.edit_message_text(
                text="Выберите модуль, который хотите настроить:",
                chat_id=chat,
                message_id=m_id
            )
        except:
            pass

        try:
            await bot.edit_message_reply_markup(
                chat_id=chat,
                message_id=m_id,
                reply_markup=modules_markup
            )
        except:
            pass

    elif callback == "lessons_settings":
        await bot.edit_message_reply_markup(
            chat_id=chat,
            message_id=m_id,
            reply_markup=lessons_settings_mp
        )

    elif callback[-6:] == "lesson":
        mode = callback.split("_")[0]
        back_to_lessons = InlineKeyboardMarkup()
        if mode == "edit":
            back_to_lessons.add(
                InlineKeyboardButton(
                    text="Оставить нынешнюю настройку",
                    callback_data="lessons_settings"
                )
            )
        back_to_lessons.add(
            InlineKeyboardButton(
                text="Назад",
                callback_data="lessons_settings"
            )
        )

        if mode == "add":
            await SettingsStates.module_name.set()
            await bot.edit_message_text(
                chat_id=chat,
                text="Введите название урока, либо вернитесь назад:",
                reply_markup=back_to_lessons
            )

        elif mode == "edit":
            await bot.edit_message_text(
                chat_id=chat,
                text="Введите название урока, либо вернитесь назад:",
                reply_markup=None
            )