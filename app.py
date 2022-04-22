from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy  # Подключение БД
from datetime import date, datetime
from werkzeug.utils import redirect  # Импорт функции реального времени
from sqlalchemy import func, text

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return ("about.html")


@app.route('/base')
def base():
    return render_template("base.html")

# @app.route('/healthy')
# def healthy():
#     db.engine.execute('SELECT 1')
#     return ''


if __name__ == "__main__":
    app.run(debug=True)
