import pymysql
from pymysql.cursors import DictCursor

class MabinogiDbConnector:
    def __init__(self, host='localhost', port=51122, user='root', password='1234', db='mabinogi', charset='utf8mb4'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.conn = None

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                charset=self.charset,
                cursorclass=DictCursor
            )
            return self.conn
        except pymysql.Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def begin_transaction(self):
        if not self.conn:
            raise ConnectionError("Database not connected. Call connect() first.")
        self.conn.begin()

    def commit_transaction(self):
        if not self.conn:
            raise ConnectionError("Database not connected. Call connect() first.")
        self.conn.commit()

    def rollback_transaction(self):
        if not self.conn:
            raise ConnectionError("Database not connected. Call connect() first.")
        self.conn.rollback()

    def execute_query(self, query, params=None):
        if not self.conn:
            raise ConnectionError("Database not connected. Call connect() or use 'with' statement first.")
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except pymysql.Error as e:
            print(f"Error executing query: {e}")
            raise

    def execute_queries(self, query, params=None):
        if not self.conn:
            raise ConnectionError("Database not connected. Call connect() or use 'with' statement first.")
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except pymysql.Error as e:
            print(f"Error executing query: {e}")
            raise

    def execute_update(self, query, params=None):
        if not self.conn:
            raise ConnectionError("Database not connected. Call connect() or use 'with' statement first.")
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount
        except pymysql.Error as e:
            print(f"Error executing update: {e}")
            raise

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
