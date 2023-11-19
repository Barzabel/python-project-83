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
from .db import Database_url, Database_url_checks
from .validation import is_validat_url
from .parser import Parser
import os
import re

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

    db_url = Database_url(DATABASE_URL)
    url = request.form.to_dict()['url'].strip()
    pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}"
    url = re.search(pattern, url)[0]
    errors = is_validat_url(url)
    if errors:
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', url=url, messages=messages)
    url_by_name = db_url.get_url_by_name(url)

    if url_by_name:
        flash('Страница уже существует',  'info')
        return redirect(url_for('urls'))
    else:
        db_url.add_url(url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('urls'))


@app.get('/urls')
def urls():
    db_url = Database_url(DATABASE_URL)
    urls = db_url.get_urls()
    messages = get_flashed_messages(with_categories=True)
    return render_template('urls.html', urls=urls, messages=messages)


@app.get('/urls/<int:id>')
def url(id):
    messages = get_flashed_messages(with_categories=True)
    db_url = Database_url(DATABASE_URL)
    url = db_url.get_url(id)
    if not url:
        return abort(404)
    db_url_checks = Database_url_checks(DATABASE_URL)
    url_checks = db_url_checks.get_url(id)
    return render_template(
        'url.html',
        url=url[0],
        url_checks=url_checks,
        messages=messages
    )


@app.post('/urls/<int:id>/checks')
def url_checks(id):
    db_url = Database_url(DATABASE_URL)
    url = db_url.get_url(id)[0]
    try:
        data = Parser(url.name)
        status_code = data.get_status()
        if int(status_code) > 299:
            flash('Произошла ошибка при проверке', 'danger')
        else:
            flash('Страница успешно проверена', 'success')
        db_url_checks = Database_url_checks(DATABASE_URL)
        db_url_checks.add_url_checks(id, status_code)
    except: # noqa E722
        flash('Произошла ошибка при проверке', 'danger')
    finally:
        return redirect(url_for('url', id=id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
