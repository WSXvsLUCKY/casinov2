from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random
from collections import deque

app = Flask(__name__)
CORS(app)

# База данных в памяти
users_db = {}

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.balance = 1000
        self.history = deque(maxlen=10)
        self.current_bet = 0
        self.auto_cashout = 2.0

# Главное меню
# Явный обработчик для корневого URL
@app.route('/')
def index():
    return render_template('menu.html')  # Убедитесь, что menu.html существует

@app.route('/aviator')
def aviator():
    return render_template('aviator.html')

# Игра Мины (заглушка)
@app.route('/mines')
def mines():
    return render_template('mines.html')

# API для Авиатора
@app.route('/api/init', methods=['POST'])
def api_init():
    data = request.get_json()
    user_id = str(data['user']['id'])
    
    if user_id not in users_db:
        users_db[user_id] = User(user_id)
    
    user = users_db[user_id]
    return jsonify({
        'balance': user.balance,
        'history': list(user.history),
        'auto_cashout': user.auto_cashout
    })

@app.route('/api/bet', methods=['POST'])
def api_bet():
    data = request.get_json()
    user_id = str(data['user']['id'])
    bet_amount = int(data['bet_amount'])
    
    if user_id not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    user = users_db[user_id]
    
    if user.balance < bet_amount:
        return jsonify({'error': 'Not enough balance'}), 400
    
    user.balance -= bet_amount
    user.current_bet = bet_amount
    crash_point = round(random.uniform(1.1, 10.0), 2)
    
    return jsonify({
        'balance': user.balance,
        'crash_point': crash_point
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)