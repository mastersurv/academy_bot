import asyncpg


class DataBase:
    def __init__(self, db_name, user, password, host, port):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            database=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def execute_query(self, query, *args):
        async with self.pool.acquire() as connection:
            result = await connection.fetch(query, *args)
            return result

    async def create_tables(self):
        if self.pool is None:
            await self.connect()
        async with self.pool.acquire() as connection:
            # Создание таблиц (CREATE TABLE ...) для PostgreSQL
            await connection.execute('''
                CREATE TABLE IF NOT EXISTS bots (
                    bot_token TEXT PRIMARY KEY,
                    tg_id INT
                );
            ''')

            await connection.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    course_id INT PRIMARY KEY,
                    course_title VARCHAR(255),
                    course_description TEXT,
                    course_image BLOB,
                    bot_token TEXT
                );
            ''')

            await connection.execute('''
                CREATE TABLE IF NOT EXISTS modules (
                    module_id INT PRIMARY KEY,
                    course_id INT REFERENCES courses(course_id),
                    module_title VARCHAR(255),
                    module_description TEXT,
                    module_image BLOB,
                    bot_token TEXT
                );
            ''')

            await connection.execute('''
                CREATE TABLE IF NOT EXISTS lessons (
                    lesson_id INT PRIMARY KEY,
                    module_id INT REFERENCES modules(module_id),
                    course_id INT REFERENCES courses(course_id),
                    lesson_title VARCHAR(255),
                    lesson_description TEXT,
                    audio BLOB,
                    photo BLOB,
                    video BLOB,
                    video_note BLOB,
                    document BLOB,
                    document_name TEXT
                );
            ''')

    async def add_bot(self, bot_token: str, tg_id: int):
        if self.pool is None:
            await self.connect()

        async with self.pool.acquire() as connection:
            await connection.execute("""
                INSERT OR REPLACE INTO bots
                (bot_token, tg_id)
                VALUES
                (?, ?)
            """, (bot_token, tg_id))
    async def add_course(
            self, course_id: int, name: str, description: str, description_image: bytes, bot_token: str
    ):
        if self.pool is None:
            await self.connect()

        async with self.pool.acquire() as connection:
            await connection.execute("""
                INSERT OR REPLACE INTO courses
                (course_id, course_title, course_description, course_image, bot_token)
                VALUES
                (?, ?, ?, ?, ?)
            """, (course_id, name, description, description_image, bot_token))

    async def add_module(
            self, module_id: int, course_id: int, module_title: str, module_description: str, module_image: bytes, bot_token: str
    ):
        if self.pool is None:
            await self.connect()

        async with self.pool.acquire() as connection:
            await connection.execute("""
               INSERT OR REPLACE INTO modules
               (module_id, course_id, module_title, module_description, module_description, module_image, bot_token)
               VALUES
               (?, ?, ?, ?, ?, ?)
            """, (module_id, course_id, module_title, module_description, module_image, bot_token))

    async def add_lesson(
            self, lesson_id: int, module_id: int, course_id: int, lesson_title: str, lesson_description: str,
            audio: bytes or None, photo: bytes or None, video: bytes or None,
            video_note: bytes or None, document: bytes or None, document_name: str or None
    ):
        if self.pool is None:
            await self.connect()

        async with self.pool.acquire() as connection:
            await connection.execute("""
              INSERT OR REPLACE INTO modules
              (lesson_id, module_id, course_id, lesson_title, lesson_description, 
              audio, photo, video, video_note, document, document_name, bot_token)
              VALUES
              (?, ?, ?, ?, ?, ?)
            """, (lesson_id, module_id, course_id, lesson_title, lesson_description,
            audio, photo, video, video_note, document, document_name))

    async def get_courses_ids(self):
        if self.pool is None:
            await self.connect()
        async with self.pool.acquire() as connection:
            courses_ids = await connection.execute("""
              SELECT course_id FROM courses
            """).fetchall()