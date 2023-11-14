from flask import Flask
from flask import render_template
from dotenv import load_dotenv
import os
import psycopg2


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)


class DatabaseException(Exception):
    def __init__(self, message):
        self.message = message


def connect(config):
    try:
        conn = psycopg2.connect(config)
        return conn
    except psycopg2.Error as e:
        message = f'Can\'t connect to the database! Error: {e}'
        raise DatabaseException(message)


@app.get('/')
def index():
    a = connect(DATABASE_URL)
    print(a)
    return render_template('index.html')
