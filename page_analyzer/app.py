from flask import Flask
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash,
    get_flashed_messages,
    abort,
)
from dotenv import load_dotenv
from .db import Database
from .validation import is_validat_url

import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.get('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post('/urls')
def urls_create():

    db = Database(DATABASE_URL)
    url = request.form.to_dict()['url'].strip()
    errors = is_validat_url(url)
    if errors:
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', url=url, messages=messages)
    url_by_name = db.get_url_by_name(url)

    if url_by_name:
        flash('Страница уже существует',  'info')
        return redirect(url_for('urls'))
    else:
        db.add_url(url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('urls'))


@app.get('/urls')
def urls():
    db = Database(DATABASE_URL)
    urls = db.get_urls()
    messages = get_flashed_messages(with_categories=True)
    return render_template('urls.html', urls=urls, messages=messages)


@app.get('/urls/<int:id>')
def url(id):
    messages = get_flashed_messages(with_categories=True)
    db = Database(DATABASE_URL)
    url = db.get_url(id)

    if not url:
        return abort(404)
    return render_template('url.html', url=url[0], messages=messages)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
