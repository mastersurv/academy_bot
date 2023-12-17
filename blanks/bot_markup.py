from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Библиотека",
        callback_data="library"
    )
).add(
    InlineKeyboardButton(
        text="Получить курс",
        callback_data="get_course"
    )
).add(
    InlineKeyboardButton(
        text="Купить подписку",
        callback_data="buy_subscription"
    )
).add(
    InlineKeyboardButton(
        text="Задать вопрос",
        callback_data="ask_question"
    )
)

to_menu = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Меню",
        callback_data="menu"
    )
)

admin_menu = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Получить курс",
        callback_data="get_course"
    )
).add(
    InlineKeyboardButton(
        text="Создание курсов",
        callback_data="creation_courses"
    )
).add(
    InlineKeyboardButton(
        text="Библиотека",
        callback_data="library"
    )
).add(
    InlineKeyboardButton(
        text="Аналитика курсов",
        callback_data="courses_analytics"
    )
).add(
    InlineKeyboardButton(
        text="Промокоды",
        callback_data="courses_promocodes"
    )
).add(
    InlineKeyboardButton(
        text="Задать вопрос",
        callback_data="ask_question"
    )
)


course_creation = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Созданные курсы",
        callback_data="created_courses"
    )
).add(
    InlineKeyboardButton(
        text="Создать курс",
        callback_data="create_course"
    )
)

to_course_creation = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="К созданию курсов",
        callback_data="creation_courses"
    )
)


back_to_modules = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Назад",
        callback_data="module_settings"
    )
)

back_to_lessons = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Назад",
        callback_data="lesson_settings"
    )
)

bot_settings_mp = (InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Изменить название курса",
        callback_data="edit_course_name"
    )
).add(
    InlineKeyboardButton(
        text="Изменить описание курса",
        callback_data="edit_course_description"
    )
).add(
    InlineKeyboardButton(
        text="Изменить фото курса",
        callback_data="edit_course_image"
    )
).add(
    InlineKeyboardButton(
        text="Настройки модулей",
        callback_data="modules_settings"
    )
).add(
    InlineKeyboardButton(
        text="Добавить модуль",
        callback_data="edit_module"
    )
).add(
    InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_bots_list"
    )
))


modules_settings_mp = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Добавить урок в этот модуль",
        callback_data="add_lesson"
    )
).add(
    InlineKeyboardButton(
        text="Удалить модуль",
        callback_data="delete_module"
    )
).add(
    InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_bot_settings"
    )
)

lessons_settings_mp = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Добавить урок",
        callback_data="add_lesson"
    )
).add(
    InlineKeyboardButton(
        text="Изменить фото урока",
        callback_data="edit_lesson_photo"
    )
).add(
    InlineKeyboardButton(
        text="Удалить урок",
        callback_data="delete_lesson"
    )
)


back_to_settings = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_bot_settings"
    )
)