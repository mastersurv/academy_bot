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
		if self.conn is None:
			await self.connect()
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
					course_id INT REFERENCES courses(course_id),
					chat_name TEXT,
					usages_left INT,
					chat_id INT
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
                module_id INT,
                course_id INT REFERENCES courses(course_id),
                module_name TEXT,
                module_description TEXT,
                module_image TEXT
            )
        ''')

		await self.execute_query('''
            CREATE TABLE IF NOT EXISTS lessons (
                lesson_id INT,
                module_id INT,
                course_id INT REFERENCES courses(course_id),
                lesson_title TEXT,
                lesson_description TEXT,
                text TEXT,
                audio TEXT,
                photo TEXT,
                video TEXT,
                video_note TEXT,
                document TEXT
            )
        ''')

		await self.execute_query('''
            CREATE TABLE IF NOT EXISTS test_questions (
                course_id INT REFERENCES courses(course_id),
                module_id INT REFERENCES modules(module_id),
                lesson_id INT REFERENCES lessons(lesson_id),
                test_id INT,
                test_question TEXT,
                right_answer TEXT
            )
        ''')

		await self.execute_query('''
            CREATE TABLE IF NOT EXISTS test_answers (
                course_id INT,
                module_id INT,
                lesson_id INT,
                test_id INT,
                answer_num INT,
                answer TEXT,
                PRIMARY KEY (course_id, module_id, lesson_id, test_id, answer_num),
                FOREIGN KEY (course_id, module_id, lesson_id, test_id) REFERENCES test_questions(course_id, module_id, lesson_id, test_id)
            )
        ''')

		await self.execute_query('''
		    CREATE TABLE IF NOT EXISTS final_message (
			    course_id INT REFERENCES courses(course_id),
			    text TEXT,
			    audio TEXT,
			    photo TEXT,
			    video TEXT,
			    video_note TEXT,
			    document TEXT
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
			UPDATE users_posts
			SET message_id = ?
			WHERE tg_id = ?
			""",
			(message_id, tg_id)
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

	async def add_course(self, course_id: int, owner_id: int, course_name: str, course_description: str,
	                     course_image_id: int,
	                     promocode: str):
		query = '''
	            INSERT OR REPLACE INTO courses (course_id, owner_id, course_name, 
	            course_description, course_image_id, promocode)
	            VALUES (?, ?, ?, ?, ?, ?)
	        '''
		await self.execute_query(query, (course_id, owner_id, course_name,
		                                 course_description, course_image_id, promocode))

	async def add_module(
			self, module_id: int, course_id: int, module_name: str, module_description: str, module_image: str
	):
		if self.conn is None:
			await self.connect()

		await self.execute_query("""
           INSERT OR REPLACE INTO modules
           (module_id, course_id, module_name, module_description, module_image)
           VALUES
           (?, ?, ?, ?, ?)
        """, (module_id, course_id, module_name, module_description, module_image))

	async def add_lesson(
			self, lesson_id: int, module_id: int, course_id: int, lesson_title: str,
			text: str = None, audio_id: str = None, photo_id: str = None, video_id: str = None,
			video_note_id: str = None, document_id: str = None, document_name: str = None
	):
		if self.conn is None:
			await self.connect()

		query = '''
            INSERT OR REPLACE INTO lessons (
                lesson_id, module_id, course_id, lesson_title, text, 
                audio, photo, video, video_note, document, document_name
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
		await self.execute_query(query, (
			lesson_id, module_id, course_id, lesson_title, text,
			audio_id, photo_id, video_id, video_note_id, document_id, document_name
		))

	async def add_test_answer(self, course_id, module_id, lesson_id, test_id, answer_num, answer):
		if self.conn is None:
			await self.connect()

		existing_record = await self.execute_query('''
		        SELECT *
		        FROM test_answers
		        WHERE course_id = ? AND module_id = ? AND lesson_id = ? AND test_id = ? AND answer_num = ?
		    ''', (course_id, module_id, lesson_id, test_id, answer_num))

		if existing_record:
			print("Запись уже существует в таблице test_answers")
		else:
			query = '''
		            INSERT INTO test_answers (course_id, module_id, lesson_id, test_id, answer_num, answer)
		            VALUES (?, ?, ?, ?, ?, ?)
		        '''
			await self.execute_query(query, (course_id, module_id, lesson_id, test_id, answer_num, answer))

	async def delete_test_question(self, course_id, module_id, lesson_id, test_id):
		if self.conn is None:
			await self.connect()

		# Удаляем тестовые ответы, связанные с вопросом
		await self.execute_query('''
            DELETE FROM test_answers
            WHERE course_id = ? AND module_id = ? AND lesson_id = ? AND test_id = ?
        ''', (course_id, module_id, lesson_id, test_id))

		# Удаляем сам тестовый вопрос
		await self.execute_query('''
            DELETE FROM test_questions
            WHERE course_id = ? AND module_id = ? AND lesson_id = ? AND test_id = ?
        ''', (course_id, module_id, lesson_id, test_id))

	async def get_courses_ids(self, tg_id):
		if self.conn is None:
			await self.connect()

		query = '''
            SELECT course_id
            FROM courses
            WHERE owner_id = ?
        '''

		user_courses = await self.execute_query(query, (tg_id,))
		return [course[0] for course in user_courses] if user_courses else []

	# ------------------- оставшиеся методы -------------------
	async def get_creators_ids(self) -> list:
		if self.conn is None:
			await self.connect()

		current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		query = '''
            SELECT u.tg_id
            FROM users u
            JOIN subscription s ON u.tg_id = s.tg_id
            WHERE s.valid_till > ?
        '''

		creators_ids = await self.execute_query(query, (current_datetime,))
		creator_ids = [row[0] for row in creators_ids]

		return creator_ids

	async def get_module_name(self, course_id, module_id):
		if self.conn is None:
			await self.connect()

		query = '''
            SELECT module_name
            FROM modules
            WHERE course_id = ? AND module_id = ?
        '''

		result = await self.execute_query(query, (course_id, module_id))

		if result:
			return result[0][0]
		else:
			return None

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
	            SELECT lesson_id, lesson_title
	            FROM lessons
	            WHERE course_id = ? AND module_id = ?
	        '''
		lessons_info = await self.execute_query(query, (course_id, module_id))
		return lessons_info

	async def get_promocodes_dict(self):
		query = '''
	            SELECT promocode, course_id
	            FROM courses
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

	async def get_course_description(self, course_id):
		query = '''
    	            SELECT course_description
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

	async def add_user(self, tg_id, full_name):
		# Проверяем, существует ли пользователь с таким tg_id
		existing_user = await self.get_user_by_id(tg_id)

		# Если пользователь уже существует, пропускаем добавление
		if existing_user:
			return

		# Иначе выполняем вставку нового пользователя
		query = '''
	        INSERT INTO users (tg_id, full_name)
	        VALUES (?, ?)
	    '''
		await self.execute_query(query, (tg_id, full_name))

	async def get_user_by_id(self, tg_id):
		query = '''
	        SELECT * FROM users WHERE tg_id = ?
	    '''
		result = await self.execute_query(query, (tg_id,))
		return result

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

	async def get_course_promocode(self, course_id):
		query = '''
	            SELECT promocode
	            FROM courses
	            WHERE course_id = ?
	        '''
		result = await self.execute_query(query, (course_id,))
		promocodes = [row[0] for row in result]
		if promocodes:
			return promocodes[0]
		return None

	async def get_promocode(self, course_id):
		if self.conn is None:
			await self.connect()

		query = '''
	        SELECT promocode
	        FROM promocodes
	        WHERE course_id = ?
	    '''

		result = await self.execute_query(query, (course_id,))
		if result:
			return result[0][0]  # Возвращаем промокод, если он есть
		else:
			return None  # Возвращаем None, если курс с указанным course_id не найден

	async def get_user_courses(self, tg_id):
		query = '''
	            SELECT course_id
	            FROM user_courses
	            WHERE tg_id = ?
	        '''
		result = await self.execute_query(query, (tg_id,))
		return [row[0] for row in result]

	async def add_user_course(self, tg_id, course_id):
		# Проверяем, существует ли уже запись с таким tg_id и course_id
		query = '''
		        SELECT COUNT(*)
		        FROM user_courses
		        WHERE tg_id = ? AND course_id = ?
		    '''
		result = await self.execute_query(query, (tg_id, course_id))
		count = result[0][0] if result else 0

		# Если запись уже существует, не добавляем её заново
		if count > 0:
			return

		# Иначе добавляем новую запись
		insert_query = '''
		        INSERT INTO user_courses (tg_id, course_id)
		        VALUES (?, ?)
		    '''
		await self.execute_query(insert_query, (tg_id, course_id))

	async def add_promocode(self, promocode, course_id,  chat_name=None, usages_left=None, chat_id=None):
		query = '''
	        INSERT OR REPLACE INTO promocodes (promocode, course_id, chat_name, usages_left, chat_id)
	        VALUES (?, ?, ?, ?, ?)
	    '''
		await self.execute_query(query, (promocode, course_id, chat_name, usages_left, chat_id))

	async def add_test_question(self, course_id, module_id, lesson_id, test_id, test_question, right_answer):
		if self.conn is None:
			await self.connect()

		query = '''
            INSERT OR REPLACE INTO test_questions (
                course_id, module_id, lesson_id, test_id, test_question, right_answer
            )
            VALUES (?, ?, ?, ?, ?, ?)
        '''
		await self.execute_query(query, (course_id, module_id, lesson_id, test_id, test_question, right_answer))

	async def get_test_numbers(self, course_id, module_id, lesson_id):
		if self.conn is None:
			await self.connect()

		query = '''
            SELECT COUNT(*) FROM test_questions
            WHERE course_id = ? AND module_id = ? AND lesson_id = ?
        '''
		result = await self.execute_query(query, (course_id, module_id, lesson_id))

		return result[0][0] if result else 1

	async def get_subscription_status(self, tg_id):
		if self.conn is None:
			await self.connect()

		current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		query = '''
            SELECT CASE
                WHEN s.valid_till > ? THEN 'active'
                ELSE 'user'
            END AS subscription_status
            FROM users u
            LEFT JOIN subscription s ON u.tg_id = s.tg_id
            WHERE u.tg_id = ?
        '''

		result = await self.execute_query(query, (current_datetime, tg_id))

		if result:
			return result[0][0]
		else:
			return 'user'

	async def generate_unique_course_id(self):
		while True:
			course_id = random.randint(10000000, 99999999)  # Генерация восьмизначного числа
			# Проверка, есть ли уже такой course_id в базе
			existing_courses = await self.execute_query(
				'SELECT course_id FROM courses WHERE course_id = ?', (course_id,)
			)
			if not existing_courses:
				return course_id

	async def get_created_courses_ids(self, tg_id):
		if self.conn is None:
			await self.connect()

		query = '''
            SELECT course_id
            FROM courses
            WHERE owner_id = ?
        '''

		user_courses = await self.execute_query(query, (tg_id,))

		return [course[0] for course in user_courses] if user_courses else []

	async def generate_unique_promocode(self, course_id):
		while True:
			# Генерация промокода из 8 случайных букв
			promocode = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))
			# Проверка, есть ли уже такой промокод в базе для данного курса
			existing_promocodes = await self.execute_query(
				'SELECT promocode FROM promocodes WHERE promocode = ? AND course_id = ?',
				(promocode, course_id)
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
	        SELECT module_name, module_description, module_image
	        FROM modules
	        WHERE course_id = ? AND module_id = ?
	    '''
		result = await self.execute_query(query, (course_id, module_id))
		return result[0] if result else None

	async def get_module_description(self, course_id, module_id):
		query = '''
	        SELECT module_description
	        FROM modules
	        WHERE course_id = ? AND module_id = ?
	    '''
		result = await self.execute_query(query, (course_id, module_id))
		return result[0][0] if result else None

	async def get_lesson_info(self, course_id, module_id, lesson_id):
		query = '''
	        SELECT lesson_title, text, audio, photo, video, video_note, document
	        FROM lessons
	        WHERE course_id = ? AND module_id = ? AND lesson_id = ?
	    '''
		result = await self.execute_query(query, (course_id, module_id, lesson_id))
		print(result)
		return result[0] if result else None

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

	async def update_course_image(self, course_id, image_file_id):
		query = '''
	            UPDATE courses
	            SET course_image_id = ?
	            WHERE course_id = ?
	        '''
		await self.execute_query(query, (image_file_id, course_id))

	async def update_module_image(self, course_id, module_id, image_file_id):
		query = '''
	            UPDATE modules
	            SET module_image = ?
	            WHERE course_id = ? AND module_id = ?
	        '''
		await self.execute_query(query, (image_file_id, course_id, module_id))

	async def update_lesson_image(self, course_id, module_id, lesson_id, new_image):
		query = '''
	            UPDATE lessons
	            SET photo = ?
	            WHERE course_id = ? AND module_id = ? AND lesson_id = ?
	        '''
		await self.execute_query(query, (new_image, course_id, module_id, lesson_id))

	async def update_lesson_material(self, course_id, module_id, lesson_id, text, audio_id, photo_id, video_id, video_note_id, document_id):
		update_query = """
			UPDATE lessons
			SET text = ?,
			audio = ?,
			photo = ?,
			video = ?,
			video_note = ?,
			document = ?
			WHERE course_id = ?
			AND module_id = ?
			AND lesson_id = ?
			
		"""
		# Выполняем запрос
		await self.execute_query(update_query, (text, audio_id, photo_id, video_id, video_note_id, document_id, course_id, module_id, lesson_id))

	async def get_test_question(self, course_id, module_id, lesson_id, test_id):
		if self.conn is None:
			await self.connect()

		# Получаем информацию о тестовом вопросе и номере правильного ответа
		result = await self.execute_query('''
            SELECT test_question, right_answer
            FROM test_questions
            WHERE course_id = ? AND module_id = ? AND lesson_id = ? AND test_id = ?
        ''', (course_id, module_id, lesson_id, test_id))

		if result:
			test_question, right_answer = result[0]
			return test_question, right_answer
		else:
			return None, None

	async def get_test_answers(self, course_id, module_id, lesson_id, test_id):
		if self.conn is None:
			await self.connect()

		# Получаем информацию о тестовом ответе
		result = await self.execute_query('''
		        SELECT test_id, answer
		        FROM test_answers
		        WHERE course_id = ? AND module_id = ? AND lesson_id = ? AND test_id = ?
		    ''', (course_id, module_id, lesson_id, test_id))

		if not result:
			return []  # Возвращаем пустой список, если ответов нет

		test_answers = [(row[0], row[1]) for row in result]
		return test_answers

	async def check_next_lesson(self, course_id, module_id, lesson_id):
		query = '''
            SELECT 1
            FROM lessons
            WHERE course_id = ? AND module_id = ? AND lesson_id > ?
            LIMIT 1
        '''
		result = await self.execute_query(query, (course_id, module_id, lesson_id))
		return bool(result)

	async def get_test_id_in_lesson(self, course_id, module_id, lesson_id):
		if self.conn is None:
			await self.connect()

		query = '''
	        SELECT test_id
	        FROM test_questions
	        WHERE course_id = ? AND module_id = ? AND lesson_id = ?
	    '''
		result = await self.execute_query(query, (course_id, module_id, lesson_id))

		return result[0][0] if result else None

	async def check_next_module(self, course_id, module_id):
		query = '''
            SELECT 1
            FROM modules
            WHERE course_id = ? AND module_id > ?
            LIMIT 1
        '''
		result = await self.execute_query(query, (course_id, module_id))
		return bool(result)

	async def get_next_lesson_in_module(self, course_id, module_id, lesson_id):
		query = '''
            SELECT lesson_id
            FROM lessons
            WHERE course_id = ? AND module_id = ? AND lesson_id > ?
            ORDER BY lesson_id
            LIMIT 1
        '''
		result = await self.execute_query(query, (course_id, module_id, lesson_id))
		return result[0][0] if result else None

	async def get_next_module(self, course_id, module_id):
		query = '''
            SELECT module_id
            FROM modules
            WHERE course_id = ? AND module_id > ?
            ORDER BY module_id
            LIMIT 1
        '''
		result = await self.execute_query(query, (course_id, module_id))
		return result[0][0] if result else None

	async def add_final_message(self, course_id, text=None, audio_id=None, photo_id=None, video_id=None, video_note_id=None,
	                            document_id=None):
		if self.conn is None:
			await self.connect()

		existing_record = await self.execute_query('SELECT course_id FROM final_message WHERE course_id = ?',
		                                           (course_id,))
		if existing_record:
			query = '''
		            UPDATE final_message
		            SET text = ?, audio = ?, photo = ?, video = ?, video_note = ?, document = ?
		            WHERE course_id = ?
		        '''
			await self.execute_query(query, (text, audio_id, photo_id, video_id, video_note_id, document_id, course_id))
		else:
			query = '''
		            INSERT INTO final_message (course_id, text, audio, photo, video, video_note, document)
		            VALUES (?, ?, ?, ?, ?, ?, ?)
		        '''
			await self.execute_query(query, (course_id, text, audio_id, photo_id, video_id, video_note_id, document_id))

	async def update_final_message(self, course_id, text=None, audio=None, photo=None, video=None, video_note=None,
	                               document=None):
		if self.conn is None:
			await self.connect()

		query = '''
	        UPDATE final_message
	        SET
	            text = ?,
	            audio = ?,
	            photo = ?,
	            video = ?,
	            video_note = ?,
	            document = ?,
	        WHERE course_id = ?
	    '''
		await self.execute_query(query, (
			text, audio, photo, video, video_note, document, course_id
		))

	async def get_final_message(self, course_id):
		if self.conn is None:
			await self.connect()

		query = '''
	        SELECT text, audio, photo, video, video_note, document
	        FROM final_message
	        WHERE course_id = ?
	    '''
		result = await self.execute_query(query, (course_id,))
		print(course_id)
		print(result)
		if not result:
			return None

		return result[0]

	async def get_lesson_name(self, course_id, module_id, lesson_id):
		if self.conn is None:
			await self.connect()

		query = '''
	        SELECT lesson_title
	        FROM lessons
	        WHERE course_id = ? AND module_id = ? AND lesson_id = ?
	    '''
		result = await self.execute_query(query, (course_id, module_id, lesson_id))

		if not result:
			return None

		return result[0][0]

	async def update_lesson_name(self, course_id, module_id, lesson_id, lesson_name):
		if self.conn is None:
			await self.connect()

		query = """
			UPDATE lessons
			SET lesson_title = ?
			WHERE course_id = ?
			AND module_id = ?
			AND lesson_id = ?
		"""
		await self.execute_query(query, (lesson_name, course_id, module_id, lesson_id))

	async def minus_usage(self, promocode):

		result = await self.execute_query('''
	        SELECT usages_left
	        FROM promocodes
	        WHERE promocode = ?
	    ''', (promocode,))

		if result:
			current_usages_left = result[0][0]
			if current_usages_left > 0:
				new_usages_left = current_usages_left - 1

				# Обновляем значение в базе данных
				await self.execute_query('''
	                UPDATE promocodes
	                SET usages_left = ?
	                WHERE promocode = ?
	            ''', (new_usages_left, promocode))

				return True  # Операция успешно выполнена
			else:
				return False  # Нет доступных использований
		else:
			return False  # Промокод не найден

	async def is_n_promo(self, promocode):
		result = await self.execute_query('''
	        SELECT usages_left
	        FROM promocodes
	        WHERE promocode = ?
	    ''', (promocode,))

		if result:
			usages_left = result[0][0]
			if usages_left is not None:
				return True
			else:
				return False
		else:
			return False  # Промокод не найден

	async def is_group_promo(self, promocode):

		# Получаем информацию о промокоде
		result = await self.execute_query('''
	        SELECT chat_id
	        FROM promocodes
	        WHERE promocode = ?
	    ''', (promocode,))

		if result:
			promo_chat_id = result[0][0]
			# Проверяем, есть ли у промокода чат
			if promo_chat_id is not None:
				return True
			else:
				return False
		else:
			return False  # Промокод не найден
