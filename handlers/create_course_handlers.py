from create_bot import dp, Dispatcher, types, bot
from keyboards import start_keyboards, create_course_keyboards
from aiogram.utils import exceptions
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiohttp, os
from config import TOKEN


# Определяем состояния для машины состояний
class CreateCourseStates(StatesGroup):
	Name = State()
	ShortDescription = State()
	ShortDescriptionImage = State()
	Description = State()
	ModuleTitle = State()
	ModuleDescription = State()


# Функция для удаления предыдущего сообщения и восстановления предыдущего состояния
async def delete_previous_message(call: types.CallbackQuery):
	try:
		await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
	except exceptions.MessageToDeleteNotFound:
		pass

	# Восстанавливаем предыдущее состояние
	await CreateCourseStates.previous()


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

	# Проверяем, существует ли папка с таким же названием в папке "courses"
	courses_path = 'courses'  # Путь к папке "courses"
	course_folder_path = os.path.join(courses_path, name)

	if os.path.exists(course_folder_path):
		await message.answer("Папка с таким названием курса уже существует. Пожалуйста, введите другое название курса.")
	else:
		await state.update_data(name=name)

		# Переходим к следующему шагу - вводу краткого описания курса
		await CreateCourseStates.ShortDescription.set()
		await message.answer("Теперь введите краткое описание курса:",
		                     reply_markup=create_course_keyboards.back_to_name_course())


# Обработчик для кнопки "Отмена" или "Заново" на этапе ввода названия курса
@dp.callback_query_handler(text='back_to_name', state=CreateCourseStates.ShortDescription)
async def back_to_name(call: types.CallbackQuery, state: FSMContext):
	await call.answer()

	# Восстанавливаем предыдущее состояние
	await delete_previous_message(call)
	try:
		await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 2)
	except exceptions.MessageToDeleteNotFound as e:
		print(e)
		pass
	await call.message.edit_text("Введи новое название курса:",
	                             reply_markup=create_course_keyboards.back_to_start_create())


# Обработчик для ввода краткого описания курса
@dp.message_handler(state=CreateCourseStates.ShortDescription)
async def enter_short_description(message: types.Message, state: FSMContext):
	# Здесь вы можете сохранить краткое описание курса в базе данных или словаре состояний
	short_description = message.text
	await state.update_data(short_description=short_description)

	# Переходим к следующему шагу - запрос на отправку изображения
	await CreateCourseStates.ShortDescriptionImage.set()
	await message.answer("Теперь отправь изображение для иллюстрации твоего курса:",
	                     reply_markup=create_course_keyboards.back_to_short_description())


# Обработчик для кнопки "Отмена" или "Заново" на этапе ввода краткого описания курса
@dp.callback_query_handler(text='back_to_short_description', state=CreateCourseStates.ShortDescriptionImage)
async def back_to_name(call: types.CallbackQuery, state: FSMContext):
	await call.answer()

	# Восстанавливаем предыдущее состояние
	await delete_previous_message(call)
	try:
		await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 2)
	except exceptions.MessageToDeleteNotFound as e:
		pass
	await call.message.edit_text("Введи новое краткое описание курса:",
	                             reply_markup=create_course_keyboards.back_to_name_course())


@dp.message_handler(content_types=types.ContentTypes.PHOTO | types.ContentTypes.VIDEO,
                    state=CreateCourseStates.ShortDescriptionImage)
async def enter_short_description_image(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		course_name = data['name']

	# Получите информацию о файле
	file = message.photo[-1] if message.photo else message.video
	file_info = await bot.get_file(file.file_id)
	file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'  # Замените BOT_TOKEN на ваш токен

	# Создайте путь для сохранения изображения
	save_path = os.path.join('courses', course_name)
	if not os.path.exists(save_path):
		os.makedirs(save_path)
	else:
		# Если папка уже существует, отправляем сообщение пользователю
		await message.answer("Папка для сохранения изображения уже существует.")

	# Получите расширение файла из URL
	file_extension = file_info.file_path.split('.')[-1]

	# Скачайте файл и сохраните его в нужной папке
	async with aiohttp.ClientSession() as session:
		async with session.get(file_url) as response:
			if response.status == 200:
				file_data = await response.read()
				file_name = f'short_description_image.{file_extension}'
				file_path = os.path.join(save_path, file_name)

				with open(file_path, 'wb') as f:
					f.write(file_data)

				# Сохраните путь к файлу в состоянии
				await state.update_data(short_description_image=file_path)

				# Переходите к следующему шагу - вводу полного описания курса
				await CreateCourseStates.Description.set()
				await message.answer("Теперь введите описание курса:")
			else:
				await message.answer("Не удалось скачать изображение.")


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
	print(data)
	# Здесь вы можете сохранить данные в базе данных вместо словаря состояний
	# data содержит все введенные пользователем данные: name, description, module_title, module_description и другие
	# Например, можно воспользоваться библиотекой PostgreSQL для сохранения данных в базе данных

	# Очищаем состояние, чтобы пользователь мог начать создание нового курса
	await state.finish()

	await message.answer("Создание курса завершено. Спасибо за участие!",
	                     reply_markup=start_keyboards.i_known_keyboard())


# --------------------- Добавление в базу данных курсов, модулей и шагов ---------------------
# async def insert_course(self, name, short_description, short_description_image, description):
#     query = "INSERT INTO courses (name, short_description, short_description_image, description) VALUES ($1, $2, $3, $4) RETURNING course_id;"
#     result = await self.execute_query(query, name, short_description, short_description_image, description)
#     return result[0]['course_id']
#
# async def insert_module(self, course_id, module_title, module_description):
#     query = "INSERT INTO modules (course_id, module_title, module_description) VALUES ($1, $2, $3) RETURNING module_id;"
#     result = await self.execute_query(query, course_id, module_title, module_description)
#     return result[0]['module_id']
#
# async def insert_step(self, module_id, step_title, step_description):
#     query = "INSERT INTO steps (module_id, step_title, step_description) VALUES ($1, $2, $3) RETURNING step_id;"
#     result = await self.execute_query(query, module_id, step_title, step_description)
#     return result[0]['step_id']

# TODO Добавить обработчик для добавление шага в модуле

def register_create_course_handlers(dp: Dispatcher):
	dp.register_callback_query_handler(creation_start, text='create_course', state='*')
	dp.register_callback_query_handler(back_to_create, text='back_to_create', state='*')
	dp.register_callback_query_handler(start_create, text='start_create', state='*')
	dp.register_message_handler(enter_name, state=CreateCourseStates.Name)
	dp.register_message_handler(enter_description, state=CreateCourseStates.Description)
	dp.register_message_handler(enter_module_title, state=CreateCourseStates.ModuleTitle)
	dp.register_message_handler(enter_module_description, state=CreateCourseStates.ModuleDescription)
