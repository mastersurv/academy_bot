from create_bot import dp, Dispatcher, types, bot
from keyboards import start_keyboards, create_course_keyboards
from aiogram.utils import exceptions


@dp.callback_query_handler(text='create_course')
async def creation_start(call: types.CallbackQuery):
	await call.answer()
	try:
		await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
	except exceptions.MessageToDeleteNotFound:
		# Если кнопка уже удалена, то продолжаем выполнение кода

		pass
	await call.message.edit_text("""
Создание курса - кропотливый процесс, отнесись к этому с повышенным вниманием
Описание форматов возможных курсов
КУРС С ВИДЕО ОФОРМЛЕНИЕМ -...
ЛОНГРИДЫ - это....
КУРСЫ В МОДУЛЬНОМ ФОРМАТЕ, СЕЙЧАС ВЫ ПРИСТУПАЕТЕ К СОЗДАНИЮ ОГЛАВЛЕНИЯ И ПЕРВОГО МОДУЛЯ
""", reply_markup=create_course_keyboards.create_course_kb())


@dp.callback_query_handler(text='back_to_create')
async def back_to_create(call: types.CallbackQuery):
	await call.answer()
	await call.message.edit_text(text="Скорее подбирай или создавай свой курс",
	                             reply_markup=start_keyboards.i_known_keyboard())


def register_create_course_handlers(dp: Dispatcher):
	dp.register_message_handler(creation_start, text='create_course')
	dp.register_message_handler(back_to_create, text='back_to_create')
