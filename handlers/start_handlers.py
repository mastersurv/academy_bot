from aiogram.utils import exceptions
from create_bot import dp, types, Dispatcher, bot
from keyboards import get_base_keyboard, first_look_keyboard, i_known_keyboard
import asyncio


# Создаем асинхронный мьютекс (asyncio.Lock) для синхронизации удаления сообщений
delete_message_lock = asyncio.Lock()


# @dp.message_handler(commands='start')
async def start(message: types.Message):
    await set_default_commands(dp, message.from_user.id)
    await message.answer(text='Welcome to the club body!\n'
                              "https://t.me/xrenator \n"
                              "https://chat.openai.com/",
                         reply_markup=get_base_keyboard())


async def set_default_commands(dp, chat_id: int):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Запуск'),
        types.BotCommand('help', 'Справка о боте'),
        types.BotCommand('education', 'Обучение'),
        types.BotCommand('profile', 'О себе'),
        types.BotCommand('subscribe', 'Проверить подписку'),
        types.BotCommand('ask_question', 'Задать вопрос')
    ], scope=types.BotCommandScopeChat(chat_id), language_code='ru')


@dp.message_handler(text='Я здесь впервые')
async def first_look(message: types.Message):
    keyboard_to_delete = types.ReplyKeyboardRemove()
    async with delete_message_lock:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        except exceptions.MessageToDeleteNotFound as e:
            # Если кнопка уже удалена, то продолжаем выполнение кода
            print(e)
    await message.answer(text="Если есть чем поделиться с людьми, то мы поможем создать  свой собственный курс \n"
                              "\n"
                              "Если хочешь приобрести новые навыки, то поможем выбрать курс",
                         reply_markup=first_look_keyboard())


# @dp.callback_query_handler(text='back_to_start')
async def back_to_start(call: types.CallbackQuery):
    await call.answer()
    async with delete_message_lock:
        try:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
        except exceptions.MessageToDeleteNotFound:
            # Если кнопка уже удалена, то продолжаем выполнение кода
            pass
        try:
            await call.message.delete()
        except exceptions.MessageToDeleteNotFound:
            # Если кнопка уже удалена, то продолжаем выполнение кода
            pass
    await call.message.answer(text='Welcome to the club body!\n'
                                   "https://t.me/xrenator \n"
                                   "https://chat.openai.com/",
                              reply_markup=get_base_keyboard())


# @dp.message_handler(text='Я знаю, что я хочу')
async def i_known(message: types.Message):
    keyboard_to_delete = types.ReplyKeyboardRemove()
    async with delete_message_lock:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        except exceptions.MessageToDeleteNotFound:
            # Если кнопка уже удалена, то продолжаем выполнение кода
            pass
    await message.answer(text="Скорее подбирай или создавай свой курс",
                         reply_markup=i_known_keyboard())


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(first_look, text='Я здесь впервые')
    dp.register_callback_query_handler(back_to_start, text='back_to_start')
    dp.register_message_handler(i_known, text='Я знаю, что я хочу')
