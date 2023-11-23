from flask import Flask
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash,
    abort,
)
from dotenv import load_dotenv
from .db import Database_url, Database_url_checks
from .url import is_validat_url, get_clear_url
from .parser import get_data
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def urls_create():
    db_url = Database_url(DATABASE_URL)
    url = request.form.to_dict()['url'].strip()
    errors = is_validat_url(url)
    if errors:
        flash('Некорректный URL', 'danger')
        return render_template('index.html', url=url), 422
    url = get_clear_url(url)
    is_exist_url = db_url.get('name', url)

    if is_exist_url:
        flash('Страница уже существует',  'info')
        id = is_exist_url[0].id
        return redirect(url_for('url', id=id))
    else:
        id = db_url.add({'name': url})
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('url', id=id[0].id))


@app.get('/urls')
def urls():
    db_url = Database_url(DATABASE_URL)
    urls = db_url.get_urls()
    return render_template('urls.html', urls=urls)


@app.get('/urls/<int:id>')
def url(id):
    db_url = Database_url(DATABASE_URL)
    url = db_url.get('id', id)
    if not url:
        return abort(404)
    db_url_checks = Database_url_checks(DATABASE_URL)
    url_checks = db_url_checks.get('url_id', id, order_by='id', desc=True)
    return render_template(
        'url.html',
        url=url[0],
        url_checks=url_checks
    )


@app.post('/urls/<int:id>/checks')
def url_checks(id):
    db_url = Database_url(DATABASE_URL)
    url = db_url.get('id', id)[0]
    try:
        data = get_data(url.name)
        data['url_id'] = id
        db_url_checks = Database_url_checks(DATABASE_URL)
        db_url_checks.add(data)
        flash('Страница успешно проверена', 'success')
    except Exception as e:
        print(e)
        flash('Произошла ошибка при проверке', 'danger')
    finally:
        return redirect(url_for('url', id=id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
