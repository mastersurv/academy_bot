from sqlite3 import connect


class Database:
    def __init__(self, db_name):
        self.connection = connect(db_name)
        self.cursor = self.connection.cursor()