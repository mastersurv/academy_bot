from aiogram import Bot, Dispatcher
from aiogram.types import ContentTypes, Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import BotBlocked

from utils.db_api.database import DataBase
from utils.db_api.funnel_db import FunnelDatabase
from markups.admin_markup import admin_markup
from markups.back_markups import back_to_admin_markup

from handlers.bot_states import BotStates, FunnelStates
from aiogram.utils.exceptions import BadRequest
from datetime import datetime
from utils.usefull_functions.sending_message import sending_function
from utils.usefull_functions.send_message_ids import send_message_ids
from utils.usefull_functions.create_markup import create_markup
from utils.usefull_functions.files_names import files_names
from utils.usefull_functions.files_ids import files_ids


class ChildBot:
    def __init__(self, token: str, database_name: str):
        memory = MemoryStorage()
        self.bot_token = token
        self.bot = Bot(token=token)
        self.dp = Dispatcher(self.bot, storage=memory)
        self.db = DataBase(db_name=database_name)

        self.chat_link = self.db.get_chat_link(bot_token=self.bot_token)
        self.group_id = self.db.get_group_id(bot_token=self.bot_token)

    async def start_handler(self, message: Message, state: FSMContext):
        tg_id = message.from_user.id

        start_text = await self.db.get_start_text(bot_token=self.bot_token)

        await self.bot.send_message(
            chat_id=tg_id,
            text=start_text
        )



