import psycopg2
from psycopg2.extras import NamedTupleCursor
from abc import ABC, abstractmethod


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

    @property
    @abstractmethod
    def filds(self):
        pass

    @property
    @abstractmethod
    def table_name(self):
        pass

    def add(self, data):
        res = []
        for fild in self.filds:
            res.append('%({})s'.format(fild))
        VALUE_FILDS = ", ".join(res)
        FILDS = ", ".join(self.filds)
        TABLE_NAME = self.table_name
        try:
            cursor = self.conect.cursor(cursor_factory=NamedTupleCursor)
            cursor.execute(
                f'''
                INSERT INTO {TABLE_NAME} ({FILDS})
                VALUES ({VALUE_FILDS}) RETURNING id
                ''', data
            )
            result = cursor.fetchall()
            self.conect.commit()
            return result
        except psycopg2.Error as e:
            message = f'Can\'t add url to database! Error: {e}'
            raise DatabaseException(message)

    def get(self, field, value, order_by=None, desc=False, one_element=False):
        ORDER_BY = ''
        if order_by:
            SC = 'DESC' if desc else 'ASC'
            ORDER_BY = f'ORDER BY {order_by} {SC}'
        TABLE_NAME = self.table_name
        try:
            cursor = self.conect.cursor(cursor_factory=NamedTupleCursor)
            SQL = f'SELECT * FROM {TABLE_NAME} WHERE {field} = (%s) {ORDER_BY}'
            cursor.execute(SQL, (value,))
            result = cursor.fetchone() if one_element else cursor.fetchall()
            return result
        except psycopg2.Error as e:
            message = f'Can\'t get url from database! Error: {e}'
            raise DatabaseException(message)

    def __del__(self):
        self.conect.close()


class Database_url(Database):
    @property
    def table_name(self):
        return "urls"

    @property
    def filds(self):
        return ['name']

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


class Database_url_checks(Database):
    @property
    def table_name(self):
        return "urls_checks"

    @property
    def filds(self):
        return ['url_id', 'status_code', 'h1', 'title', 'description']
