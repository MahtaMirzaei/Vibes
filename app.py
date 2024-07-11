from flask import Flask, render_template, request, url_for, redirect, flash, session
import sqlite3
import random
import string
import datetime
import logging

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Connect to the database and create the tables with the new schema
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

    connect.execute(
        """
        CREATE TABLE IF NOT EXISTS ALBUM (
            album_id TEXT PRIMARY KEY,
            name TEXT,
            released_date DATE,
            genre TEXT
        )
    """
    )

    connect.execute(
        """
        CREATE TABLE IF NOT EXISTS SONGS (
            song_id TEXT PRIMARY KEY,
            user_id TEXT,
            album_id TEXT,
            name TEXT,
            file TEXT,
            lyrics TEXT,
            released_date DATE,
            age_rating INTEGER CHECK(age_rating >= 9 AND age_rating <= 120),
            genre TEXT,
            duration INTEGER,
            is_limited BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES USERS (user_id),
            FOREIGN KEY (album_id) REFERENCES ALBUM (album_id)
        )
    """
    )
    connect.execute(
        """
        CREATE TABLE IF NOT EXISTS TRANSACTIONS (
            transaction_id TEXT PRIMARY KEY,
            user_id TEXT,
            recipient_id TEXT,
            amount INTEGER,
            date DATE,
            FOREIGN KEY (user_id) REFERENCES USERS (user_id),
            FOREIGN KEY (recipient_id) REFERENCES USERS (user_id)
        )
    """
    )
    connect.execute(
                """
                CREATE TABLE IF NOT EXISTS concerts (
                    concert_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date DATE NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    ticket_number INTEGER NOT NULL,
                    user_id TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES USERS (user_id)
                )
                """
    )
    connect.execute(
        """
        INSERT OR IGNORE  INTO USERS (user_id, name, email, city, country, phone, age, password, balance, is_artist, is_premium)
        VALUES (1, 'admin', 'a@mail.com' , 'Isfahan', 'Iran', 1212, 100, 123123, 99999999999, 1, 1)
    """
    )

    connect.execute(
        """
        INSERT OR IGNORE  INTO USERS (user_id, name, email, city, country, phone, age, password, balance, is_artist, is_premium)
        VALUES (2, 'singer', 'a@mail.com' , 'Isfahan', 'Iran', 1212, 100, 123123, 99999999999, 1, 1)
    """
    )

    connect.execute(
        """
        INSERT OR IGNORE  INTO SONGS (album_id, name, released_date, genre)
        VALUES (3, 'Zootopia', 2016-08-12 , 'happy')
    """
    )
    
    connect.execute(
        """
        INSERT OR IGNORE  INTO SONGS (song_id, user_id, album_id, name, file, lyrics, released_date, age_rating, genre, duration, is_limited)
        VALUES (1, 2, 3 , 'Try Everything', 'Iran', '1212', 2016-08-12, 20, 'happy', 1, 0)
    """
    )

    connect.execute(
        """
        INSERT OR IGNORE  INTO USERS (user_id, name, email, city, country, phone, age, password, balance, is_artist, is_premium)
        VALUES (2, 'bank', 'b@mail.com' , 'Isfahan', 'Iran', 1010, 25, 123123, 0, 1, 1)
    """
    )
    connect.execute(
        """
        INSERT OR IGNORE  INTO TRANSACTIONS (transaction_id, user_id, recipient_id, date, amount)
        VALUES ('0', '1', '2', '2/2/2', 1000 )
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
        return render_template("login.html")
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
logging.basicConfig(level=logging.DEBUG)

@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if request.method == "POST":
        user_id = request.form["user_id"]
        recipient_id = request.form["recipient_id"]
        amount = int(request.form["amount"])
        transaction_id = "".join(random.choices(string.ascii_letters + string.digits, k=12))
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()

                # Verify sender and recipient exist and have sufficient balance
                cursor.execute("SELECT balance FROM USERS WHERE user_id = ?", (user_id,))
                sender_balance = cursor.fetchone()

                cursor.execute("SELECT balance FROM USERS WHERE user_id = ?", (recipient_id,))
                recipient_balance = cursor.fetchone()

                if not sender_balance or not recipient_balance:
                    flash("Invalid user ID or recipient ID")
                    return redirect(url_for("transfer"))

                if sender_balance[0] < amount:
                    flash("Insufficient balance")
                    return redirect(url_for("transfer"))

                # Perform the transaction
                new_sender_balance = sender_balance[0] - amount
                new_recipient_balance = recipient_balance[0] + amount

                cursor.execute("UPDATE USERS SET balance = ? WHERE user_id = ?", (new_sender_balance, user_id))
                cursor.execute("UPDATE USERS SET balance = ? WHERE user_id = ?", (new_recipient_balance, recipient_id))

                # Insert the transaction record
                cursor.execute(
                    """
                    INSERT INTO TRANSACTIONS (transaction_id, user_id, recipient_id, amount, date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (transaction_id, user_id, recipient_id, amount, date),
                )
                connect.commit()

                # Log success
                logging.info(f"Transfer successful: {amount} units from {user_id} to {recipient_id}")

            flash("Transfer successful!")
            return redirect(url_for("index"))

        except sqlite3.Error as e:
            logging.error(f"SQLite error during transfer: {e}")
            flash("Database error occurred. Please try again later.")
            return redirect(url_for("transfer"))

        except Exception as e:
            logging.error(f"Error during transfer: {e}")
            flash("An error occurred during the transfer.")
            return redirect(url_for("transfer"))

    else:
        return render_template("transfer.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with sqlite3.connect("database.db") as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM USERS WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()

            if user:
                session["user_id"] = user[0]
                session["name"] = user[1]
                session["balance"] = user[8]
                session["is_artist"] = user[9]
                session["is_premium"] = user[10]
                return redirect(url_for("user"))
            else:
                flash("Invalid email or password")
                return redirect(url_for("login"))
    else:
        return render_template("login.html")

@app.route("/user")
def user():
    if "user_id" in session:
        user_id = session["user_id"]
        name = session["name"]
        balance = session["balance"]
        is_premium = session["is_premium"]
        is_artist = session["is_artist"]

        return render_template("user.html", user_id=user_id, name=name, balance=balance, is_premium=is_premium, is_artist=is_artist)
    else:
        return redirect(url_for("login"))

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_category = request.form["search_category"]
        search_input = request.form["search_input"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        if search_category == "song_name":
            c.execute("SELECT name, user_id, age_rating, genre FROM songs WHERE name LIKE ? LIMIT 5", ("%"+search_input+"%",))
        elif search_category == "artist":
            c.execute("""
                SELECT s.name, u.name, s.age_rating, s.genre
                FROM songs s
                JOIN users u ON s.user_id = u.user_id
                WHERE u.name LIKE ?
                LIMIT 5
            """, ("%"+search_input+"%",))
        elif search_category == "age":
            c.execute("SELECT name, user_id, age_rating, genre FROM songs WHERE age_rating LIKE ? LIMIT 5", ("%"+search_input+"%",))
        elif search_category == "genre":
            c.execute("SELECT name, user_id, age_rating, genre FROM songs WHERE genre LIKE ? LIMIT 5", ("%"+search_input+"%",))

        results = c.fetchall()
        conn.close()

        data = [{"song_name": row[0], "artist": row[1], "age": row[2], "genre": row[3]} for row in results]

        return render_template("search.html", data=data)

    return render_template("search.html")

@app.route("/artist_page", methods=["GET", "POST"])
def artist_page():
    if "user_id" in session and session.get("is_artist"):
        user_id = session["user_id"]

        if request.method == "POST":
            action = request.form["action"]

            if action == "add":
                name = request.form["name"]
                date = request.form["date"]
                price = request.form["price"]
                ticket_number = request.form["ticket_number"]

                try:
                    with sqlite3.connect("database.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(
                            "INSERT INTO concerts (name, date, price, ticket_number, user_id) VALUES (?, ?, ?, ?, ?)",
                            (name, date, price, ticket_number, user_id),
                        )
                        connect.commit()
                        flash("Concert successfully added.")
                except Exception as e:
                    logging.error(f"Error adding concert: {e}")
                    flash("An error occurred while adding the concert.")

            elif action == "delete":
                concert_id = request.form["concert_id"]

                try:
                    with sqlite3.connect("database.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(
                            "DELETE FROM concerts WHERE concert_id = ? AND user_id = ?", (concert_id, user_id)
                        )
                        connect.commit()
                        flash("Concert successfully deleted.")
                except Exception as e:
                    logging.error(f"Error deleting concert: {e}")
                    flash("An error occurred while deleting the concert.")

        try:
            with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT concert_id, name, date, price, ticket_number FROM concerts WHERE user_id = ?", (user_id,))
                concerts = cursor.fetchall()

            return render_template("artist.html", concerts=concerts, user_id=user_id)

        except Exception as e:
            logging.error(f"Error fetching artist page: {e}")
            flash("An error occurred while fetching the artist page.")
            return redirect(url_for("user"))
    else:
        flash("Access denied: You are not an artist.")
        return redirect(url_for("user"))
    
@app.route("/charge", methods=["POST"])
def charge():
    if "user_id" in session:
        amount = int(request.form["amount"])

        if amount <= 0:
            flash("Amount must be a positive integer")
            return redirect(url_for("user"))

        user_id = session["user_id"]
        bank_id = "2"  # Assuming bank's user_id is 2
        transaction_id_user = "".join(random.choices(string.ascii_letters + string.digits, k=12))
        transaction_id_bank = "".join(random.choices(string.ascii_letters + string.digits, k=12))
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()

                # Update user's balance
                cursor.execute("UPDATE USERS SET balance = balance + ? WHERE user_id = ?", (amount, user_id))

                # Deduct the same amount from bank's balance
                cursor.execute("UPDATE USERS SET balance = balance - ? WHERE user_id = ?", (amount, bank_id))

                # Insert transaction records for user and bank
                cursor.execute(
                    """
                    INSERT INTO TRANSACTIONS (transaction_id, user_id, recipient_id, amount, date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (transaction_id_user, user_id, bank_id, amount, date)
                )

                cursor.execute(
                    """
                    INSERT INTO TRANSACTIONS (transaction_id, user_id, recipient_id, amount, date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (transaction_id_bank, bank_id, user_id, -amount, date)
                )

                connect.commit()

                session["balance"] += amount
                flash(f"You successfully charged {amount} to your account.")
                return redirect(url_for("user"))

        except sqlite3.Error as e:
            logging.error(f"SQLite error during charge: {e}")
            flash("Database error occurred. Please try again later.")
            return redirect(url_for("user"))

        except Exception as e:
            logging.error(f"Error during charge: {e}")
            flash("An error occurred during charging your account.")
            return redirect(url_for("user"))

    else:
        return redirect(url_for("login"))

    
@app.route("/premium", methods=["POST"])
def premium():
    if "user_id" in session:
        user_id = session["user_id"]
        admin_id = "1"  # Assuming admin's user_id is 1
        transaction_id_user = "".join(random.choices(string.ascii_letters + string.digits, k=12))
        transaction_id_admin = "".join(random.choices(string.ascii_letters + string.digits, k=12))
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        premium_cost = 1000

        if session["balance"] < premium_cost:
            flash("You don't have enough credit, please charge first.")
            return redirect(url_for("user"))

        try:
            with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()

                # Deduct premium cost from user's balance
                cursor.execute("UPDATE USERS SET balance = balance - ? WHERE user_id = ?", (premium_cost, user_id))

                # Add premium cost to admin's balance
                cursor.execute("UPDATE USERS SET balance = balance + ? WHERE user_id = ?", (premium_cost, admin_id))

                # Update user's premium status
                cursor.execute("UPDATE USERS SET is_premium = 1 WHERE user_id = ?", (user_id,))

                # Insert transaction records for user and admin
                cursor.execute(
                    """
                    INSERT INTO TRANSACTIONS (transaction_id, user_id, recipient_id, amount, date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (transaction_id_user, user_id, admin_id, -premium_cost, date)
                )

                cursor.execute(
                    """
                    INSERT INTO TRANSACTIONS (transaction_id, user_id, recipient_id, amount, date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (transaction_id_admin, admin_id, user_id, premium_cost, date)
                )

                connect.commit()

                session["balance"] -= premium_cost
                session["is_premium"] = 1
                flash("Congratulations! You are now a premium member.")
                return redirect(url_for("user"))

        except sqlite3.Error as e:
            logging.error(f"SQLite error during premium purchase: {e}")
            flash("Database error occurred. Please try again later.")
            return redirect(url_for("user"))

        except Exception as e:
            logging.error(f"Error during premium purchase: {e}")
            flash("An error occurred during purchasing premium membership.")
            return redirect(url_for("user"))

    else:
        return redirect(url_for("login"))
    

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True)