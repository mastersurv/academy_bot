import sqlite3

class DataBase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.lastrow_id = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)

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

        # TODO создание таблиц CREATE TABLE ...


        self.conn.commit()
        self.disconnect()