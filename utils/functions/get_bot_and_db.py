from aiogram import Bot
from utils.db_api.database import Database
from config import bot_token, db_name


def get_bot_and_db():
    bot = Bot(bot_token)
    db = Database(db_name)

    return bot, db