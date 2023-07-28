from create_bot import dp, Dispatcher, types, bot
from keyboards import start_keyboards, create_course_keyboards
from aiogram.utils import exceptions
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


# Определяем состояния для машины состояний
class CreateCourseStates(StatesGroup):
	Name = State()
	Description = State()
	ModuleTitle = State()
	ModuleDescription = State()


# Вспомогательная функция для удаления сообщения
async def delete_previous_message(call: types.CallbackQuery):
	try:
		await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
	except exceptions.MessageToDeleteNotFound:
		pass


# Обработчик для начала процесса создания курса
@dp.callback_query_handler(text='create_course', state='*')
async def creation_start(call: types.CallbackQuery, state: FSMContext):
	await call.answer()
	await delete_previous_message(call)

	# Переходим в состояние Name, чтобы пользователь мог ввести название курса
	# await CreateCourseStates.Name.set()
	await call.message.edit_text("""
    Создание курса - кропотливый процесс, отнесись к этому с повышенным вниманием
    Описание форматов возможных курсов
    КУРС С ВИДЕО ОФОРМЛЕНИЕМ -...
    ЛОНГРИДЫ - это....
    КУРСЫ В МОДУЛЬНОМ ФОРМАТЕ, СЕЙЧАС ВЫ ПРИСТУПАЕТЕ К СОЗДАНИЮ ОГЛАВЛЕНИЯ И ПЕРВОГО МОДУЛЯ
    """, reply_markup=create_course_keyboards.create_course_kb())


# Обработчик для возврата на предыдущий шаг
@dp.callback_query_handler(text='back_to_create', state='*')
async def back_to_create(call: types.CallbackQuery, state: FSMContext):
	await call.answer()
	await delete_previous_message(call)

	# await CreateCourseStates.Name.set()
	await state.reset_state()
	await call.message.edit_text(text="Скорее подбирай или создавай свой курс",
	                             reply_markup=start_keyboards.i_known_keyboard())


# Обработчик для начала создания курса
@dp.callback_query_handler(text='start_create', state='*')
async def start_create(call: types.CallbackQuery, state: FSMContext):
	await call.answer()
	await delete_previous_message(call)

	# Переходим в состояние Name, чтобы пользователь мог ввести название курса
	await CreateCourseStates.Name.set()
	await call.message.edit_text("Введи название курса:", reply_markup=create_course_keyboards.back_to_start_create())


# Обработчик для ввода названия курса
@dp.message_handler(state=CreateCourseStates.Name)
async def enter_name(message: types.Message, state: FSMContext):
	# Здесь вы можете сохранить название курса в базе данных или словаре состояний
	name = message.text
	await state.update_data(name=name)

	# Переходим к следующему шагу - вводу описания курса
	await CreateCourseStates.Description.set()
	await message.answer("Теперь введи описание курса:")


# Обработчик для ввода описания курса
@dp.message_handler(state=CreateCourseStates.Description)
async def enter_description(message: types.Message, state: FSMContext):
	# Здесь вы можете сохранить описание курса в базе данных или словаре состояний
	description = message.text
	await state.update_data(description=description)

	# Переходим к следующему шагу - вводу названия модуля
	await CreateCourseStates.ModuleTitle.set()
	await message.answer("Теперь введи название первого модуля:")


# Обработчик для ввода названия модуля
@dp.message_handler(state=CreateCourseStates.ModuleTitle)
async def enter_module_title(message: types.Message, state: FSMContext):
	# Здесь вы можете сохранить название модуля в базе данных или словаре состояний
	module_title = message.text
	await state.update_data(module_title=module_title)

	# Переходим к следующему шагу - вводу описания модуля
	await CreateCourseStates.ModuleDescription.set()
	await message.answer("Теперь введи описание первого модуля:")


# Обработчик для ввода описания модуля
@dp.message_handler(state=CreateCourseStates.ModuleDescription)
async def enter_module_description(message: types.Message, state: FSMContext):
	# Здесь вы можете сохранить описание модуля в базе данных или словаре состояний
	module_description = message.text
	await state.update_data(module_description=module_description)

	# Завершаем процесс создания курса и переходим в исходное состояние
	data = await state.get_data()
	# Здесь вы можете сохранить данные в базе данных вместо словаря состояний
	# data содержит все введенные пользователем данные: name, description, module_title, module_description и другие
	# Например, можно воспользоваться библиотекой PostgreSQL для сохранения данных в базе данных

	# Очищаем состояние, чтобы пользователь мог начать создание нового курса
	await state.finish()

	await message.answer("Создание курса завершено. Спасибо за участие!",
	                     reply_markup=start_keyboards.i_known_keyboard())


def register_create_course_handlers(dp: Dispatcher):
	dp.callback_query_handler(creation_start, text='create_course', state='*')
	dp.callback_query_handler(back_to_create, text='back_to_create', state='*')
	dp.callback_query_handler(start_create, text='start_create', state='*')
	dp.register_message_handler(enter_name, state=CreateCourseStates.Name)
	dp.register_message_handler(enter_description, state=CreateCourseStates.Description)
	dp.register_message_handler(enter_module_title, state=CreateCourseStates.ModuleTitle)
	dp.register_message_handler(enter_module_description, state=CreateCourseStates.ModuleDescription)
