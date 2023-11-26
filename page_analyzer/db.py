import psycopg2
from psycopg2.extras import NamedTupleCursor
from abc import ABC


class DatabaseException(Exception):
    def __init__(self, message):
        self.message = message


class Database(ABC):
    def __init__(self, config):
        try:
            self.conect = psycopg2.connect(config)
        except psycopg2.Error as e:
            message = f'Can\'t connect to the database! Error: {e}'
            raise DatabaseException(message)

    def __del__(self):
        self.conect.close()


class DatabaseUrl(Database):

    def get_urls(self):
        try:
            cursor = self.conect.cursor(cursor_factory=NamedTupleCursor)
            cursor.execute('SELECT urls.id, urls.name, urls.created_at, \
            urls_checks.status_code, urls_checks.created_at AS \
            urls_checks_created_at , MAX(urls_checks.url_id) \
            FROM urls LEFT JOIN urls_checks ON \
            urls.id=urls_checks.url_id GROUP BY \
            urls.id, urls.name, urls.created_at, urls_checks.status_code, \
            urls_checks.created_at ORDER BY urls.id DESC')
            result = cursor.fetchall()
            return result
        except psycopg2.Error as e:
            message = f'Can\'t get url from database! Error: {e}'
            raise DatabaseException(message)

    def add(self, url):
        try:
            cursor = self.conect.cursor(cursor_factory=NamedTupleCursor)
            cursor.execute(
                    'INSERT INTO urls (name) VALUES (%s) RETURNING id',
                    (str(url),))
            result = cursor.fetchone()
            self.conect.commit()
            return result
        except psycopg2.Error as e:
            message = f'Can\'t add url to database! Error: {e}'
            raise DatabaseException(message)

    def get_url_by_id(self, id):
        try:
            cursor = self.conect.cursor(cursor_factory=NamedTupleCursor)
            cursor .execute(
                'SELECT * FROM urls WHERE id = (%s)',
                (id,)
            )
            result = cursor.fetchone()
            return result
        except psycopg2.Error as e:
            message = f'Can\'t get url from database! Error: {e}'
            raise DatabaseException(message)

    def get_url_by_name(self, name):
        try:
            cursor = self.conect.cursor(cursor_factory=NamedTupleCursor)
            cursor.execute(
                'SELECT * FROM urls WHERE name = (%s)',
                (name,)
            )
            result = cursor.fetchone()
            return result
        except psycopg2.Error as e:
            message = f'Can\'t get url from database! Error: {e}'
            raise DatabaseException(message)


class DatabaseUrlChecks(Database):
    def add(self, data):
        try:
            cursor = self.conect.cursor(cursor_factory=NamedTupleCursor)
            cursor.execute(
                '''
                INSERT INTO urls_checks (url_id, status_code,
                h1, title, description)
                VALUES (%(url_id)s, %(status_code)s, %(h1)s,
                %(title)s, %(description)s)
                ''', data
            )
            self.conect.commit()
        except psycopg2.Error as e:
            message = f'Can\'t add url to database! Error: {e}'
            raise DatabaseException(message)

    def get_url_by_id(self, id):
        try:
            cursor = self.conect.cursor(cursor_factory=NamedTupleCursor)
            cursor.execute(
                'SELECT * FROM urls_checks \
                WHERE url_id = (%s) ORDER BY id DESC',
                (id,)
            )
            result = cursor.fetchall()
            return result
        except psycopg2.Error as e:
            message = f'Can\'t get url from database! Error: {e}'
            raise DatabaseException(message)
