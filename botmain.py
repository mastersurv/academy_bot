from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from courses_constructor import MyBot
from utils.db_api.database import DataBase
from config import TOKEN, db_name, db_user, password_db, db_host, db_port


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
db = DataBase(db_name, db_user, password_db, db_host, db_port)

my_bot = MyBot(bot=bot, dp=dp, db=db)
my_bot.run()