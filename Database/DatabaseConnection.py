import psycopg2
from playlist_gen.config import ENABLE_DATABASE, HOST, DATABASE, USER, PASSWORD, SCHEMA

class DatabaseConnection:
    def __init__(self):
        self.conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)

    def exit(self):
        self.conn.close()

    def query(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()
