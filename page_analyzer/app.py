from flask import Flask
from flask import render_template
from dotenv import load_dotenv
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html')
