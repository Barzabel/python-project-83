import psycopg2
from psycopg2.extras import NamedTupleCursor


class DatabaseException(Exception):
    def __init__(self, message):
        self.message = message


class Database_url:
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
            SQL = 'SELECT urls.id, urls.name, urls.created_at, \
            urls_checks.status_code, MAX(urls_checks.created_at) FROM urls\
            LEFT JOIN urls_checks ON urls.id=urls_checks.url_id GROUP BY \
            urls.id, urls.name, urls.created_at, urls_checks.status_code, \
            urls_checks.created_at ORDER BY urls.created_at DESC'

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


class Database_url_checks:
    def __init__(self, config):
        try:
            self.conect = psycopg2.connect(config)
        except psycopg2.Error as e:
            message = f'Can\'t connect to the database! Error: {e}'
            raise DatabaseException(message)

    def __del__(self):
        self.conect.close()

    def add_url_checks(self, url_id):
        try:
            cur = self.conect.cursor(cursor_factory=NamedTupleCursor)
            SQL = 'INSERT INTO urls_checks (url_id) VALUES (%s) RETURNING id'
            cur.execute(
                    SQL,
                    (str(url_id),))
            result = cur.fetchall()
            self.conect.commit()
            return result
        except psycopg2.Error as e:
            message = f'Can\'t add url to database! Error: {e}'
            raise DatabaseException(message)

    def get_url(self, id):
        try:
            cur = self.conect.cursor(cursor_factory=NamedTupleCursor)
            SQL = 'SELECT * FROM urls_checks WHERE url_id = (%s)'
            cur.execute(SQL, (id,))
            result = cur.fetchall()
            return result
        except psycopg2.Error as e:
            message = f'Can\'t get url from database! Error: {e}'
            raise DatabaseException(message)
