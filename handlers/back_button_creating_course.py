from create_bot import dp, Dispatcher, types, bot
from keyboards import start_keyboards, create_course_keyboards
from aiogram.utils import exceptions
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiohttp, os
from config import TOKEN
from .create_course_handlers import CreateCourseStates, delete_previous_message


# Обработчик для возврата на предыдущий шаг
@dp.callback_query_handler(text='back_to_create', state='*')
async def back_to_create(call: types.CallbackQuery, state: FSMContext):
	await call.answer()
	await delete_previous_message(call)

	# await CreateCourseStates.Name.set()
	await state.reset_state()
	await call.message.edit_text(text="Скорее подбирай или создавай свой курс",
	                             reply_markup=start_keyboards.i_known_keyboard())



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


@dp.callback_query_handler(text='back_to_image_description', state=CreateCourseStates.Description)
async def back_to_name(call: types.CallbackQuery, state: FSMContext):
	print('rewr')
	await call.answer()

	# Восстанавливаем предыдущее состояние
	await delete_previous_message(call)
	try:
		await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 2)
	except exceptions.MessageToDeleteNotFound as e:
		pass
	await call.message.answer("Теперь отправь новое изображение для иллюстрации твоего курса:",
	                          reply_markup=create_course_keyboards.back_to_short_description())


def register_back_creating(dp: Dispatcher):
	dp.register_callback_query_handler(back_to_create, text='back_to_create', state='*')