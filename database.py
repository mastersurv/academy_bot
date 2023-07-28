import psycopg2

class DataBase:
    def __init__(self, db_name, user, password, host, port):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.lastrow_id = None

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query, parameters=None):
        self.connect()
        cursor = self.conn.cursor()

        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)

        self.lastrow_id = cursor.lastrowid
        result = cursor.fetchall()

        self.conn.commit()
        cursor.close()

        return result

    def create_tables(self):
        self.connect()

        cursor = self.conn.cursor()

        # TODO: Создание таблиц (CREATE TABLE ...) для PostgreSQL

        self.conn.commit()
        self.disconnect()
