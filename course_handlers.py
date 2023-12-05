from create_bot import dp, types, Dispatcher
from course_keyboards import generate_courses_keyboard, generate_modules_keyboard, generate_lessons_keyboard
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class CourseStates(StatesGroup):
	Courses = State()
	Modules = State()
	Lessons = State()


async def set_default_commands(dp: Dispatcher, chat_id: int):
	await dp.bot.set_my_commands([
		types.BotCommand('start', 'Запуск'),
		types.BotCommand('help', 'Справка о боте'),
		types.BotCommand('analytics', 'Аналитика'),
		types.BotCommand('my_bots', 'О себе'),
		types.BotCommand('ask_question', 'Задать вопрос')
	], scope=types.BotCommandScopeChat(chat_id), language_code='ru')


# Обработчик команды /start
@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
	await set_default_commands(dp, message.from_user.id)
	await CourseStates.Courses.set()
	keyboard = await generate_courses_keyboard()
	await message.answer("Выберите курс:", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith='course_', state=CourseStates.Courses)
async def handle_course_button(call: types.CallbackQuery, state: FSMContext):
	await call.answer()
	course_id = call.data.split('_')[1]
	async with state.proxy() as data:
		data['course_id'] = course_id

	# Код для получения описания курса по course_id из базы данных
	# Например: description = get_course_description(course_id)
	description = f"Описание курса {course_id}"
	modules_keyboard = await generate_modules_keyboard(int(course_id))
	await CourseStates.Modules.set()
	await call.message.edit_text(text=description, reply_markup=modules_keyboard)


# Кнопка назад (Выбор курса)
@dp.callback_query_handler(text='back_courses', state=CourseStates.Modules)
async def back_courses(call: types.CallbackQuery, state: FSMContext):
	await call.answer()
	keyboard = await generate_courses_keyboard()
	await CourseStates.previous()
	await call.message.edit_text("Выберите курс:", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith='module_', state=CourseStates.Modules)
async def handle_module_button(call: types.CallbackQuery, state: FSMContext):
	await call.answer()
	module_id = call.data.split('_')[1]
	async with state.proxy() as data:
		data['module_id'] = module_id
		course_id = data['course_id']

	# Код для получения информации о модуле по module_id из базы данных
	# Например: module_info = get_module_info(module_id)
	module_info = f"Информация о модуле {module_id}"
	lesson_keyboard = await generate_lessons_keyboard(course_id, int(module_id))

	await call.message.edit_text(text=module_info, reply_markup=lesson_keyboard)


@dp.callback_query_handler(text_startswith='lesson_')
async def handle_lesson_button(call: types.CallbackQuery, state: FSMContext):
	await call.answer()
	lesson_id = call.data.split('_')[1]

	# Код для получения информации о модуле по lesson_id из базы данных
	# Например: module_info = get_module_info(lesson_id)
	lesson_info = f"Информация о уроке {lesson_id}"

	await call.message.edit_text(text=lesson_info)


def register_course_handlers(dp: Dispatcher):
	dp.register_message_handler(start, commands='start')
