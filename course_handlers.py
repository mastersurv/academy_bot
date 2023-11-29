from create_bot import dp, types, Dispatcher
from course_keyboards import generate_courses_keyboard, generate_modules_keyboard


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
	await message.answer("Выберите курс:", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith='course_')
async def handle_course_button(call: types.CallbackQuery):
	await call.answer()
	course_id = call.data.split('_')[1]

	# Код для получения описания курса по course_id из базы данных
	# Например: description = get_course_description(course_id)
	description = f"Описание курса {course_id}"
	modules_keyboard = await generate_modules_keyboard(int(course_id))
	await call.message.edit_text(text=description, reply_markup=modules_keyboard)


# Кнопка назад (Выбор курса)
@dp.callback_query_handler(text='back_courses')
async def back_courses(call: types.CallbackQuery):
	await call.answer()
	keyboard = await generate_courses_keyboard()
	await call.message.edit_text("Выберите курс:", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith='module_')
async def handle_module_button(call: types.CallbackQuery):
	await call.answer()
	module_id = call.data.split('_')[1]

	# Код для получения информации о модуле по module_id из базы данных
	# Например: module_info = get_module_info(module_id)
	module_info = f"Информация о модуле {module_id}"

	await call.message.edit_text(text=module_info)


def register_course_handlers(dp: Dispatcher):
	dp.register_message_handler(start, commands='start')
