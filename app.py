from flask import Flask, render_template, request, url_for, redirect, flash
import sqlite3
import random
import string

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Connect to the database and create the table with the new schema
with sqlite3.connect("database.db") as connect:
    connect.execute(
        """
        CREATE TABLE IF NOT EXISTS USERS (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            city TEXT,
            country TEXT,
            phone TEXT,
            age INTEGER CHECK(age >= 9 AND age <= 120),
            password TEXT,
            balance INTEGER DEFAULT 0,
            is_artist BOOLEAN DEFAULT 0,
            is_premium BOOLEAN DEFAULT 0
        )
    """
    )


with sqlite3.connect("database.db") as connect:
    connect.execute(
        """
        CREATE TABLE IF NOT EXISTS ALBUM (
            album_id INT PRIMARY KEY,
            name TEXT,
            release_date DATE,
            genre TEXT
        )
        """
    )

with sqlite3.connect("database.db") as connect:
    connect.execute(
        """
        CREATE TABLE IF NOT EXISTS SONGS (
            song_id INT PRIMARY KEY,
            artist_id INT DEFAULT 0,
            album_id INT DEFAULT 0,
            name TEXT,
            file TEXT,
            lyrics TEXT,
            release_date DATE,
            age_rating INTEGER CHECK(age_rating >= 9 AND age_rating <= 120),
            genre TEXT,
            duration INTEGER,
            is_limited BOOLEAN DEFAULT 0,
            FOREIGN KEY(album_id) REFERENCES album(album_id)
        )
    """
    )

with sqlite3.connect("database.db") as songs:
    cursor = songs.cursor()
    cursor.execute(
        """
        INSERT INTO SONGS ( artist_id, album_id, name, file, lyrics, release_date, age_rating, genre, duration, is_limited)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (13, 14, 'Try Everything', 'None', 'None', '2018-09-11', 12, 'happy', 1234, 0)
    )
    songs.commit()

# :)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        user_id = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        name = request.form["name"]
        email = request.form["email"]
        city = request.form["city"]
        country = request.form["country"]
        phone = request.form["phone"]
        age = request.form["age"]
        password = request.form["password"]

        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute(
                """
                INSERT INTO USERS (user_id, name, email, city, country, phone, age, password, balance, is_artist, is_premium)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0)
            """,
                (user_id, name, email, city, country, phone, age, password),
            )
            users.commit()
        return render_template("index.html")
    else:
        return render_template("join.html")


        


@app.route("/participant")
def participants():
    with sqlite3.connect("database.db") as connect:
        cursor = connect.cursor()

        cursor.execute("SELECT * FROM USERS")
        data = cursor.fetchall()

        cursor.execute("SELECT * FROM SONGS")
        song_data = cursor.fetchall()

    return render_template("participants.html", data=data, song_data=song_data)


if __name__ == "__main__":
    app.run(debug=True)
