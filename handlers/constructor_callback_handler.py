from aiogram.types import CallbackQuery
from aiogram.dispatcher.dispatcher import FSMContext

from utils.functions.get_bot_and_db import get_bot_and_db
from states_handlers.states import SettingsStates


async def constructor_callback_handler(call: CallbackQuery, state: FSMContext):
    bot, db = get_bot_and_db()
    chat = call.message.chat.id
    callback = call.data

    if callback[:8] == "settings":
        await SettingsStates.settings.set()
        bot_token = callback.split("_")[1]
        async with state.proxy() as data:
            data["bot_token"] = bot_token

