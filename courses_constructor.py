from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardButton
from utils.db_api.database import DataBase

from aiogram.types import Message
from aiogram.dispatcher.dispatcher import FSMContext

from blanks.bot_markup import menu, admin_menu

from handlers.constructor_callback_handler import constructor_callback_handler

from states_handlers.states import SettingsStates, MenuStates
from states_handlers.get_promocode_handler import get_promocode_handler

from course_creation_handlers.edit_course_name import edit_course_name
from course_creation_handlers.edit_course_description import edit_course_description
from course_creation_handlers.edit_course_image import edit_course_image

from config import channel_id, group_id


class MyBot:
    def __init__(self, bot: Bot, dp: Dispatcher, db: DataBase):
        self.bot = bot
        self.dp = dp
        self.db = db

    async def start_handler(self, message: Message, state: FSMContext):
        chat = message.chat.id
        tg_id = message.from_user.id
        username = message.from_user.username

        users = self.db.get_users_ids()
        keyboard = menu

        creators_ids = await self.db.get_creators_ids()
        if tg_id in creators_ids:
            keyboard = admin_menu

        await self.bot.send_message(
            chat_id=chat,
            text="Добро пожаловать в нашего бота!",
        )

        await self.bot.send_message(
            chat_id=chat,
            text="<b>Меню</b>",
            parse_mode="html",
            reply_markup=keyboard
        )

        if tg_id not in users:
            try:
                await self.dp.bot.send_message(
                    chat_id=channel_id, text=f"Чат с пользователем @{username}",
                )

                reply_message = await self.dp.bot.send_message(
                    chat_id=group_id,
                    text="Новый чат",
                )
                await self.db.add_user_post(tg_id=tg_id, post_id=reply_message.message_id + 1)

            except Exception as e:
                print(e)

    async def text_handler(self, message: Message, state: FSMContext):
        tg_id = message.from_user.id
        m_id = message.message_id
        chat_type = message.chat.type
        if chat_type == "supergroup":
            try:
                if message.sender_chat is None or message.sender_chat.type != "channel":
                    await self.dp.bot.copy_message(
                        from_chat_id=message.chat.id,
                        message_id=message.message_id,
                        chat_id=await self.db.get_message_or_user(
                            id=True,
                            message_id=message.reply_to_message.message_id,
                        )
                    )
            except Exception:
                pass

        elif chat_type == "private":
            try:
                message_to_chat = await self.dp.bot.copy_message(
                    chat_id=group_id,
                    from_chat_id=tg_id,
                    message_id=m_id,
                    reply_to_message_id=await self.db.get_post_id(tg_id=tg_id)
                )
                await self.db.add_user_message(tg_id=tg_id, message_id=message_to_chat.message_id)

            except Exception as e:
                pass

    def register_handlers(self):
        self.dp.register_message_handler(callback=self.start_handler, commands=["start"], state="*")
        self.dp.register_callback_query_handler(callback=constructor_callback_handler, state="*")

        self.dp.register_message_handler(callback=get_promocode_handler, content_types=["text"], state=MenuStates.promocode)

        self.dp.register_message_handler(callback=edit_course_name, state=SettingsStates.course_name, content_types=["text"])
        self.dp.register_message_handler(callback=edit_course_description, state=SettingsStates.course_description, content_types=["text"])
        self.dp.register_message_handler(callback=edit_course_image, state=SettingsStates.course_image, content_types=["photo"])

        self.dp.register_message_handler(callback=self.text_handler, state="*", content_types=["photo"])

    def run(self):
        self.register_handlers()
        executor.start_polling(dispatcher=self.dp, skip_updates=True)