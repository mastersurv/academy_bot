from aiogram import Bot, Dispatcher, executor
from utils.db_api.database import DataBase

from aiogram.types import Message
from aiogram.dispatcher.dispatcher import FSMContext

from handlers.constructor_callback_handler import constructor_callback_handler


class MyBot:
    def __init__(self, bot: Bot, dp: Dispatcher, db: DataBase):
        self.bot = bot
        self.dp = dp
        self.db = db

    async def start_handler(self, message: Message, state: FSMContext):
        chat = message.chat.id
        tg_id = message.from_user.id

    def register_handlers(self):
        self.dp.register_message_handler(callback=self.start_handler, commands=["start"], state="*")
        self.dp.register_callback_query_handler(callback=constructor_callback_handler, state="*")

    def run(self):
        self.register_handlers()
        executor.start_polling(dispatcher=self.dp, skip_updates=True)