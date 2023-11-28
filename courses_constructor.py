from aiogram import Bot, Dispatcher, executor
from utils.db_api.database import Database

from aiogram.types import Message
from aiogram.dispatcher.dispatcher import FSMContext

from handlers.callback_handler import callback_handler


class MyBot:
    def __init__(self, bot: Bot, dp: Dispatcher, db: Database):
        self.bot = bot
        self.dp = dp
        self.db = db

    async def start_handler(self, message: Message, state: FSMContext):
        chat = message.chat.id
        tg_id = message.from_user.id

    def register_handlers(self):
        self.dp.register_message_handler(callback=self.start_handler, commands=["start"], state="*")
        self.dp.register_callback_query_handler(callback=callback_handler, state="*")

    def run(self):
        self.register_handlers()
        executor.start_polling(dispatcher=self.dp, skip_updates=True)