from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "panya_pay_secret_key"

users_db = {}
SYMBOLS = ['🍒', '🍋', '🍇', '🔔', '💎', '7️⃣']

@app.route('/')
def index():
    if 'user' in session and session['user'] in users_db:
        return render_template('game.html', user=users_db[session['user']])
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    phone = request.form.get('phone')
    name = request.form.get('name')
    if phone not in users_db:
        users_db[phone] = {'name': name, 'balance': 5000} # အစမ်း ၅ ထောင်ပေးမယ်
    session['user'] = phone
    return render_template('game.html', user=users_db[phone])

@app.route('/spin', methods=['POST'])
def spin():
    phone = session.get('user')
    if not phone or users_db[phone]['balance'] < 500:
        return jsonify({'error': 'ပိုက်ဆံကုန်သွားပြီ! ဒါဟာ လောင်းကစားရဲ့ နိဂုံးပဲ။'})

    users_db[phone]['balance'] -= 500
    
    # ပညာပေး logic - နိုင်ခြေ ၅% ပဲရှိမယ်
    is_win = random.random() < 0.05 
    if is_win:
        result = ['7️⃣', '7️⃣', '7️⃣']
        users_db[phone]['balance'] += 5000
    else:
        result = [random.choice(SYMBOLS) for _ in range(3)]
        if result[0] == result[1] == result[2]: # တိုက်ဆိုင်ပြီး တူသွားရင် တစ်ခုပြောင်းမယ်
            result[2] = '🍋'

    return jsonify({'result': result, 'balance': users_db[phone]['balance'], 'is_win': is_win})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)