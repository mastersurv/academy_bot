from create_bot import dp, Dispatcher, types
from keyboards.create_course_keyboards import *


# @dp.callback_query_handler(text='create_course')
# async def creation_start(call: types.CallbackQuery):
# 	await call.answer()
# 	await call.message.answer("""
# Создание курса - кропотливый процесс, отнесись к этому с повышенным вниманием
# Описание форматов возможных курсов
# КУРС С ВИДЕО ОФОРМЛЕНИЕМ -...
# ЛОНГРИДЫ - это....
# КУРСЫ В МОДУЛЬНОМ ФОРМАТЕ, СЕЙЧАС ВЫ ПРИСТУПАЕТЕ К СОЗДАНИЮ ОГЛАВЛЕНИЯ И ПЕРВОГО МОДУЛЯ
# """, reply_markup=create_course_kb())


@dp.message_handler(text='create_course')
async def creation_start(message: types.Message):
	await message.answer("""
Создание курса - кропотливый процесс, отнесись к этому с повышенным вниманием
Описание форматов возможных курсов
КУРС С ВИДЕО ОФОРМЛЕНИЕМ -...
ЛОНГРИДЫ - это....
КУРСЫ В МОДУЛЬНОМ ФОРМАТЕ, СЕЙЧАС ВЫ ПРИСТУПАЕТЕ К СОЗДАНИЮ ОГЛАВЛЕНИЯ И ПЕРВОГО МОДУЛЯ
""", reply_markup=create_course_kb())


def register_create_course_handlers(dp: Dispatcher):
	dp.register_message_handler(creation_start, text='create_course')
