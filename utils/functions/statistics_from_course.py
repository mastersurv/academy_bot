from utils.functions.get_bot_and_db import get_bot_and_db


async def statistics_to_creator(course_id: int):
    bot, db = get_bot_and_db()

    all_users = await db.get_users_passers_by_status(course_id=course_id, status="all")
    passed_users = await db.get_users_passers_by_status(course_id=course_id, status="passed")

    if len(all_users) == 0:
        passing_percentage = "0 %"
    else:
        passing_percentage = str(round(len(passed_users) / len(all_users) * 100, 1)) + "%"

    years, month, days, hours, minutes = 0, 0, 0, 0, 0
    for user_id in all_users:
        start_time, end_time = await db.get_completion(tg_id=user_id, course_id=course_id)
        if start_time and end_time:
            start_time_list = start_time.split("_")
            end_time_list = end_time.split("_")

            years += (int(end_time_list[0]) - int(start_time_list[0])) * 24 * 30 * 365
            month += (int(end_time_list[1]) - int(start_time_list[1])) * 24 * 30
            days += (int(end_time_list[2]) - int(start_time_list[2])) * 24
            hours += (int(end_time_list[3]) - int(start_time_list[3]))
            minutes += int(end_time_list[4]) - int(start_time_list[4]) / 60

    average_time = round((years + month + days + hours + minutes) / len(all_users), 1)

    right_answer = 0
    wrong_answer = 0
    for user_id in all_users:
        right_answer += await db.get_positive_count(tg_id=user_id, course_id=course_id) # TODO
        wrong_answer += await db.get_negative_count(tg_id=user_id, course_id=course_id) # TODO

    return (passing_percentage, len(passed_users), right_answer, wrong_answer, average_time)
