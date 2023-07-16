from create_bot import dp, types, Dispatcher
from keyboards import get_base_keyboard


# @dp.message_handler(commands='start')
async def start(message: types.Message):
    await set_default_commands(dp, message.from_user.id)
    await message.answer(text='Welcome to the club body!\n'
                              "https://t.me/xrenator \n"
                              "https://chat.openai.com/",
                         reply_markup=get_base_keyboard())


async def set_default_commands(dp, chat_id: int):
    await dp.bot.set_my_commands([
        # types.BotCommand('ОБУЧЕНИЕ', 'Начать сначала'),
        # types.BotCommand('ПРОФИЛЬ', 'Справка о боте'),
        # types.BotCommand('ПОДПИСКА', 'Справка о боте'),
        # types.BotCommand('ЗАДАТЬ_ВОПРОС', 'Справка о боте'),
        types.BotCommand('start', 'Справка о боте'),
        types.BotCommand('help', 'Справка о боте')
    ], scope=types.BotCommandScopeChat(chat_id), language_code='ru')


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
