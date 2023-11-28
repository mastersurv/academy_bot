from aiogram.dispatcher.filters.state import StatesGroup, State


class SettingsStates(StatesGroup):
    add_bot = State()
    settings = State()
