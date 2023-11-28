from aiogram import Bot
from utils.db_api.database import DataBase
from config import TOKEN, db_name, db_user, password_db, db_host, db_port


def get_bot_and_db():
    bot = Bot(TOKEN)
    db = DataBase(db_name, db_user, password_db, db_host, db_port)
    return bot, db