from utils.functions.get_bot_and_db import get_bot_and_db


# TODO write function - generate_promocode
async def generate_promocode() -> str:
    bot, db = get_bot_and_db()
    promocodes = await db.promocodes()
    return ""