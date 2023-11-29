from aiogram import executor, types
import logging
from create_bot import dp, bot, db
from course_handlers import register_course_handlers


logging.basicConfig(level=logging.INFO)

# Регистрация хэндлеров start_handlers
register_course_handlers(dp)


async def on_startup(dp):
	await bot.send_message(633496059, 'Бот запущен')
	# await bot.send_message(1087245469, 'Бот запущен')
	await db.create_tables()



if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
