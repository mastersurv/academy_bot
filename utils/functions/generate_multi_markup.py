from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.functions.get_bot_and_db import get_bot_and_db


async def generate_multi_keyboard(course_id=None, module_id=None, lesson_id=None, test_id=None, answer=None):
    bot, db = get_bot_and_db()
    keyboard = InlineKeyboardMarkup()

    if answer:
        # Возвращаем только кнопку "Далее"
        return [("Далее", f"question_{test_id + 1}")]

    if test_id is not None:
        # Клавиатура для теста
        keyboard.add(
            InlineKeyboardButton(
                text="Следующий вопрос",
                callback_data=f"question_{test_id + 1}"
            )
        ).add(
            InlineKeyboardButton(
                text="Назад",
                callback_data=f"back_to_lesson_{lesson_id}"
            )
        )

    elif lesson_id is not None:
        # Клавиатура для урока
        has_next_lesson = await db.check_next_lesson(course_id, module_id, lesson_id)
        has_next_module = await db.check_next_module(course_id, module_id)

        if has_next_lesson:
            next_lesson_id = await db.get_next_lesson_in_module(course_id, module_id, lesson_id)
            if next_lesson_id:
                keyboard.add(
                    InlineKeyboardButton(
                        text="Следующий урок",
                        callback_data=f"lesson_{module_id}_{next_lesson_id}"
                    )
                )
        elif has_next_module:
            next_module_id = await db.get_next_module(course_id, module_id)
            if next_module_id:
                keyboard.add(
                    InlineKeyboardButton(
                        text="Следующий модуль",
                        callback_data=f"module_{course_id}_{next_module_id}"
                    )
                )
        keyboard.add(
            InlineKeyboardButton(
                text="Назад",
                callback_data=f"module_{course_id}_{module_id}"
            )
        )

    elif module_id is not None:
        # Клавиатура для модуля
        has_next_module = await db.check_next_module(course_id, module_id)
        if has_next_module:
            next_module_id = await db.get_next_module(course_id, module_id)
            if next_module_id:
                keyboard.add(
                    InlineKeyboardButton(
                        text="Следующий модуль",
                        callback_data=f"module_{course_id}_{next_module_id}"
                    )
                )
        keyboard.add(
            InlineKeyboardButton(
                text="Назад",
                callback_data=f"course_{course_id}"
            )
        )

    elif course_id is not None:
        # Клавиатура для курса
        keyboard.add(
            InlineKeyboardButton(
                text="Начать курс",
                callback_data=f"course_{course_id}"
            )
        )

    return keyboard
