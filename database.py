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
			await cursor.execute(query, *args)
			result = await cursor.fetchall()
		await self.conn.commit()
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
		        course_image_id TEXT,
		        promocode TEXT
		    )
		''')

		await self.execute_query('''
            CREATE TABLE IF NOT EXISTS modules (
                module_id INT PRIMARY KEY,
                course_id INT REFERENCES courses(course_id),
                module_title TEXT,
                module_description TEXT,
                module_image TEXT
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

	async def add_course(self, course_id: int, owner_id: int, course_name: str, course_description: str, course_image_id: int,
	                     promocode: str):
		query = '''
	            INSERT OR REPLACE INTO courses (course_id, owner_id, course_name, 
	            course_description, course_image_id, promocode)
	            VALUES (?, ?, ?, ?, ?, ?)
	        '''
		await self.execute_query(query, (course_id, owner_id, course_name,
		                                 course_description, course_image_id, promocode))

	async def add_module(
			self, module_id: int, course_id: int, module_title: str, module_description: str, module_image: str
	):
		if self.conn is None:
			await self.connect()

		await self.execute_query("""
           INSERT OR REPLACE INTO modules
           (module_id, course_id, module_title, module_description, module_image)
           VALUES
           (?, ?, ?, ?, ?)
        """, (module_id, course_id, module_title, module_description, module_image))

	async def add_lesson(
			self, lesson_id: int, module_id: int, course_id: int, lesson_title: str, lesson_description: str,
			audio: str = None, photo: str = None, video: str = None,
			video_note: str = None, document: str = None, document_name: str = None
	):
		if self.conn is None:
			await self.connect()

		query = '''
		        INSERT OR REPLACE INTO lessons (
		            lesson_id, module_id, course_id, lesson_title, lesson_description,
		            audio, photo, video, video_note, document, document_name
		        )
		        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		    '''
		await self.execute_query(query, (
			lesson_id, module_id, course_id, lesson_title, lesson_description,
			audio, photo, video, video_note, document, document_name
		))

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

	# Запросы для курсов, модулей, уроков
	async def get_course_info(self, course_id):
		query = '''
	        SELECT course_name, course_description, course_image_id
	        FROM courses
	        WHERE course_id = ?
	    '''
		result = await self.execute_query(query, (course_id,))
		return result[0] if result else None

	async def get_module_info(self, course_id, module_id):
		query = '''
	        SELECT module_title, module_description, module_image
	        FROM modules
	        WHERE course_id = ? AND module_id = ?
	    '''
		result = await self.execute_query(query, (course_id, module_id))
		return result[0] if result else None

	async def get_lesson_info(self, course_id, module_id, lesson_id):
		query = '''
	            SELECT lesson_title, lesson_description, audio, photo, video, video_note, document, document_name
	            FROM lessons
	            WHERE course_id = ? AND module_id = ? AND lesson_id = ?
	        '''
		result = await self.execute_query(query, (course_id, module_id, lesson_id))
		if result:
			lesson_info = {
				"lesson_title": result[0][0],
				"lesson_description": result[0][1],
				"audio": result[0][2],
				"photo": result[0][3],
				"video": result[0][4],
				"video_note": result[0][5],
				"document": result[0][6],
				"document_name": result[0][7]
			}
			return lesson_info
		else:
			return None

	async def get_modules_numbers(self, course_id):
		query = '''
	            SELECT COUNT(*) as num_modules
	            FROM modules
	            WHERE course_id = ?
	        '''
		result = await self.execute_query(query, (course_id,))
		return result[0][0] if result else 0

	async def get_lessons_numbers(self, course_id, module_id):
		query = '''
	            SELECT COUNT(*) as num_lessons
	            FROM lessons
	            WHERE course_id = ? AND module_id = ?
	        '''
		result = await self.execute_query(query, (course_id, module_id))
		return result[0][0] if result else 0

	# Обновления данных в таблицах
	async def update_course_name(self, course_id, new_name):
		query = '''
	            UPDATE courses
	            SET course_name = ?
	            WHERE course_id = ?
	        '''
		await self.execute_query(query, (new_name, course_id))

	async def update_module_name(self, course_id, module_id, new_name):
		query = '''
	            UPDATE modules
	            SET module_name = ?
	            WHERE course_id = ? AND module_id = ?
	        '''
		await self.execute_query(query, (new_name, course_id, module_id))

	async def update_lesson_title(self, course_id, module_id, lesson_id, new_title):
		query = '''
	            UPDATE lessons
	            SET lesson_title = ?
	            WHERE course_id = ? AND module_id = ? AND lesson_id = ?
	        '''
		await self.execute_query(query, (new_title, course_id, module_id, lesson_id))

	async def update_course_description(self, course_id, new_description):
		query = '''
	            UPDATE courses
	            SET course_description = ?
	            WHERE course_id = ?
	        '''
		await self.execute_query(query, (new_description, course_id))

	async def update_module_description(self, course_id, module_id, new_description):
		query = '''
	            UPDATE modules
	            SET module_description = ?
	            WHERE course_id = ? AND module_id = ?
	        '''
		await self.execute_query(query, (new_description, course_id, module_id))

	async def update_lesson_description(self, course_id, module_id, lesson_id, new_description):
		query = '''
	            UPDATE lessons
	            SET lesson_description = ?
	            WHERE course_id = ? AND module_id = ? AND lesson_id = ?
	        '''
		await self.execute_query(query, (new_description, course_id, module_id, lesson_id))

	async def update_course_image(self, course_id, new_image):
		query = '''
	            UPDATE courses
	            SET course_image_id = ?
	            WHERE course_id = ?
	        '''
		await self.execute_query(query, (new_image, course_id))

	async def update_module_image(self, course_id, module_id, new_image):
		query = '''
	            UPDATE modules
	            SET module_image = ?
	            WHERE course_id = ? AND module_id = ?
	        '''
		await self.execute_query(query, (new_image, course_id, module_id))

	async def update_lesson_image(self, course_id, module_id, lesson_id, new_image):
		query = '''
	            UPDATE lessons
	            SET photo = ?
	            WHERE course_id = ? AND module_id = ? AND lesson_id = ?
	        '''
		await self.execute_query(query, (new_image, course_id, module_id, lesson_id))

	async def update_lesson_materials(self, course_id, module_id, lesson_id, materials):
		valid_materials = {
			'audio': 'audio',
			'photo': 'photo',
			'video': 'video',
			'video_note': 'video_note',
			'document': 'document',
			'document_name': 'document_name'
		}

		update_query = 'UPDATE lessons SET '

		for key, field in valid_materials.items():
			if key in materials and materials[key] is not None:
				update_query += f'{field} = ?, '

		# Удаляем последнюю запятую и пробел
		update_query = update_query.rstrip(', ')

		update_query += ' WHERE course_id = ? AND module_id = ? AND lesson_id = ?'

		# Собираем значения для запроса
		values = [materials[key] for key in valid_materials if key in materials and materials[key] is not None]
		values.extend([course_id, module_id, lesson_id])

		# Выполняем запрос
		await self.execute_query(update_query, values)


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
# 	# Добавление КУРСА
# 	loop.run_until_complete(db.add_course(course_id=1, owner_id=1, course_name='python base',
# 	                                      course_description='base funcs in python',
# 	                                      course_image_id=123, promocode='123'))
#
# 	# вывод данных по курсу
# 	print(loop.run_until_complete(db.get_course_info(1)), 'Курс')
#
# 	# Добавление МОДУЛЯ
# 	loop.run_until_complete(db.add_module(module_id=1, course_id=1, module_title='1. Variables',
# 	                                      module_description='Test', module_image='brbrbrbbr'))
#
# 	# вывод данных по модулю
# 	print(loop.run_until_complete(db.get_module_info(1, 1)), 'Модуль')
#
# 	# Добавление УРОКА
# 	loop.run_until_complete(db.add_lesson(lesson_id=1, module_id=1, course_id=1, lesson_title='Первый урок',
# 	                                      lesson_description='Описание', video='video_id'))
#
# 	# вывод данных по уроку
# 	print(loop.run_until_complete(db.get_lesson_info(1, 1, 1)), 'Урок')
#
# 	# Закройте цикл событий после выполнения
# 	loop.close()
