from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot import MyBot
from utils.db_api.database import Database
from config import bot_token, db_name


bot = Bot(bot_token)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
db = Database(db_name)

my_bot = MyBot(bot=bot, dp=dp, db=db)
my_bot.run()