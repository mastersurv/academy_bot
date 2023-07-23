from create_bot import dp, Dispatcher, types, bot
from keyboards.create_course_keyboards import *


@dp.callback_query_handler(text='create_course')
async def creation_start(call: types.CallbackQuery):
	await call.answer()
	await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
	await call.message.edit_text("""
Создание курса - кропотливый процесс, отнесись к этому с повышенным вниманием
Описание форматов возможных курсов
КУРС С ВИДЕО ОФОРМЛЕНИЕМ -...
ЛОНГРИДЫ - это....
КУРСЫ В МОДУЛЬНОМ ФОРМАТЕ, СЕЙЧАС ВЫ ПРИСТУПАЕТЕ К СОЗДАНИЮ ОГЛАВЛЕНИЯ И ПЕРВОГО МОДУЛЯ
""", reply_markup=create_course_kb())


def register_create_course_handlers(dp: Dispatcher):
	dp.register_message_handler(creation_start, text='create_course')
