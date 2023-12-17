from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def generate_lessons_settings_keyboard(course_id: int, module_id: int, lesson_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            text="Изменить название урока",
            callback_data=f"edit_lesson_name_{course_id}_{module_id}_{lesson_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Изменить описание урока",
            callback_data=f"edit_lesson_description_{course_id}_{module_id}_{lesson_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Изменить материал урока",
            callback_data=f"edit_lesson_material_{course_id}_{module_id}_{lesson_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Посмотреть демо урока (как будет выглядеть для пользователя)",
            callback_data=f"check_demo_lesson_{course_id}_{module_id}_{lesson_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="К списку уроков",
            callback_data=f"created_lessons_{course_id}_{module_id}"
        )
    )

    return keyboard