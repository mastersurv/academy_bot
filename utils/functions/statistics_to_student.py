from utils.functions.get_bot_and_db import get_bot_and_db


async def statistics_to_student(tg_id: int):
    bot, db = get_bot_and_db()

    courses_ids = await db.get_created_courses_ids(tg_id=tg_id)
