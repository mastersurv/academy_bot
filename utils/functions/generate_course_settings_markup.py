from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def generate_courses_settings_keyboard(course_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            text="Изменить название курса",
            callback_data=f"edit_course_name_{course_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Изменить описание курса",
            callback_data=f"edit_course_description_{course_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Изменить фото курса",
            callback_data=f"edit_course_image_{course_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Посмотреть демо курса",
            callback_data=f"check_demo_course_{course_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Финальное сообщение",
            callback_data=f"edit_final_message_{course_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Получить статистику по курсу",
            callback_data=f"get_course_statistics_{course_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Добавить модуль 🎯",
            callback_data=f"add_module_{course_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Настройки модулей",
            callback_data=f"created_modules_{course_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Удалить курс",
            callback_data=f"delete_course_{course_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Назад",
            callback_data="created_courses"
        )
    )

    return keyboard