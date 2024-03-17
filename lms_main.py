from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

from courses_constructor import MyBot
from utils.db_api.database import DataBase
from config import TOKEN, db_name


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
db = DataBase(db_name)
loop = asyncio.get_event_loop()
loop.run_until_complete(db.create_tables())

my_bot = MyBot(bot=bot, dp=dp, db=db)
my_bot.run()