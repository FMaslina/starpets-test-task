import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from helpers import fetch_weather

# Инициализация БД
db = SQLAlchemy()

# Инициализация приложения
app = Flask(__name__)

# Настройки для подключения к базе данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format('users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем расширение SQLAlchemy
db.init_app(app)


# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)

    def __init__(self, username, balance):
        self.username = username
        self.balance = balance

    # Сохранение в базу
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Обновление записи в базе
    def update_to_db(self):
        db.session.commit()

    # Получение записи по ID
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)


with app.app_context():
    if not os.path.exists('users.db'):
        # Создаем все таблицы, определенные в моделях
        db.create_all()

        sample_users = [('Алиса', 10000), ('Денис', 5000), ('Кирилл', 12000), ('Лена', 8000), ('Ева', 7000)]

        # Создаем тестовые данные
        for username, balance in sample_users:
            user_obj = User(username=username, balance=balance)
            db.session.add(user_obj)
        db.session.commit()


# Запрос на обновление баланса
@app.route('/update_balance', methods=['POST'])
def update_balance():
    data = request.get_json()
    user_id = data['userId']
    city = data['city']

    temperature = fetch_weather(city)
    if temperature is None:
        return jsonify({'error': "Ошибка при получении температуры"}), 400

    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'Пользователь не найден'}), 400

    new_balance = user.balance + temperature
    if new_balance < 0:
        return jsonify({'error': 'Баланс пользователя не может быть отрицательным'}), 400

    user.balance = new_balance
    db.session.commit()

    return jsonify({'message': 'Баланс обновлён успешно'})


if __name__ == '__main__':
    app.run(debug=True)
