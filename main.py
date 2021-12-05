from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'  # Указываем настройку, что используем БД shop.db
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)  # Создание объекта на основе класс SQLAlchemy, уточняем (app)


class Item(db.Model):  # Создаем класс для таблички, который наследуется от db.Model
    id = db.Column(db.Integer, primary_key=True)  # Перечисляем поля нашей таблицы. primary_key=True -автоматическое
    title = db.Column(db.String(100), nullable=False)  # проставление айди по порядку. nullable=False - непустое поле
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    # text = db.Column(db.Text, nullable=False)         # db.Text - не ограничивает до 250 симолов, можно больше

    def __repr__(self):
        return self.title


@app.route('/')  # Декоратор, ожидающий основную домашнюю страницу
def index():  # Функация, при попадания на домашнюю страницу
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилась ошибка =("
    else:
        return render_template('create.html')


if __name__ == "__main__":  # Если домашняя страница, то
    app.run(debug=True)  # запускаем сервер. debug=True - Ошибки сразу в браузере
