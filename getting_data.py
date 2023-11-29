from create_bot import bot


async def get_courses(bot_token: str) -> list[tuple]:
    # Код для получения списка курсов из базы данных
    # Возвращаем список курсов в формате (id, name)
    courses = [(1, 'Course 1'), (2, 'Course 2'), (3, 'Course 3')]
    return courses


async def get_course_modules(bot_token: str, course_id: int) -> list[tuple]:
    # Код для получения списка курсов из базы данных
    # Возвращаем список курсов в формате (id, name)
    modules = [(1, 'Module 1'), (2, 'Module 2'), (3, 'Module 3')]
    return modules