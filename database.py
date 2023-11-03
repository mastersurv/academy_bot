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
                CREATE TABLE IF NOT EXISTS courses (
                    course_id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    short_description TEXT,
                    short_description_image VARCHAR(255),
                    description TEXT
                );
            ''')

			await connection.execute('''
                CREATE TABLE IF NOT EXISTS modules (
                    module_id SERIAL PRIMARY KEY,
                    course_id INT REFERENCES courses(course_id),
                    module_title VARCHAR(255),
                    module_description TEXT
                );
            ''')

			await connection.execute('''
                CREATE TABLE IF NOT EXISTS steps (
                    step_id SERIAL PRIMARY KEY,
                    module_id INT REFERENCES modules(module_id),
                    step_title VARCHAR(255),
                    step_description TEXT
                );
            ''')
