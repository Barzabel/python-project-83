import psycopg2
from psycopg2.extras import NamedTupleCursor, RealDictCursor


class DatabaseException(Exception):
    def __init__(self, message):
        self.message = message


class Database:
    def __init__(self, config):
        try:
            self.conect = psycopg2.connect(config)
        except psycopg2.Error as e:
            message = f'Can\'t connect to the database! Error: {e}'
            raise DatabaseException(message)

    def __del__(self):
        self.conect.close()

    def add_url(self, url):
        try:
            cur = self.conect.cursor(cursor_factory=NamedTupleCursor)
            SQL = 'INSERT INTO urls (name) VALUES (%s) RETURNING id'
            cur.execute(
                    SQL,
                    (str(url),))
            result = cur.fetchall()
            self.conect.commit()
            return result
        except psycopg2.Error as e:
            message = f'Can\'t add url to database! Error: {e}'
            raise DatabaseException(message)

    def get_urls(self):
        try:
            cur = self.conect.cursor(cursor_factory=NamedTupleCursor)
            SQL = 'SELECT * FROM urls ORDER BY created_at DESC'
            cur.execute(SQL)
            result = cur.fetchall()
            return result
        except psycopg2.Error as e:
            message = f'Can\'t get url from database! Error: {e}'
            raise DatabaseException(message)

    def get_url(self, id):
        try:
            cur = self.conect.cursor(cursor_factory=NamedTupleCursor)
            SQL = 'SELECT * FROM urls WHERE id = (%s)'
            cur.execute(SQL, (id,))
            result = cur.fetchall()
            return result
        except psycopg2.Error as e:
            message = f'Can\'t get url from database! Error: {e}'
            raise DatabaseException(message)

    def get_url_by_name(self, name):
        try:
            cur = self.conect.cursor(cursor_factory=NamedTupleCursor)
            SQL = 'SELECT * FROM urls WHERE name = (%s)'
            cur.execute(SQL, (name,))
            result = cur.fetchall()
            return result
        except psycopg2.Error as e:
            message = f'Can\'t get url from database! Error: {e}'
            raise DatabaseException(message)
