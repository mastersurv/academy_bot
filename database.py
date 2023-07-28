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
        async with self.pool.acquire() as connection:
            # TODO: Создание таблиц (CREATE TABLE ...) для PostgreSQL
            pass
