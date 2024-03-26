from utils.functions.get_bot_and_db import get_bot_and_db
from xlsxwriter import Workbook
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.functions.statistics_from_course import statistics_to_creator
from datetime import datetime


async def statistics_to_course(tg_id: int, course_id: int):
    bot, db = get_bot_and_db()

    users_ids = await db.get_course_users_ids(course_id=course_id)
    usernames_students = await db.get_usernames_course_users(course_id=course_id)
    course_name = await db.get_course_name(course_id=course_id)
    excel = Workbook(f"Статистика курса {course_name}.xlsx")
    worksheet = excel.add_worksheet()

    row = 0
    worksheet.write(row, 0, "username")
    worksheet.write(row, 1, "Статус прохождения")
    worksheet.write(row, 2, "Количество правильных ответов")
    worksheet.write(row, 3, "количество неверных ответов")
    worksheet.write(row, 4, "Время прохождения (мин)")

    print(usernames_students)
    username = "user"
    for ui in users_ids:
        try:
            username = '@' + usernames_students[row]
        except Exception as e:
            print(e)
        row += 1
        course_status = await db.get_user_passer_status(tg_id=ui, course_id=course_id)
        right_answer = await db.get_positive_count(tg_id=ui, course_id=course_id)
        wrong_answer = await db.get_negative_count(tg_id=ui, course_id=course_id)
        start_time, end_time = await db.get_completion(tg_id=ui, course_id=course_id)

        # time = '2024_03_25 13_10_24'  # time example
        time_in_minutes = 0
        if start_time and end_time:
            start_time_list = start_time.split()
            start_time_list = start_time_list[0].split("_") + start_time_list[1].split("_")
            end_time_list = end_time.split()
            end_time_list = end_time_list[0].split("_") + end_time_list[1].split("_")

            print(start_time_list, end_time_list)
            start_time = datetime(*map(int, start_time_list))
            end_time = datetime(*map(int, end_time_list))

            # Вычисление разницы между начальным и конечным временем
            time_difference = end_time - start_time

            # Преобразование разницы времени в минуты
            time_in_minutes = time_difference.total_seconds() / 60
            # years = (int(end_time_list[0]) - int(start_time_list[0]))
            # month = (int(end_time_list[1]) - int(start_time_list[1]))
            # days = (int(end_time_list[2]) - int(start_time_list[2]))
            # hours = (int(end_time_list[3]) - int(start_time_list[3]))
            # minutes = int(end_time_list[4]) - int(start_time_list[4])
            # average_time = round((years + month + days + hours + minutes), 1)

        worksheet.write(row, 0, username)
        worksheet.write(row, 1, course_status)
        worksheet.write(row, 2, right_answer)
        worksheet.write(row, 3, wrong_answer)
        worksheet.write(row, 4, time_in_minutes)
        # worksheet.write(row, 4, average_time)

    excel.close()
    course_name = await db.get_course_name(course_id=course_id)
    passing_percentage, passed_users, right_answer, wrong_answer, average_time = await statistics_to_creator(
		course_id=course_id)
    with open(f"Статистика курса {course_name}.xlsx", "rb") as document:
        await bot.send_document(
            chat_id=tg_id,
            document=document,
			caption=f"Статистика по курсу <b>{course_name}</b>:\n\n"
				 f"Доходимость курса: {passing_percentage}\n"
				 f"Количество проходящих курс сейчас: {passed_users}\n"
				 f"Количество верных ответов: {right_answer}\n"
				 f"Количество неверных ответов: {wrong_answer}\n"
				 f"Среднее время прохождения курса: {average_time} мин",
			parse_mode='html',
			reply_markup=InlineKeyboardMarkup().add(
				InlineKeyboardButton(text='Назад', callback_data='courses_analytics')
			)
        )

    os.remove(f"Статистика курса {course_name}.xlsx")
