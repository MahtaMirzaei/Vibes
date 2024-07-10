from flask import Flask, render_template, request, url_for, redirect, flash
import sqlite3
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to the database and create the table with the new schema
with sqlite3.connect('database.db') as connect:
    connect.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            city TEXT,
            country TEXT,
            phone TEXT,
            age INTEGER,
            password TEXT,
            balance INTEGER DEFAULT 0,
            is_artist BOOLEAN DEFAULT 0,
            is_premium BOOLEAN DEFAULT 0
        )
    ''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        name = request.form['name']
        email = request.form['email']
        city = request.form['city']
        country = request.form['country']
        phone = request.form['phone']
        age = request.form['age']
        password = request.form['password']

        if not age.isdigit() or int(age) <= 8:
            flash('Age must be a positive integer greater than 8.')
            return redirect(url_for('join'))

        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("""
                INSERT INTO USERS (user_id, name, email, city, country, phone, age, password, balance, is_artist, is_premium)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0)
            """, (user_id, name, email, city, country, phone, age, password))
            users.commit()
        return render_template("index.html")
    else:
        return render_template('join.html')

@app.route('/participant')
def participants():
    with sqlite3.connect('database.db') as connect:
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM USERS')
        data = cursor.fetchall()
    return render_template("participants.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)
