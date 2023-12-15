import datetime
import aiosqlite
import random
import string


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
                full_name TEXT
            )
        ''')

		await self.execute_query('''
		    CREATE TABLE IF NOT EXISTS subscription(
				  sub_id INTEGER,
				  tg_id int REFERENCES users(tg_id),
				  created_at datetime,
				  valid_till datetime
				)
		        ''')

		await self.execute_query('''
		            CREATE TABLE IF NOT EXISTS user_courses(
		                tg_id int REFERENCES users(tg_id),
		                course_id INT REFERENCES courses(course_id)
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
		    CREATE TABLE IF NOT EXISTS promocodes (
		            promocode TEXT PRIMARY KEY,
					course_id INT REFERENCES courses(course_id)
		        )
		    ''')

		await self.execute_query('''
		    CREATE TABLE IF NOT EXISTS courses (
		        course_id INTEGER PRIMARY KEY,
		        owner_id INTEGER REFERENCES users(tg_id),
		        course_name TEXT,
		        course_description TEXT,
		        course_preview TEXT,
		        promocode TEXT
		    )
		''')

		await self.execute_query('''
            CREATE TABLE IF NOT EXISTS modules (
                module_id INT PRIMARY KEY,
                course_id INT REFERENCES courses(course_id),
                module_title TEXT,
                module_description TEXT,
                module_image TEXT,
            )
        ''')

		await self.execute_query('''
            CREATE TABLE IF NOT EXISTS lessons (
                lesson_id INT PRIMARY KEY,
                module_id INT REFERENCES modules(module_id),
                course_id INT REFERENCES courses(course_id),
                lesson_title TEXT,
                lesson_description TEXT,
                audio TEXT,
                photo TEXT,
                video TEXT,
                video_note TEXT,
                document TEXT,
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

	async def add_course(self, course_id: int, course_name: int, course_description: int, course_image_id: int,
	                     promocode: str):
		query = '''
	            INSERT OR REPLACE INTO courses (course_id, course_name, course_description, course_image_id, promocode)
	            VALUES (?, ?, ?, ?, ?)
	        '''
		await self.execute_query(query, (course_id, course_name, course_description, course_image_id, promocode))

	async def add_module(
			self, module_id: int, course_id: int, module_title: str, module_description: str, module_image: str
	):
		if self.conn is None:
			await self.connect()

		await self.execute_query("""
           INSERT OR REPLACE INTO modules
           (module_id, course_id, module_title, module_description, module_description, module_image, bot_token)
           VALUES
           (?, ?, ?, ?, ?)
        """, (module_id, course_id, module_title, module_description, module_image))

	async def add_lesson(
			self, lesson_id: int, module_id: int, course_id: int, lesson_title: str, lesson_description: str,
			audio: str or None, photo: str or None, video: str or None,
			video_note: str or None, document: str or None, document_name: str or None
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

	async def get_courses_ids(self, tg_id):
		query = '''
	            SELECT courses_ids
	            FROM users
	            WHERE tg_id = ?
	        '''
		user_courses_ids = await self.execute_query(query, (tg_id,))
		return user_courses_ids[0][0].split(',') if user_courses_ids else []

	# ------------------- оставшиеся методы -------------------
	async def get_creators_ids(self) -> list:
		if self.conn is None:
			await self.connect()
		current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		creators_ids = await self.execute_query('''
	            SELECT u.tg_id
	            FROM users u
	            JOIN subscription s ON u.tg_id = s.tg_id
	            WHERE s.valid_till > '{}'
	        '''.format(current_datetime))

		creator_ids = [row[0] for row in creators_ids]

		return creator_ids

	async def get_course_modules(self, course_id):
		query = '''
	            SELECT module_id, module_name
	            FROM modules
	            WHERE course_id = ?
	        '''
		modules_info = await self.execute_query(query, (course_id,))
		return modules_info

	async def get_module_lessons(self, course_id, module_id):
		query = '''
	            SELECT lesson_id, lesson_name
	            FROM lessons
	            WHERE course_id = ? AND module_id = ?
	        '''
		lessons_info = await self.execute_query(query, (course_id, module_id))
		return lessons_info

	async def get_promocodes_dict(self):
		query = '''
	            SELECT promocode, course_id
	            FROM promocodes
	        '''
		promocodes_info = await self.execute_query(query)
		promocodes_dict = {row[0]: row[1] for row in promocodes_info}
		return promocodes_dict

	async def add_course_to_user(self, tg_id, course_id):
		current_courses_ids = await self.get_courses_ids(tg_id)

		if current_courses_ids is not None:
			# Если у пользователя уже есть какие-то курсы
			new_courses_ids = f'{current_courses_ids},{course_id}'
		else:
			# Если у пользователя еще нет курсов
			new_courses_ids = str(course_id)

		# Обновляем поле courses_ids в таблице users
		update_query = '''
	            UPDATE users
	            SET courses_ids = ?
	            WHERE tg_id = ?
	        '''
		await self.execute_query(update_query, (new_courses_ids, tg_id))

	async def get_course_name(self, course_id):
		query = '''
	            SELECT course_name
	            FROM courses
	            WHERE course_id = ?
	        '''
		course_info = await self.execute_query(query, (course_id,))
		return course_info[0][0] if course_info else None

	async def get_users_ids(self):
		query = '''
	            SELECT tg_id
	            FROM users
	        '''
		users_ids = await self.execute_query(query)
		return [row[0] for row in users_ids]

	async def get_number_of_created_courses(self, tg_id):
		query = '''
	            SELECT COUNT(*) as num_created_courses
	            FROM courses
	            WHERE owner_id = ?
	        '''
		result = await self.execute_query(query, (tg_id,))
		return result[0][0] if result else 0

	async def get_subscription_data(self):
		query = '''
	            SELECT status, COUNT(*) as num_courses
	            FROM (
	                SELECT
	                    CASE
	                        WHEN valid_till >= datetime('now') THEN 'active'
	                        ELSE 'expired'
	                    END as status
	                FROM subscription
	            ) AS sub_status
	            GROUP BY status
	        '''
		result = await self.execute_query(query)
		subscription_data = {row[0]: row[1] for row in result}
		return subscription_data

	async def get_promocodes(self):
		query = '''
	            SELECT promocode
	            FROM promocodes
	        '''
		result = await self.execute_query(query)
		promocodes = [row[0] for row in result]
		return promocodes

	async def get_promocode(self, course_id):
		query = '''
	            SELECT promocode
	            FROM promocodes
	            WHERE course_id = ?
	        '''
		result = await self.execute_query(query, (course_id,))
		promocodes = [row[0] for row in result]
		return promocodes

	async def get_user_courses(self, tg_id):
		query = '''
	            SELECT course_id
	            FROM user_courses
	            WHERE tg_id = ?
	        '''
		result = await self.execute_query(query, (tg_id,))
		return [row[0] for row in result]

	async def add_user_course(self, tg_id, course_id):
		query = '''
	            INSERT INTO user_courses (tg_id, course_id)
	            VALUES (?, ?)
	        '''
		await self.execute_query(query, (tg_id, course_id))

	async def generate_unique_course_id(self):
		while True:
			course_id = random.randint(10000000, 99999999)  # Генерация восьмизначного числа
			# Проверка, есть ли уже такой course_id в базе
			existing_courses = await self.execute_query(
				'SELECT course_id FROM courses WHERE course_id = %s', course_id
			)
			if not existing_courses:
				return course_id

	async def generate_unique_promocode(self, course_id):
		while True:
			# Генерация промокода из 8 случайных букв
			promocode = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))
			# Проверка, есть ли уже такой промокод в базе для данного курса
			existing_promocodes = await self.execute_query(
				'SELECT promocode FROM promocodes WHERE promocode = %s AND course_id = %s',
				promocode, course_id
			)
			if not existing_promocodes:
				return promocode

# import asyncio
#
# if __name__ == '__main__':
# 	db = DataBase('test.db')
#
# 	# Создайте цикл событий asyncio
# 	loop = asyncio.get_event_loop()
#
# 	# Запустите асинхронную функцию в цикле событий
# 	loop.run_until_complete(db.create_tables())
#
# 	# Закройте цикл событий после выполнения
#
#
# 	print(loop.run_until_complete(db.get_creators_ids()))
# 	loop.close()
