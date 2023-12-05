from create_bot import bot


async def get_courses(bot_token: str) -> list[tuple]:
    # Код для получения списка курсов из базы данных
    # Возвращаем список курсов в формате (id, name)
    courses = [(1, 'Course 1'), (2, 'Course 2'), (3, 'Course 3')]
    return courses


async def get_course_modules(bot_token: str, course_id: int) -> list[tuple]:
    # Код для получения списка модулей курса из базы данных
    # Возвращаем список модулей курса в формате (id, name)
    modules = [(1, 'Module 1'), (2, 'Module 2'), (3, 'Module 3')]
    return modules


async def get_module_lessons(bot_token: str, course_id: int, module_id: int) -> list[tuple]:
    # Код для получения списка уроков модуля из базы данных
    # Возвращаем список уроков модуля в формате (id, name)
    modules = [(1, 'Lesson 1'), (2, 'Lesson 2'), (3, 'Lesson 3')]
    return modules