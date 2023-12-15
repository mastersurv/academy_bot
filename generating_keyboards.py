from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def generate_courses_markup(self, tg_id):
        courses_ids = await self.db.get_courses_ids(tg_id)
        buttons = [
            InlineKeyboardButton(f"Course {course_id}", callback_data=f"course_{course_id}")
            for course_id in courses_ids
        ]
        markup = InlineKeyboardMarkup(*buttons)
        return markup
