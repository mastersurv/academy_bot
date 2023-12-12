from aiogram.dispatcher.filters.state import StatesGroup, State


class MenuStates(StatesGroup):
    promocode = State()
    ask_question = State()


class SettingsStates(StatesGroup):
    add_bot = State()
    settings = State()

    course_name = State()
    course_description = State()
    course_image = State()

    module_name = State()
    module_description = State()
    module_blob = State()

    lesson_name = State()
    lesson_description = State()
    lesson_blob = State()
