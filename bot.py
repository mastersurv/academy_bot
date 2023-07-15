from aiogram import executor, types
import logging
from create_bot import dp, bot  # , db
# from handlers import start_handlers


logging.basicConfig(level=logging.INFO)


# Регистрация хэндлеров start_handlers
# start_handlers.register_start_handlers(dp)


async def on_startup(dp):
	await bot.send_message(633496059, 'Бот запущен')
	await bot.send_message(1087245469, 'Бот запущен')


if __name__ == "__main__":
	# Создаем необходимые таблицы
	# db.create_tables()
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
