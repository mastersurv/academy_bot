from utils.functions.get_bot_and_db import get_bot_and_db
from xlsxwriter import Workbook
import os


async def statistics_to_student(tg_id: int):
    bot, db = get_bot_and_db()

    courses_ids = await db.get_courses_ids(tg_id=tg_id)
    excel = Workbook("Статистика пользователя.xlsx")
    worksheet = excel.add_worksheet()

    row = 0
    worksheet.write(row, 0, "Название курса")
    worksheet.write(row, 1, "Статус прохождения")
    worksheet.write(row, 2, "Количество правильных ответов")
    worksheet.write(row, 3, "количество неверных ответов")
    worksheet.write(row, 4, "Время прохождения")

    average_time = "-"
    for ci in courses_ids:
        row += 1
        course_name = await db.get_course_name(course_id=ci)
        course_status = await db.get_user_passer_status(tg_id=tg_id)
        right_answer = await db.get_positive_count(tg_id=tg_id, course_id=ci) # TODO
        wrong_answer = await db.get_negative_count(tg_id=tg_id, course_id=ci) # TODO
        start_time, end_time = await db.get_completion(tg_id=tg_id, course_id=ci) # TODO

        if start_time and end_time:
            start_time_list = start_time.split("_")
            end_time_list = end_time.split("_")

            years = (int(end_time_list[0]) - int(start_time_list[0])) * 24 * 30 * 365
            month = (int(end_time_list[1]) - int(start_time_list[1])) * 24 * 30
            days = (int(end_time_list[2]) - int(start_time_list[2])) * 24
            hours = (int(end_time_list[3]) - int(start_time_list[3]))
            minutes = int(end_time_list[4]) - int(start_time_list[4]) / 60

            average_time = round((years + month + days + hours + minutes), 1)

        worksheet.write(row, 0, course_name)
        worksheet.write(row, 1, course_status)
        worksheet.write(row, 2, right_answer)
        worksheet.write(row, 3, wrong_answer)
        worksheet.write(row, 4, average_time)

        with open("Статистика пользователя.xlsx", "rb") as document:
            await bot.send_document(
                chat_id=tg_id,
                document=document,
                caption="Ваша статистика по курсам"
            )

        os.remove("Статистика пользователя.xlsx")