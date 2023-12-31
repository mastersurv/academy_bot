from aiogram import executor, types
import logging
from create_bot import dp, bot, db
from handlers import register_start_handlers, register_create_course_handlers, register_back_creating


logging.basicConfig(level=logging.INFO)


# Регистрация хэндлеров start_handlers
register_start_handlers(dp)

# Регистрация хэндлеров create_course_handlers
register_create_course_handlers(dp)

# Регистрация хэндлеров back_button_creating_course
register_back_creating(dp)


async def on_startup(dp):
	await bot.send_message(633496059, 'Бот запущен')
	# await bot.send_message(1087245469, 'Бот запущен')
	await db.create_tables()


if __name__ == "__main__":
	# Создаем необходимые таблицы
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
