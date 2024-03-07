from aiogram.dispatcher.filters.state import StatesGroup, State


class MenuStates(StatesGroup):
    promocode = State()
    n_promo = State()
    group_promo = State()
    ask_question = State()

    button_post = State()

class SettingsStates(StatesGroup):
    create_course = State()
    settings = State()

    course_name = State()
    course_description = State()
    course_image = State()
    final_message = State()

    module_name = State()
    module_description = State()
    module_image = State()

    lesson_name = State()
    lesson_description = State()
    lesson_material = State()

    test_question = State()
    test_keyboard = State()