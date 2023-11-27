import psycopg2
from psycopg2.extras import NamedTupleCursor


class DatabaseException(Exception):
    def __init__(self, message):
        self.message = message


def get_connect(config):
    try:
        conect = psycopg2.connect(config)
        return conect
    except psycopg2.Error as e:
        message = f'Can\'t connect to the database! Error: {e}'
        raise DatabaseException(message)


def add_url_checks(config, data):
    with get_connect(config) as conect:
        cursor = conect.cursor(cursor_factory=NamedTupleCursor)
        cursor.execute(
            '''
            INSERT INTO urls_checks (url_id, status_code,
            h1, title, description)
            VALUES (%(url_id)s, %(status_code)s, %(h1)s,
            %(title)s, %(description)s)
            ''', data
        )
        conect.commit()


def get_url_checks_by_id(config, id):
    with get_connect(config) as conect:
        cursor = conect.cursor(cursor_factory=NamedTupleCursor)
        cursor.execute(
            'SELECT * FROM urls_checks \
            WHERE url_id = (%s) ORDER BY id DESC',
            (id,)
        )
        result = cursor.fetchall()
        return result


def get_all_urls(config):
    with get_connect(config) as conect:
        cursor = conect.cursor(cursor_factory=NamedTupleCursor)
        cursor.execute('SELECT urls.id, urls.name, urls.created_at, \
        urls_checks.status_code, urls_checks.created_at AS \
        urls_checks_created_at , MAX(urls_checks.url_id) \
        FROM urls LEFT JOIN urls_checks ON \
        urls.id=urls_checks.url_id GROUP BY \
        urls.id, urls.name, urls.created_at, urls_checks.status_code, \
        urls_checks.created_at ORDER BY urls.id DESC')
        result = cursor.fetchall()
        return result


def add_url(config, url):
    with get_connect(config) as conect:
        cursor = conect.cursor(cursor_factory=NamedTupleCursor)
        cursor.execute(
            'INSERT INTO urls (name) VALUES (%s) RETURNING id',
            (str(url),)
        )
        result = cursor.fetchone()
        conect.commit()
        return result


def get_url_by_id(config, id):
    with get_connect(config) as conect:
        cursor = conect.cursor(cursor_factory=NamedTupleCursor)
        cursor .execute(
            'SELECT * FROM urls WHERE id = (%s)',
            (id,)
        )
        result = cursor.fetchone()
        return result


def get_url_by_name(config, name):
    with get_connect(config) as conect:
        cursor = conect.cursor(cursor_factory=NamedTupleCursor)
        cursor.execute(
            'SELECT * FROM urls WHERE name = (%s)',
            (name,)
        )
        result = cursor.fetchone()
        return result
