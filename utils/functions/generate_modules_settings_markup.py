from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def generate_modules_settings_keyboard(course_id: int, module_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            text="Изменить название модуля",
            callback_data=f"edit_module_name_{course_id}_{module_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Изменить описание модуля",
            callback_data=f"edit_module_description_{course_id}_{module_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Изменить фото модуля",
            callback_data=f"edit_module_image_{course_id}_{module_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Посмотреть демо модуля (как будет выглядеть для пользователя)",
            callback_data=f"check_demo_module_{course_id}_{module_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Добавить урок в этот модуль",
            callback_data=f"add_lesson_{course_id}_{module_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Настройки уроков",
            callback_data=f"lessons_settings_{course_id}_{module_id}"
        )
    ).add(
        InlineKeyboardButton(
            text="Назад",
            callback_data=f"created_modules_{course_id}"
        )
    )

    return keyboard