from create_bot import dp, types, Dispatcher, bot
from course_keyboards import generate_courses_keyboard
import asyncio


async def set_default_commands(dp: Dispatcher, chat_id: int):
	await dp.bot.set_my_commands([
		types.BotCommand('start', 'Запуск'),
		types.BotCommand('help', 'Справка о боте'),
		types.BotCommand('analytics', 'Аналитика'),
		types.BotCommand('my_bots', 'О себе'),
		types.BotCommand('ask_question', 'Задать вопрос')
	], scope=types.BotCommandScopeChat(chat_id), language_code='ru')


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	await set_default_commands(dp, message.from_user.id)
	keyboard = await generate_courses_keyboard()
	text = "Выберите курс:"
	await message.answer(text, reply_markup=keyboard)


# Обработчик для inline-кнопок
@dp.callback_query_handler(text_startswith='course_')
async def handle_inline_button(call: types.CallbackQuery):
	# Обработка нажатия на inline-кнопку
	await call.answer()
	course_id = call.data.split('_')[1]

	# Код для получения описания курса по course_id из базы данных
	# Например: description = get_course_description(course_id)
	description = f"Описание курса {course_id}"

	await call.message.edit_text(text=description)






def register_course_handlers(dp: Dispatcher):
	dp.register_message_handler(start, commands='start')
