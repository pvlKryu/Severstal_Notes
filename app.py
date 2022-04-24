from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy  # Подключение БД
from datetime import date, datetime
from werkzeug.utils import redirect  # Импорт функции реального времени
from sqlalchemy import func, text
# import bleach  # для защиты входных данных от "злых" скриптов

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'  # Создаем БД
db = SQLAlchemy(app)  # Запускаем БД


class Note(db.Model):  # создаем класс Заметка
    note_id = db.Column(db.Integer, primary_key=True)  # создаем поля
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # По запросу будет выдаваться объект + ID
        return '<Note %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/base')
def base():
    return render_template("base.html")


@app.route('/create_note', methods=['POST', 'GET'])
def create_note():
    if request.method == "POST":
        title = request.form['title']  # Заполняем поля из формы
        # text = request.form['text']
        text = request.form['editordata']
        # Создаем объект, заполняем поля, передавая переменные
        note = Note(title=title, text=text)
        try:  # Обрабатываем ошибки
            if title and text:  # Проверка на заполненность
                db.session.add(note)  # Добавляем объект
                db.session.commit()  # Сохраняем объект
                # Если успешно - переводим на главную страницy:
                return redirect('/notes')
            else:
                return "Заполните все поля"  # ДОДЕЛАТЬ КНОПКУ НАЗАД
        except:  # На случай ошибки
            return render_template("create_note.html")
        # traceback.format_exc() # Код ошибки

    else:
        return render_template("create_note.html")


@app.route('/notes')  # Все заметки
def notes():
    q = request.args.get('q')
    if q:
        notes = Note.query.filter(Note.title.contains(q) | Note.text.contains(
            q) | Note.note_id.contains(q)).all()
    else:
        # Выводим все записи из БД сортируя по дате:
        notes = Note.query.order_by(Note.date.desc()).all()
        # в шаблон передаем заметки
    return render_template("notes.html", notes=notes)


@app.route('/notes/<int:note_id>')  # Конкретная заметка
def note_detail(note_id):
    # Выводим все записи из БД сортируя по дате:
    note = Note.query.get(note_id)
    # в шаблон передаем список контрактов
    return render_template("note_detail.html", note=note)


@app.route('/notes/<int:note_id>/del')  # Удаление заметки
def note_delet(note_id):
    # Ищем нужную запись в БД:
    note = Note.query.get_or_404(note_id)
    try:
        db.session.delete(note)
        db.session.commit()
        return redirect('/notes')
    except:  # На случай ошибки
        return "There is a mistake while note deleting"


# Редактирование заметки
@app.route('/notes/<int:note_id>/update', methods=['POST', 'GET'])
def notes_update(note_id):
    note = Note.query.get(note_id)  # Ищем объект
    if request.method == "POST":
        note.title = request.form['title']  # Заполняем поля из формы
        note.text = request.form['editordata']
        try:  # Обрабатываем ошибки
            db.session.commit()  # Сохраняем объект
            return redirect('/notes')
        except:  # На случай ошибки
            return "There is a mistake while note editing"
    else:
        return render_template("note_update.html", note=note)


# @app.route('/healthy')
# def healthy():
#     db.engine.execute('SELECT 1')
#     return ''


if __name__ == "__main__":
    app.run(debug=True)
