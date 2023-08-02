import os
from aiogram import Bot, Dispatcher, types
from database import DataBase
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN, db_name, db_user, password_db, db_host, db_port


db = DataBase(db_name, db_user, password_db, db_host, db_port)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
