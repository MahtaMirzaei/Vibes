from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(100))
    profilepic = db.Column(db.LargeBinary)
    is_artist = db.Column(db.Boolean)
    is_premium = db.Column(db.Boolean)
    
@app.route('/')
def home():
    return "Welcome to Vibes!"

@app.route('/users', methods=['GET'])
def get_users():
    users = db.engine.execute('SELECT * FROM users').fetchall()
    users_list = []
    for user in users:
        users_list.append({
            'user_id': user['user_id'],
            'name': user['name'],
            'balance': user['balance'],
            'email': user['email'],
            'address': user['address'],
            'is_artist': user['is_artist'],
            'is_premium': user['is_premium']
        })
    return jsonify(users_list)

if __name__ == '__main__':
    app.run(debug=True)
