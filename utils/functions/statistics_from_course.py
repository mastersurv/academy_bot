from utils.functions.get_bot_and_db import get_bot_and_db


async def statistics_to_creator(course_id: int):
    bot, db = get_bot_and_db()

    all_users = db.get_users_passers_by_status(course_id=course_id, status="all")
    passed_users = db.get_users_passers_by_status(course_id=course_id, status="passed")

    if len(all_users) == 0:
        passing_percentage = 0
    else:
        passing_percentage = str(round(passed_users / all_users * 100, 1)) + "%"

    average_time = 0
    for user_id in all_users:
        start_time, end_time = await db.get_completion(tg_id=user_id, course_id=course_id)
        start_time_list = start_time.split("_")
        end_time_list = end_time.split("_")

        years = int(end_time_list[0]) - int(start_time_list[0])
        month = int(end_time_list[1]) - int(start_time_list[1])
        days = int(end_time_list[2]) - int(start_time_list[2])
        hours = int(end_time_list[3]) - int(start_time_list[3])
        minutes = int(end_time_list[4]) - int(start_time_list[4])