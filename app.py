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
        CREATE TABLE IF NOT EXISTS TRANSACTIONS (
            transaction_id TEXT PRIMARY KEY,
            user_id TEXT,
            recipient_id TEXT,
            amount INTEGER,
            date TEXT,
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
                    date TEXT NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    ticket_number INTEGER NOT NULL,
                    user_id TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES USERS (user_id)
                )
                """
    )
    connect.execute(
        """
            CREATE TABLE IF NOT EXISTS ALBUM (
                album_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                release_date DATE,
                genre TEXT,
                user_id TEXT,
                FOREIGN KEY (user_id) REFERENCES USERS (user_id)
            )
            """
    )
    connect.execute(
        """
            CREATE TABLE IF NOT EXISTS SONGS (
                song_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                file TEXT,
                lyrics TEXT,
                release_date DATE,
                age_rating INTEGER CHECK(age_rating >= 9 AND age_rating <= 120),
                genre TEXT,
                duration INTEGER,
                is_limited BOOLEAN DEFAULT 0,
                album_id INTEGER,
                user_id TEXT,
                FOREIGN KEY (album_id) REFERENCES ALBUM (album_id),
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
        VALUES (2, 'bank', 'b@mail.com' , 'Isfahan', 'Iran', 1010, 25, 123123, 0, 1, 1)
    """
    )
    connect.execute(
        """
        INSERT OR IGNORE  INTO TRANSACTIONS (transaction_id, user_id, recipient_id, date, amount)
        VALUES ('0', '1', '2', '2/2/2', 1000 )
    """
    )


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
    return render_template("participants.html", data=data)


logging.basicConfig(level=logging.DEBUG)


@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if request.method == "POST":
        user_id = request.form["user_id"]
        recipient_id = request.form["recipient_id"]
        amount = int(request.form["amount"])
        transaction_id = "".join(
            random.choices(string.ascii_letters + string.digits, k=12)
        )
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()

                # Verify sender and recipient exist and have sufficient balance
                cursor.execute(
                    "SELECT balance FROM USERS WHERE user_id = ?", (user_id,)
                )
                sender_balance = cursor.fetchone()

                cursor.execute(
                    "SELECT balance FROM USERS WHERE user_id = ?", (recipient_id,)
                )
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

                cursor.execute(
                    "UPDATE USERS SET balance = ? WHERE user_id = ?",
                    (new_sender_balance, user_id),
                )
                cursor.execute(
                    "UPDATE USERS SET balance = ? WHERE user_id = ?",
                    (new_recipient_balance, recipient_id),
                )

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
                logging.info(
                    f"Transfer successful: {amount} units from {user_id} to {recipient_id}"
                )

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
            cursor.execute(
                "SELECT * FROM USERS WHERE email = ? AND password = ?",
                (email, password),
            )
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

        return render_template(
            "user.html",
            user_id=user_id,
            name=name,
            balance=balance,
            is_premium=is_premium,
            is_artist=is_artist,
        )
    else:
        return redirect(url_for("login"))


@app.route("/charge", methods=["POST"])
def charge():
    if "user_id" in session:
        amount = int(request.form["amount"])

        if amount <= 0:
            flash("Amount must be a positive integer")
            return redirect(url_for("user"))

        user_id = session["user_id"]
        bank_id = "2"  # Assuming bank's user_id is 2
        transaction_id_user = "".join(
            random.choices(string.ascii_letters + string.digits, k=12)
        )
        transaction_id_bank = "".join(
            random.choices(string.ascii_letters + string.digits, k=12)
        )
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()

                # Update user's balance
                cursor.execute(
                    "UPDATE USERS SET balance = balance + ? WHERE user_id = ?",
                    (amount, user_id),
                )

                # Deduct the same amount from bank's balance
                cursor.execute(
                    "UPDATE USERS SET balance = balance - ? WHERE user_id = ?",
                    (amount, bank_id),
                )

                # Insert transaction records for user and bank
                cursor.execute(
                    """
                    INSERT INTO TRANSACTIONS (transaction_id, user_id, recipient_id, amount, date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (transaction_id_user, user_id, bank_id, amount, date),
                )

                cursor.execute(
                    """
                    INSERT INTO TRANSACTIONS (transaction_id, user_id, recipient_id, amount, date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (transaction_id_bank, bank_id, user_id, -amount, date),
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
        transaction_id_user = "".join(
            random.choices(string.ascii_letters + string.digits, k=12)
        )
        transaction_id_admin = "".join(
            random.choices(string.ascii_letters + string.digits, k=12)
        )
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        premium_cost = 1000

        if session["balance"] < premium_cost:
            flash("You don't have enough credit, please charge first.")
            return redirect(url_for("user"))

        try:
            with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()

                # Deduct premium cost from user's balance
                cursor.execute(
                    "UPDATE USERS SET balance = balance - ? WHERE user_id = ?",
                    (premium_cost, user_id),
                )

                # Add premium cost to admin's balance
                cursor.execute(
                    "UPDATE USERS SET balance = balance + ? WHERE user_id = ?",
                    (premium_cost, admin_id),
                )

                # Update user's premium status
                cursor.execute(
                    "UPDATE USERS SET is_premium = 1 WHERE user_id = ?", (user_id,)
                )

                # Insert transaction records for user and admin
                cursor.execute(
                    """
                    INSERT INTO TRANSACTIONS (transaction_id, user_id, recipient_id, amount, date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (transaction_id_user, user_id, admin_id, -premium_cost, date),
                )

                cursor.execute(
                    """
                    INSERT INTO TRANSACTIONS (transaction_id, user_id, recipient_id, amount, date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (transaction_id_admin, admin_id, user_id, premium_cost, date),
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

@app.route("/artist_page", methods=["GET", "POST"])
def artist_page():
    if "user_id" in session and session.get("is_artist"):
        user_id = session["user_id"]

        if request.method == "POST":
            action = request.form["action"]

            if action == "add_concert":
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

            elif action == "delete_concert":
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

            elif action == "add_song":
                song_name = request.form["song_name"]
                file = request.form["file"]
                lyrics = request.form["lyrics"]
                release_date = request.form["release_date"]
                age_rating = request.form["age_rating"]
                genre = request.form["genre"]
                duration = request.form["duration"]
                album_id = request.form["album_id"]

                try:
                    with sqlite3.connect("database.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(
                            """
                            INSERT INTO songs (name, file, lyrics, release_date, age_rating, genre, duration, album_id, user_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (song_name, file, lyrics, release_date, age_rating, genre, duration, album_id, user_id),
                        )
                        connect.commit()
                        flash("Song successfully added.")
                except Exception as e:
                    logging.error(f"Error adding song: {e}")
                    flash("An error occurred while adding the song.")
            elif action == "delete_song":
                song_id = request.form["song_id"]

                try:
                    with sqlite3.connect("database.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(
                            "DELETE FROM songs WHERE song_id = ? AND user_id = ?", (song_id, user_id)
                        )
                        connect.commit()
                        flash("Song successfully deleted.")
                except Exception as e:
                    logging.error(f"Error deleting song: {e}")
                    flash("An error occurred while deleting the song.")

            return redirect(url_for("artist_page"))

        try:
            with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT concert_id, name, date, price, ticket_number FROM concerts WHERE user_id = ?", (user_id,))
                concerts = cursor.fetchall()

                cursor.execute("SELECT song_id, name, album_id, release_date, genre, duration FROM songs WHERE user_id = ?", (user_id,))
                songs = cursor.fetchall()

            return render_template("artist.html", concerts=concerts, songs=songs, user_id=user_id)

        except Exception as e:
            logging.error(f"Error fetching artist page: {e}")
            flash("An error occurred while fetching the artist page.")
            return redirect(url_for("user"))
    else:
        flash("Access denied: You are not an artist.")
        return redirect(url_for("user"))


if __name__ == "__main__":
    app.run(debug=True)
