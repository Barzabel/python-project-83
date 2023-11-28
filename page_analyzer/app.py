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
from .db import (
    add_url_checks,
    add_url,
    get_url_checks_by_id,
    get_all_urls,
    get_url_by_id,
    get_url_by_name
)
from .url import validate_url, extract_domain
from .parser import get_data
import os
import requests


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
    url = request.form.to_dict()['url'].strip()
    errors = validate_url(url)
    if errors:
        for text, category in errors:
            flash(text, category)
        return render_template('index.html', url=url), 422
    url = extract_domain(url)
    found_url = get_url_by_name(DATABASE_URL, url)

    if found_url:
        flash('Страница уже существует', 'info')
        id = found_url.id
        return redirect(url_for('url', id=id))
    else:
        id = add_url(DATABASE_URL, url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('url', id=id.id))


@app.get('/urls')
def urls():
    urls = get_all_urls(DATABASE_URL)
    return render_template('urls.html', urls=urls)


@app.get('/urls/<int:id>')
def url(id):
    url = get_url_by_id(DATABASE_URL, id)
    if not url:
        return abort(404)

    url_checks = get_url_checks_by_id(DATABASE_URL, id)
    return render_template(
        'url.html',
        url=url,
        url_checks=url_checks
    )


@app.post('/urls/<int:id>/checks')
def url_checks(id):
    url = get_url_by_id(DATABASE_URL, id)
    try:
        response = requests.get(url.name, timeout=3)
        response.raise_for_status()
        data = get_data(response.text)
        data['status_code'] = response.status_code
        data['url_id'] = id
        flash('Страница успешно проверена', 'success')
        add_url_checks(DATABASE_URL, data)
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
    finally:
        return redirect(url_for('url', id=id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
