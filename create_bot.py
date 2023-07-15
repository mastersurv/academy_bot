import os
from aiogram import Bot, Dispatcher, types
# from database import DataBase
from aiogram.contrib.fsm_storage.memory import MemoryStorage


TOKEN = os.getenv('TOKEN')
# db = DataBase('academy.db')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())