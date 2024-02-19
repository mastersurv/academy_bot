import asyncio
from child_bot import ChildBot
from utils.db_api.database import DataBase
import aioschedule

used_tokens = []


def bot_init(event_loop, token):
    try:
        bot = ChildBot(token=token, database_name="courses.db")
    except Exception:
        pass

    try:
        bot.run(event_loop)
    except RuntimeError:
        pass
    except TypeError:
        pass
    except Exception:
        pass


async def scheduler():
    try:
        aioschedule.every(1).minutes.do(starting_bots)
    except TypeError:
        pass

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main_schedule():
    try:
        await asyncio.create_task(scheduler())
    except TypeError:
        pass


async def starting_bots():
    global event_loop
    db = DataBase(db_name="comments.db")
    tokens = db.get_tokens()
    # print(tokens)

    if tokens is not None:
        for token in tokens:
            if token not in used_tokens:
                used_tokens.append(token)
                bot_init(event_loop, token)


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    while True:
        event_loop.run_until_complete(starting_bots())


