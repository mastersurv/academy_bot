import aiosqlite


class DataBase:
	def __init__(self, db_name):
		self.db_name = db_name
		self.conn = None

	async def connect(self):
		self.conn = await aiosqlite.connect(self.db_name)

	async def disconnect(self):
		if self.conn:
			await self.conn.close()

	async def execute_query(self, query, *args):
		async with self.conn.cursor() as cursor:
			await cursor.execute(query, args)
			result = await cursor.fetchall()
		return result

	async def create_tables(self):
		if self.conn is None:
			await self.connect()

		# Создание таблиц для SQLite

		await self.execute_query('''
            CREATE TABLE IF NOT EXISTS users(
                tg_id INTEGER PRIMARY KEY,
                full_name TEXT,
            )
        ''')

		await self.execute_query('''
		    CREATE TABLE IF NOT EXISTS subscription(
				  sub_id INTEGER,
				  tg_id int REFERENCES user(tg_id),
				  created_at datetime,
				  valid_till datetime
				)
		        ''')

		await self.execute_query('''
            CREATE TABLE IF NOT EXISTS users_posts(
                tg_id INTEGER PRIMARY KEY,
                post_id INTEGER,
                message_id INTEGER
            )
        ''')

		await self.execute_query('''
            CREATE TABLE IF NOT EXISTS courses (
                course_id INT PRIMARY KEY,
                course_title TEXT,
                course_description TEXT,
                course_image BLOB,
                bot_token TEXT
            )
        ''')

		await self.execute_query('''
            CREATE TABLE IF NOT EXISTS modules (
                module_id INT PRIMARY KEY,
                course_id INT REFERENCES courses(course_id),
                module_title TEXT,
                module_description TEXT,
                module_image BLOB,
                bot_token TEXT
            )
        ''')

		await self.execute_query('''
            CREATE TABLE IF NOT EXISTS lessons (
                lesson_id INT PRIMARY KEY,
                module_id INT REFERENCES modules(module_id),
                course_id INT REFERENCES courses(course_id),
                lesson_title TEXT,
                lesson_description TEXT,
                audio BLOB,
                photo BLOB,
                video BLOB,
                video_note BLOB,
                document BLOB,
                document_name TEXT
            )
        ''')

	async def add_user_post(self, tg_id: int, post_id: int) -> None:
		if self.conn is None:
			await self.connect()

		await self.execute_query(
			"""
			INSERT OR REPLACE INTO users_posts
			VALUES(?, ?, ?)
			""",
			(tg_id, post_id, 0)
		)

	async def get_post_id(self, tg_id: int) -> int:
		if self.conn is None:
			await self.connect()

		post_id_data = await self.execute_query(
			"""
			SELECT post_id FROM users_posts
			WHERE tg_id=?
			""",
			(tg_id,)
		)

		if post_id_data:
			return post_id_data[0][0]

	# Остальные методы аналогичны
	async def get_message_or_user(self, tg_id=None, message_id=None, id=None, message=None) -> int:
		if self.conn is None:
			await self.connect()

		if message:
			message_id_data = await self.execute_query(
				"""
				SELECT message_id FROM users_posts
				WHERE tg_id=?
				""",
				(tg_id,)
			)
			if message_id_data:
				return message_id_data[0][0]

		elif id:
			tg_id_data = await self.execute_query(
				"""
				SELECT tg_id FROM users_posts
				WHERE message_id=?
				""",
				(message_id,)
			)
			if tg_id_data:
				return tg_id_data[0][0]

	async def add_user_message(self, tg_id: int, message_id: int) -> None:
		if self.conn is None:
			await self.connect()

		await self.execute_query(
			"""
			INSERT OR REPLACE INTO users_messages
			VALUES(?, ?)
			""",
			(tg_id, message_id)
		)

	async def add_bot(self, bot_token: str, tg_id: int):
		if self.conn is None:
			await self.connect()

		await self.execute_query("""
            INSERT OR REPLACE INTO bots
            (bot_token, tg_id)
            VALUES
            (?, ?)
        """, (bot_token, tg_id))

	async def add_course(
			self, course_id: int, name: str, description: str or None, description_image: bytes or None, bot_token: str
	):
		if self.conn is None:
			await self.connect()

		await self.execute_query("""
            INSERT OR REPLACE INTO courses
            (course_id, course_title, course_description, course_image, bot_token)
            VALUES
            (?, ?, ?, ?, ?)
        """, (course_id, name, description, description_image, bot_token))

	async def add_module(
			self, module_id: int, course_id: int, module_title: str, module_description: str, module_image: bytes,
			bot_token: str
	):
		if self.conn is None:
			await self.connect()

		await self.execute_query("""
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
		if self.conn is None:
			await self.connect()

		await self.execute_query("""
          INSERT OR REPLACE INTO modules
          (lesson_id, module_id, course_id, lesson_title, lesson_description, 
          audio, photo, video, video_note, document, document_name, bot_token)
          VALUES
          (?, ?, ?, ?, ?, ?)
        """, (lesson_id, module_id, course_id, lesson_title, lesson_description,
		      audio, photo, video, video_note, document, document_name))

	async def get_courses_ids(self):
		if self.conn is None:
			await self.connect()
		courses_ids = await self.execute_query("""
          SELECT course_id FROM courses
        """)
		return courses_ids

	# ------------------- оставшиеся методы -------------------
	async def get_creators_ids(self) -> list:
		if self.conn is None:
			await self.connect()

	async def get_subscriptions(self):
		if self.conn is None:
			await self.connect()
		subscriptions = await self.execute_query(
			"select sub_id from subscription where tg_id = %d and valid_till > now()"
		)
		courses = await self.execute_query(
			"select course_id from subscription_course where sub_id in (%s)", subscriptions
		)
		return courses

