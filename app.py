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
        CREATE TABLE IF NOT EXISTS FOLLOWS (
        user_id1 TEXT,
        user_id2 TEXT,
        PRIMARY KEY (user_id1, user_id2),
        FOREIGN KEY (user_id1) REFERENCES users(user_id),
        FOREIGN KEY (user_id2) REFERENCES users(user_id)

        )
"""
    )
        connect.execute(
        """
    CREATE TABLE IF NOT EXISTS TICKETS (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    concert_id INTEGER,
    user_id TEXT,
    ticket_price REAL,
    FOREIGN KEY (concert_id) REFERENCES concerts(concert_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    
    )
"""
    )
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
        connect.execute("""
    CREATE TABLE IF NOT EXISTS messages (
    sender_id TEXT REFERENCES users(id),
    receiver_id TEXT REFERENCES users(id),
    text TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )

""")
        connect.execute("""
    CREATE TABLE IF NOT EXISTS friends (
    user_id TEXT REFERENCES users(id),
    friend_id TEXT REFERENCES users(id),
    PRIMARY KEY (user_id, friend_id)
)

    """)
    
        connect.execute("""
    CREATE TABLE IF NOT EXISTS friendship_requests (
    sender_id TEXT REFERENCES users(id),
    receiver_id TEXT REFERENCES users(id),
    PRIMARY KEY (sender_id, receiver_id)
    )

     """)
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
                user_id TEXT ,
                FOREIGN KEY (user_id) REFERENCES USERS (user_id)
            )
            """
    )

        connect.execute(
                    """
            CREATE TABLE IF NOT EXISTS song_likes (
            song_likes_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            song_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (song_id) REFERENCES songs(song_id)
);
            """
    )
        connect.execute(" INSERT OR IGNORE INTO album (album_id, name, release_date, genre, user_id) VALUES ('1', 'album-1', '2017-05-14', 'happy', 2) ")
        connect.execute(" INSERT OR IGNORE INTO album (album_id, name, release_date, genre, user_id) VALUES ('2','album-2', '2017-05-14', 'happy', 2) ")
        connect.execute(" INSERT OR IGNORE INTO album (album_id, name, release_date, genre, user_id) VALUES ('3','album-3', '2017-05-14', 'happy', 2) ")
        connect.execute(" INSERT OR IGNORE INTO album (album_id, name, release_date, genre, user_id) VALUES ('4','album-4', '2017-05-14', 'happy', 2) ")


        connect.execute(
        """
            CREATE TABLE IF NOT EXISTS album_likes (
            album_likes_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            album_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (album_id) REFERENCES album(album_id)
);
            """
    )


        connect.execute(
        """
            CREATE TABLE IF NOT EXISTS playlist_likes (
            playlist_likes_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            playlist_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id)
);
            """
    )

    
        connect.execute(" INSERT OR IGNORE INTO album_likes (user_id, album_id) VALUES (1, 4) ")
        connect.execute(" INSERT OR IGNORE INTO album_likes (user_id, album_id) VALUES (1, 3) ")
        connect.execute(" INSERT OR IGNORE INTO song_likes (user_id, song_id) VALUES (1, 8) ")
        connect.execute(" INSERT OR IGNORE INTO song_likes (user_id, song_id) VALUES (1, 3) ")


        connect.execute(
        """
            CREATE TABLE IF NOT EXISTS playlist_favorite (
            playlist_favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            playlist_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id)
);
            """
    )
        
        connect.execute(
        """
            CREATE TABLE IF NOT EXISTS album_favorite (
            album_favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            album_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (album_id) REFERENCES album(album_id)
);
            """
    )
        
        connect.execute(
                    """
            CREATE TABLE IF NOT EXISTS song_favorite (
            song_favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            song_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (song_id) REFERENCES songs(song_id)
);
            """
    )

        connect.execute(
                    """
            CREATE TABLE IF NOT EXISTS song_comments (
            song_comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            song_id INTEGER NOT NULL,
            comment TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (song_id) REFERENCES songs(song_id)
);
            """
    )

        connect.execute(
                    """
            CREATE TABLE IF NOT EXISTS playlist_comments (
            playlist_comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            playlist_id INTEGER NOT NULL,
            comment TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id)
);
            """
    )

        connect.execute(
                    """
            CREATE TABLE IF NOT EXISTS album_comments (
            album_comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            album_id INTEGER NOT NULL,
            comment TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (album_id) REFERENCES album(album_id)
);
            """
    )
    

        connect.execute(
        """CREATE TABLE IF NOT EXISTS playlists (
    playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id TEXT,
    playlist_name TEXT NOT NULL,
    genre TEXT NOT NULL,
    is_private BOOLEAN NOT NULL CHECK (is_private IN (0, 1)),
    FOREIGN KEY (creator_id) REFERENCES users(user_id)
)
"""
    )
        connect.execute("""
CREATE TRIGGER IF NOT EXISTS delete_song_from_playlists
AFTER UPDATE OF is_limited ON songs
FOR EACH ROW
WHEN NEW.is_limited = 1
BEGIN
    DELETE FROM playlist_songs WHERE song_id = NEW.song_id;
END;
""")
        connect.execute(
            """
            CREATE TRIGGER IF NOT EXISTS remove_song_from_playlists
            AFTER DELETE ON SONGS
            FOR EACH ROW
            BEGIN
                DELETE FROM playlist_songs WHERE song_id = OLD.song_id;
            END;
            """
        )
        connect.execute(
        """CREATE TABLE IF NOT EXISTS playlist_songs (
    playlist_id INTEGER,
    song_id INTEGER,
    FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id),
    PRIMARY KEY (playlist_id, song_id)
);"""
    )
        connect.execute(
        """
            CREATE TABLE IF NOT EXISTS SONGS (
                song_id INTEGER PRIMARY KEY AUTOINCREMENT,
                album_id INTEGER,
                name TEXT,
                file TEXT,
                lyrics TEXT,
                release_date DATE,
                age_rating INTEGER CHECK(age_rating >= 9 AND age_rating <= 120),
                genre TEXT,
                duration INTEGER,
                is_limited BOOLEAN DEFAULT 0,
                user_id TEXT,
                FOREIGN KEY (album_id) REFERENCES ALBUM (album_id),
                FOREIGN KEY (user_id) REFERENCES USERS (user_id)
            )
            """
    )


        connect.execute(" INSERT OR IGNORE INTO songs (song_id, name, file, lyrics, release_date, age_rating, genre, duration, is_limited, album_id, user_id) VALUES ('1', 'song-5', '0', '0', '2017-05-14', 12, 'scary', 2, 0, 3, 1) ")
        connect.execute(" INSERT OR IGNORE INTO songs (song_id,name, file, lyrics, release_date, age_rating, genre, duration, is_limited, album_id, user_id) VALUES ('2', 'song-6', '0', '0', '2017-05-14', 13, 'scary', 2, 0, 3, 1) ")
        connect.execute(" INSERT OR IGNORE INTO songs (song_id,name, file, lyrics, release_date, age_rating, genre, duration, is_limited, album_id, user_id) VALUES ('3', 'song-7', '0', '0', '2017-05-14', 14, 'scary', 2, 0, 3, 1) ")
        connect.execute(" INSERT OR IGNORE INTO songs (song_id,name, file, lyrics, release_date, age_rating, genre, duration, is_limited, album_id, user_id) VALUES ('4', 'song-8', '0', '0', '2017-05-14', 15, 'scary', 2, 1, 3, 1) ")

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
        connect.execute(

        """
        INSERT OR IGNORE  INTO playlists (playlist_id, creator_id, playlist_name, genre, is_private)
        VALUES ('0', '1', 'kitty', 'haappy', 0 )
    """
    )
        connect.execute(
        "INSERT OR IGNORE INTO FOLLOWS (user_id1, user_id2) VALUES (1, 2)")
        connect.execute(
        "INSERT OR IGNORE INTO FOLLOWS (user_id1, user_id2) VALUES (2, 1)")

        connect.execute(
        """
            CREATE TABLE IF NOT EXISTS INBOX (
                notice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                friend_id TEXT,
                item_name TEXT,
                action TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES USERS (user_id)
                FOREIGN KEY (user_id) REFERENCES USERS (friend_id)
            )
            """
    )

        connect.execute("""
    CREATE TRIGGER IF NOT EXISTS insert_song_like
    AFTER INSERT ON song_likes
    BEGIN
        INSERT INTO INBOX (user_id, friend_id, item_name, action)
    SELECT NEW.user_id, f.friend_id, (SELECT name FROM songs WHERE song_id = NEW.song_id), 'like'
    FROM friends f
    WHERE f.user_id = NEW.user_id;
    END;
""")

        connect.execute("""
    CREATE TRIGGER IF NOT EXISTS delete_song_like
    AFTER DELETE ON song_likes
    BEGIN
        INSERT INTO INBOX (user_id, friend_id, item_name, action)
    SELECT OLD.user_id, f.friend_id, (SELECT name FROM songs WHERE song_id = OLD.song_id), 'dislike'
    FROM friends f
    WHERE f.user_id = OLD.user_id;
    END;
""")

        connect.execute("""
    CREATE TRIGGER IF NOT EXISTS insert_album_like
    AFTER INSERT ON album_likes
    BEGIN
        INSERT INTO INBOX (user_id, friend_id, item_name, action)
    SELECT NEW.user_id, f.friend_id, (SELECT name FROM album WHERE album_id = NEW.album_id), 'like'
    FROM friends f
    WHERE f.user_id = NEW.user_id;
    END;
""")

        connect.execute("""
    CREATE TRIGGER IF NOT EXISTS delete_album_like
    AFTER DELETE ON album_likes
    BEGIN
        INSERT INTO INBOX (user_id, friend_id, item_name, action)
    SELECT OLD.user_id, f.friend_id, (SELECT name FROM album WHERE album_id = OLD.album_id), 'dislike'
    FROM friends f
    WHERE f.user_id = OLD.user_id;
    END;
""")
        connect.execute("""
    CREATE TRIGGER IF NOT EXISTS insert_playlist_like
    AFTER INSERT ON playlist_likes
    BEGIN
        INSERT INTO INBOX (user_id, friend_id, item_name, action)
    SELECT NEW.user_id, f.friend_id, (SELECT playlist_name FROM playlists WHERE playlist_id = NEW.playlist_id), 'like'
    FROM friends f
    WHERE f.user_id = NEW.user_id;
    END;
""")

        connect.execute("""
    CREATE TRIGGER IF NOT EXISTS delete_playlist_like
    AFTER DELETE ON playlist_likes
    BEGIN
         INSERT INTO INBOX (user_id, friend_id, item_name, action)
    SELECT OLD.user_id, f.friend_id, (SELECT playlist_name FROM playlists WHERE playlist_id = OLD.playlist_id), 'dislike'
    FROM friends f
    WHERE f.user_id = OLD.user_id;
    END;
""")

        connect.execute("""
    CREATE TRIGGER IF NOT EXISTS insert_song_comments
    AFTER INSERT ON song_comments
    BEGIN
        INSERT INTO INBOX (user_id, friend_id, item_name, action)
    SELECT NEW.user_id, f.friend_id, (SELECT name FROM songs WHERE song_id = NEW.song_id), 'commente'
    FROM friends f
    WHERE f.user_id = NEW.user_id;
    END;
""")

        connect.execute("""
    CREATE TRIGGER IF NOT EXISTS insert_playlist_comments
    AFTER INSERT ON playlist_comments
    BEGIN
        INSERT INTO INBOX (user_id, friend_id, item_name, action)
    SELECT NEW.user_id, f.friend_id, (SELECT playlist_name FROM playlists WHERE playlist_id = NEW.playlist_id), 'commente'
    FROM friends f
    WHERE f.user_id = NEW.user_id;
    END;
""")

        connect.execute("""
    CREATE TRIGGER IF NOT EXISTS insert_album_comments
    AFTER INSERT ON album_comments
    BEGIN
        INSERT INTO INBOX (user_id, friend_id, item_name, action)
    SELECT NEW.user_id, f.friend_id, (SELECT name FROM album WHERE album_id = NEW.album_id), 'commente'
    FROM friends f
    WHERE f.user_id = NEW.user_id;
    END;
""")
        




@app.route("/")
def index():
    return render_template("login.html")


@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        user_id = "".join(random.choices(
            string.ascii_letters + string.digits, k=8))
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



logging.basicConfig(level=logging.DEBUG)



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



@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_category = request.form["search_category"]
        search_input = request.form["search_input"]

        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()

            user_id = session["user_id"]

            if search_category == "song_name":
                c.execute("""
                    SELECT DISTINCT s.song_id, s.name, u.name, s.age_rating, s.genre, 
                        CASE WHEN sl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, 
                        CASE WHEN sf.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite
                    FROM songs s 
                    JOIN users u ON s.user_id = u.user_id
                    LEFT JOIN song_likes sl ON s.song_id = sl.song_id AND sl.user_id = ?
                    LEFT JOIN song_favorite sf ON s.song_id = sf.song_id AND sf.user_id = ?
                    WHERE s.name LIKE ? AND s.is_limited = 0
                """, (user_id, user_id, "%"+search_input+"%"))
                table_name = "songs"
                columns = ["song_id", "song_name", "artist",
                           "age", "genre", "is_liked", "is_favorite"]
            elif search_category == "artist":
                c.execute("""
                    SELECT DISTINCT s.song_id, s.name, u.name, s.age_rating, s.genre, 
                        CASE WHEN sl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, 
                        CASE WHEN sf.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite
                    FROM songs s 
                    JOIN users u ON s.user_id = u.user_id
                    LEFT JOIN song_likes sl ON s.song_id = sl.song_id AND sl.user_id = ?
                    LEFT JOIN song_favorite sf ON s.song_id = sf.song_id AND sf.user_id = ?
                    WHERE u.name LIKE ? AND s.is_limited = 0
                """, (user_id, user_id, "%"+search_input+"%"))
                table_name = "songs"
                columns = ["song_id", "song_name", "artist",
                           "age", "genre", "is_liked", "is_favorite"]
            elif search_category == "age":
                c.execute("""
                    SELECT DISTINCT s.song_id, s.name, u.name, s.age_rating, s.genre, 
                        CASE WHEN sl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, 
                        CASE WHEN sf.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite
                    FROM songs s 
                    JOIN users u ON s.user_id = u.user_id
                    LEFT JOIN song_likes sl ON s.song_id = sl.song_id AND sl.user_id = ?
                    LEFT JOIN song_favorite sf ON s.song_id = sf.song_id AND sf.user_id = ?
                    WHERE s.age_rating LIKE ? AND s.is_limited = 0
                """, (user_id, user_id, "%"+search_input+"%"))
                table_name = "songs"
                columns = ["song_id", "song_name", "artist",
                           "age", "genre", "is_liked", "is_favorite"]
            elif search_category == "genre":
                c.execute("""
                    SELECT DISTINCT s.song_id, s.name, u.name, s.age_rating, s.genre, 
                        CASE WHEN sl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, 
                        CASE WHEN sf.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite
                    FROM songs s 
                    JOIN users u ON s.user_id = u.user_id
                    LEFT JOIN song_likes sl ON s.song_id = sl.song_id AND sl.user_id = ?
                    LEFT JOIN song_favorite sf ON s.song_id = sf.song_id AND sf.user_id = ?
                    WHERE s.genre LIKE ? AND s.is_limited = 0
                """, (user_id, user_id, "%"+search_input+"%"))
                table_name = "songs"
                columns = ["song_id", "song_name", "artist",
                           "age", "genre", "is_liked", "is_favorite"]
            elif search_category == "album_name":
                c.execute("SELECT DISTINCT a.album_id, a.name, u.name, a.genre, a.release_date, CASE WHEN sl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, CASE WHEN af.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite FROM album a JOIN users u ON a.user_id = u.user_id LEFT JOIN album_likes sl ON a.album_id = sl.album_id AND sl.user_id = ? LEFT JOIN album_favorite af ON a.album_id = af.album_id AND af.user_id = ? WHERE a.name LIKE ? ", (user_id, user_id, "%"+search_input+"%"))
                table_name = "albums"
                columns = ["album_id", "album_name", "album_artist",
                           "genre", "release_date", "is_liked", "is_favorite"]
            elif search_category == "album_artist":
                c.execute("SELECT DISTINCT a.album_id, a.name, u.name, a.genre, a.release_date, CASE WHEN sl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, CASE WHEN af.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite FROM album a JOIN users u ON a.user_id = u.user_id LEFT JOIN album_likes sl ON a.album_id = sl.album_id AND sl.user_id = ? LEFT JOIN album_favorite af ON a.album_id = af.album_id AND af.user_id = ? WHERE u.name LIKE ? ", (user_id, user_id, "%"+search_input+"%"))
                table_name = "albums"
                columns = ["album_id", "album_name", "album_artist",
                           "genre", "release_date", "is_liked", "is_favorite"]
            elif search_category == "playlist_name":
                c.execute("""SELECT DISTINCT p.playlist_id, p.playlist_name, p.genre, 
                CASE WHEN sl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, 
                CASE WHEN pf.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite
                FROM playlists p
                JOIN users u ON p.creator_id = u.user_id
                LEFT JOIN friends f ON p.creator_id = f.friend_id AND f.user_id = ?
                LEFT JOIN playlist_likes sl ON p.playlist_id = sl.playlist_id AND sl.user_id = ?
                LEFT JOIN playlist_favorite pf ON p.playlist_id = pf.playlist_id AND pf.user_id = ?
                WHERE p.is_private = 0 and (f.user_id IS NOT NULL OR p.creator_id = ?)
                AND p.playlist_name LIKE ?
                """, (user_id, user_id, user_id, user_id, "%"+search_input+"%"))
                table_name = "playlists"
                columns = ["playlist_id", "playlist_name",
                           "genre", "is_liked", "is_favorite"]

            results = c.fetchall()
            conn.close()

            data = [dict(zip(columns, row)) for row in results]

            return render_template("search.html", data=data, table_name=table_name)

        except sqlite3.Error as e:
            # Log the error
            logging.error(
                f"An error occurred while processing the search request: {e}")
            # Display a user-friendly error message
            return "An error occurred while processing your search request. Please try again later."

    return render_template("search.html")





@app.route("/like_song/<int:song_id>", methods=["POST"])
def like_song(song_id):
    user_id = session["user_id"]
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM song_likes WHERE user_id = ? AND song_id = ?", (user_id, song_id))
        result = c.fetchone()
        if result:
            c.execute(
                "DELETE FROM song_likes WHERE user_id = ? AND song_id = ?", (user_id, song_id))
        else:
            c.execute(
                "INSERT INTO song_likes (user_id, song_id) VALUES (?, ?)", (user_id, song_id))
        conn.commit()

        # Fetch the updated search results
        c.execute("""
            SELECT DISTINCT s.song_id, s.name, u.name, s.age_rating, s.genre, 
                CASE WHEN sl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, 
                CASE WHEN sf.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite
            FROM songs s 
            JOIN users u ON s.user_id = u.user_id
            LEFT JOIN song_likes sl ON s.song_id = sl.song_id AND sl.user_id = ?
            LEFT JOIN song_favorite sf ON s.song_id = sf.song_id AND sf.user_id = ?
            WHERE s.is_limited = 0
        """, (user_id, user_id))
        song_results = c.fetchall()
        song_data = [dict(zip(["song_id", "song_name", "artist",
                               "age", "genre", "is_liked", "is_favorite"], row)) for row in song_results]

        conn.close()

        return render_template("search.html", table_name="songs", data=song_data)
    except sqlite3.Error as e:
        # Log the error
        logging.error(
            f"An error occurred while processing the like request: {e}")
        # Display a user-friendly error message
        return "An error occurred while processing your like request. Please try again later."


@app.route("/dislike_song/<int:song_id>", methods=["POST"])
def dislike_song(song_id):
    user_id = session["user_id"]
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM song_likes WHERE user_id = ? AND song_id = ?", (user_id, song_id))
        result = c.fetchone()
        if result:
            c.execute(
                "DELETE FROM song_likes WHERE user_id = ? AND song_id = ?", (user_id, song_id))
        else:
            c.execute(
                "INSERT INTO song_likes (user_id, song_id) VALUES (?, ?)", (user_id, song_id))
        conn.commit()

        # Fetch the updated search results
        c.execute("SELECT DISTINCT s.song_id, s.name, u.name, s.age_rating, s.genre, CASE WHEN sl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, CASE WHEN sf.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite FROM songs s JOIN users u ON s.user_id = u.user_id LEFT JOIN song_likes sl ON s.song_id = sl.song_id AND sl.user_id = ? LEFT JOIN song_favorite sf ON s.song_id = sf.song_id AND sf.user_id = ?", (user_id, user_id))
        song_results = c.fetchall()
        song_data = [dict(zip(["song_id", "song_name", "artist",
                               "age", "genre", "is_liked", "is_favorite"], row)) for row in song_results]

        conn.close()

        return render_template("search.html", table_name="songs", data=song_data)
    except sqlite3.Error as e:
        # Log the error
        logging.error(
            f"An error occurred while processing the like request: {e}")
        # Display a user-friendly error message
        return "An error occurred while processing your like request. Please try again later."


@app.route("/like_album/<int:album_id>", methods=["POST"])
def like_album(album_id):
    user_id = session["user_id"]
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM album_likes WHERE user_id = ? AND album_id = ?", (user_id, album_id))
        result = c.fetchone()
        if result:
            c.execute(
                "DELETE FROM album_likes WHERE user_id = ? AND album_id = ?", (user_id, album_id))
        else:
            c.execute(
                "INSERT INTO album_likes (user_id, album_id) VALUES (?, ?)", (user_id, album_id))
        conn.commit()

        c.execute("SELECT DISTINCT a.album_id, a.name, u.name AS album_artist, a.genre, a.release_date,  CASE WHEN al.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, CASE WHEN af.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite FROM album a JOIN users u ON a.user_id = u.user_id LEFT JOIN album_favorite af ON a.album_id = af.album_id AND af.user_id = ? LEFT JOIN album_likes al ON a.album_id = al.album_id AND al.user_id = ? ", (user_id, user_id))
        album_results = c.fetchall()
        album_data = [dict(zip(["album_id", "name", "album_artist", "genre",
                           "release_date", "is_liked", "is_favorite"], row)) for row in album_results]

        conn.close()

        return render_template("search.html", table_name="albums", data=album_data)
    except sqlite3.Error as e:
        # Log the error
        logging.error(
            f"An error occurred while processing the like request: {e}")
        # Display a user-friendly error message
        return "An error occurred while processing your like request. Please try again later."


@app.route("/dislike_album/<int:album_id>", methods=["POST"])
def dislike_album(album_id):
    user_id = session["user_id"]
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM album_likes WHERE user_id = ? AND album_id = ?", (user_id, album_id))
        result = c.fetchone()
        if result:
            c.execute(
                "DELETE FROM album_likes WHERE user_id = ? AND album_id = ?", (user_id, album_id))
        else:
            c.execute(
                "INSERT INTO album_likes (user_id, album_id) VALUES (?, ?)", (user_id, album_id))
        conn.commit()

        c.execute("SELECT DISTINCT a.album_id, a.name, u.name AS album_artist, a.genre, a.release_date,  CASE WHEN al.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, CASE WHEN af.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite FROM album a JOIN users u ON a.user_id = u.user_id LEFT JOIN album_favorite af ON a.album_id = af.album_id AND af.user_id = ? LEFT JOIN album_likes al ON a.album_id = al.album_id AND al.user_id = ? ", (user_id, user_id))
        album_results = c.fetchall()
        album_data = [dict(zip(["album_id", "name", "album_artist", "genre",
                           "release_date", "is_liked", "is_favorite"], row)) for row in album_results]

        conn.close()

        return render_template("search.html", table_name="albums", data=album_data)
    except sqlite3.Error as e:
        # Log the error
        logging.error(
            f"An error occurred while processing the like request: {e}")
        # Display a user-friendly error message
        return "An error occurred while processing your like request. Please try again later."


@app.route("/like_playlist/<int:playlist_id>", methods=["POST"])
def like_playlist(playlist_id):
    user_id = session["user_id"]
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM playlist_likes WHERE user_id = ? AND playlist_id = ?", (user_id, playlist_id))
        result = c.fetchone()
        if result:
            c.execute(
                "DELETE FROM playlist_likes WHERE user_id = ? AND playlist_id = ?", (user_id, playlist_id))
        else:
            c.execute(
                "INSERT INTO playlist_likes (user_id, playlist_id) VALUES (?, ?)", (user_id, playlist_id))
        conn.commit()

        c.execute("""
                    SELECT DISTINCT p.playlist_id, p.playlist_name, p.genre, 
                                    CASE WHEN pf.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite, 
                                    CASE WHEN pl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked
                    FROM playlists p
                    LEFT JOIN playlist_favorite pf ON p.playlist_id = pf.playlist_id AND pf.user_id = ?
                    LEFT JOIN playlist_likes pl ON p.playlist_id = pl.playlist_id AND pl.user_id = ?
                    LEFT JOIN friends f ON p.creator_id = f.friend_id AND f.user_id = ?
                    LEFT JOIN users u ON p.creator_id = u.user_id
                    WHERE (p.is_private = 0 OR p.creator_id = ? OR f.user_id IS NOT NULL) AND u.user_id IS NOT NULL
                    """, (user_id, user_id, user_id, user_id))

        playlist_results = c.fetchall()
        playlist_data = [dict(zip(["playlist_id", "playlist_name", "genre",
                              "is_favorite", "is_liked"], row)) for row in playlist_results]

        conn.close()

        return render_template("search.html", table_name="playlists", data=playlist_data)
    except sqlite3.Error as e:
        # Log the error
        logging.error(
            f"An error occurred while processing the like request: {e}")
        # Display a user-friendly error message
        return "An error occurred while processing your like request. Please try again later."


@app.route("/dislike_playlist/<int:playlist_id>", methods=["POST"])
def dislike_playlist(playlist_id):
    user_id = session["user_id"]
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM playlist_likes WHERE user_id = ? AND playlist_id = ?", (user_id, playlist_id))
        result = c.fetchone()
        if result:
            c.execute(
                "DELETE FROM playlist_likes WHERE user_id = ? AND playlist_id = ?", (user_id, playlist_id))
        else:
            c.execute(
                "INSERT INTO playlist_likes (user_id, playlist_id) VALUES (?, ?)", (user_id, playlist_id))
        conn.commit()

        c.execute("""
                    SELECT DISTINCT p.playlist_id, p.playlist_name, p.genre, 
                                    CASE WHEN pf.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite, 
                                    CASE WHEN pl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked
                    FROM playlists p
                    LEFT JOIN playlist_favorite pf ON p.playlist_id = pf.playlist_id AND pf.user_id = ?
                    LEFT JOIN playlist_likes pl ON p.playlist_id = pl.playlist_id AND pl.user_id = ?
                    LEFT JOIN friends f ON p.creator_id = f.friend_id AND f.user_id = ?
                    LEFT JOIN users u ON p.creator_id = u.user_id
                    WHERE (p.is_private = 0 OR p.creator_id = ? OR f.user_id IS NOT NULL) AND u.user_id IS NOT NULL
                    """, (user_id, user_id, user_id, user_id))

        playlist_results = c.fetchall()
        playlist_data = [dict(zip(["playlist_id", "playlist_name", "genre",
                              "is_favorite", "is_liked"], row)) for row in playlist_results]

        conn.close()

        return render_template("search.html", table_name="playlists", data=playlist_data)
    except sqlite3.Error as e:
        # Log the error
        logging.error(
            f"An error occurred while processing the like request: {e}")
        # Display a user-friendly error message
        return "An error occurred while processing your like request. Please try again later."


@app.route("/favorite_song/<int:song_id>", methods=["POST"])
def favorite_song(song_id):
    user_id = session["user_id"]
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM song_favorite WHERE user_id = ? AND song_id = ?", (user_id, song_id))
        result = c.fetchone()
        if result:
            c.execute(
                "DELETE FROM song_favorite WHERE user_id = ? AND song_id = ?", (user_id, song_id))
        else:
            c.execute(
                "INSERT INTO song_favorite (user_id, song_id) VALUES (?, ?)", (user_id, song_id))
        conn.commit()

        # Fetch the updated search results
        c.execute("""
            SELECT DISTINCT s.song_id, s.name, u.name, s.age_rating, s.genre, 
                CASE WHEN sl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, 
                CASE WHEN sf.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite
            FROM songs s 
            JOIN users u ON s.user_id = u.user_id
            LEFT JOIN song_likes sl ON s.song_id = sl.song_id AND sl.user_id = ?
            LEFT JOIN song_favorite sf ON s.song_id = sf.song_id AND sf.user_id = ?
            WHERE s.is_limited = 0
        """, (user_id, user_id))
        song_results = c.fetchall()
        song_data = [dict(zip(["song_id", "song_name", "artist",
                               "age", "genre", "is_liked", "is_favorite"], row)) for row in song_results]

        conn.close()

        return render_template("search.html", table_name="songs", data=song_data)
    except sqlite3.Error as e:
        # Log the error
        logging.error(
            f"An error occurred while processing the favorite request: {e}")
        # Display a user-friendly error message
        return "An error occurred while processing your favorite request. Please try again later."


@app.route("/disfavorite_song/<int:song_id>", methods=["POST"])
def disfavorite_song(song_id):
    user_id = session["user_id"]
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM song_favorite WHERE user_id = ? AND song_id = ?", (user_id, song_id))
        result = c.fetchone()
        if result:
            c.execute(
                "DELETE FROM song_favorite WHERE user_id = ? AND song_id = ?", (user_id, song_id))
        else:
            c.execute(
                "INSERT INTO song_favorite (user_id, song_id) VALUES (?, ?)", (user_id, song_id))
        conn.commit()

        # Fetch the updated search results
        c.execute("SELECT DISTINCT s.song_id, s.name, u.name, s.age_rating, s.genre, CASE WHEN sl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, CASE WHEN sf.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite FROM songs s JOIN users u ON s.user_id = u.user_id LEFT JOIN song_likes sl ON s.song_id = sl.song_id AND sl.user_id = ? LEFT JOIN song_favorite sf ON s.song_id = sf.song_id AND sf.user_id = ?", (user_id, user_id))
        song_results = c.fetchall()
        song_data = [dict(zip(["song_id", "song_name", "artist",
                               "age", "genre", "is_liked", "is_favorite"], row)) for row in song_results]

        conn.close()

        return render_template("search.html", table_name="songs", data=song_data)
    except sqlite3.Error as e:
        # Log the error
        logging.error(
            f"An error occurred while processing the favorite request: {e}")
        # Display a user-friendly error message
        return "An error occurred while processing your favorite request. Please try again later."


@app.route("/favorite_album/<int:album_id>", methods=["POST"])
def favorite_album(album_id):
    user_id = session["user_id"]
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM album_favorite WHERE user_id = ? AND album_id = ?", (user_id, album_id))
        result = c.fetchone()
        if result:
            c.execute(
                "DELETE FROM album_favorite WHERE user_id = ? AND album_id = ?", (user_id, album_id))
        else:
            c.execute(
                "INSERT INTO album_favorite (user_id, album_id) VALUES (?, ?)", (user_id, album_id))
        conn.commit()

        c.execute("SELECT DISTINCT a.album_id, a.name, u.name AS album_artist, a.genre, a.release_date,  CASE WHEN al.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, CASE WHEN af.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite FROM album a JOIN users u ON a.user_id = u.user_id LEFT JOIN album_favorite af ON a.album_id = af.album_id AND af.user_id = ? LEFT JOIN album_likes al ON a.album_id = al.album_id AND al.user_id = ? ", (user_id, user_id))
        album_results = c.fetchall()
        album_data = [dict(zip(["album_id", "name", "album_artist", "genre",
                           "release_date", "is_liked", "is_favorite"], row)) for row in album_results]

        conn.close()

        return render_template("search.html", table_name="albums", data=album_data)
    except sqlite3.Error as e:
        # Log the error
        logging.error(
            f"An error occurred while processing the favorite request: {e}")
        # Display a user-friendly error message
        return "An error occurred while processing your favorite request. Please try again later."


@app.route("/disfavorite_album/<int:album_id>", methods=["POST"])
def disfavorite_album(album_id):
    user_id = session["user_id"]
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM album_favorite WHERE user_id = ? AND album_id = ?", (user_id, album_id))
        result = c.fetchone()
        if result:
            c.execute(
                "DELETE FROM album_favorite WHERE user_id = ? AND album_id = ?", (user_id, album_id))
        else:
            c.execute(
                "INSERT INTO album_favorite (user_id, album_id) VALUES (?, ?)", (user_id, album_id))
        conn.commit()

        c.execute("SELECT DISTINCT a.album_id, a.name, u.name AS album_artist, a.genre, a.release_date,  CASE WHEN al.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked, CASE WHEN af.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite FROM album a JOIN users u ON a.user_id = u.user_id LEFT JOIN album_favorite af ON a.album_id = af.album_id AND af.user_id = ? LEFT JOIN album_likes al ON a.album_id = al.album_id AND al.user_id = ? ", (user_id, user_id))
        album_results = c.fetchall()
        album_data = [dict(zip(["album_id", "name", "album_artist", "genre",
                           "release_date", "is_liked", "is_favorite"], row)) for row in album_results]

        conn.close()

        return render_template("search.html", table_name="albums", data=album_data)
    except sqlite3.Error as e:
        # Log the error
        logging.error(
            f"An error occurred while processing the favorite request: {e}")
        # Display a user-friendly error message
        return "An error occurred while processing your favorite request. Please try again later."


@app.route("/favorite_playlist/<int:playlist_id>", methods=["POST"])
def favorite_playlist(playlist_id):
    user_id = session["user_id"]
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM playlist_favorite WHERE user_id = ? AND playlist_id = ?", (user_id, playlist_id))
        result = c.fetchone()
        if result:
            c.execute(
                "DELETE FROM playlist_favorite WHERE user_id = ? AND playlist_id = ?", (user_id, playlist_id))
        else:
            c.execute(
                "INSERT INTO playlist_favorite (user_id, playlist_id) VALUES (?, ?)", (user_id, playlist_id))

        conn.commit()

        c.execute("""
                    SELECT DISTINCT p.playlist_id, p.playlist_name, p.genre, 
                                    CASE WHEN pl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked,
                                    CASE WHEN pf.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite
                    FROM playlists p
                    JOIN users u ON p.creator_id = u.user_id
                    LEFT JOIN playlist_favorite pf ON p.playlist_id = pf.playlist_id AND pf.user_id = ?
                    LEFT JOIN playlist_likes pl ON p.playlist_id = pl.playlist_id AND pl.user_id = ?
                    WHERE (p.is_private = 0 OR p.creator_id = ? OR p.creator_id IN (
                        SELECT friend_id FROM friends WHERE user_id = ?
                    )) AND u.user_id IS NOT NULL
                    """, (user_id, user_id, user_id, user_id))

        playlist_results = c.fetchall()
        playlist_data = [dict(zip(["playlist_id", "playlist_name", "genre",
                              "is_liked", "is_favorite"], row)) for row in playlist_results]

        conn.close()

        return render_template("search.html", table_name="playlists", data=playlist_data)
    except sqlite3.Error as e:
        # Log the error
        logging.error(
            f"An error occurred while processing the favorite request: {e}")
        # Display a user-friendly error message
        return "An error occurred while processing your favorite request. Please try again later."


@app.route("/disfavorite_playlist/<int:playlist_id>", methods=["POST"])
def disfavorite_playlist(playlist_id):
    user_id = session["user_id"]
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM playlist_favorite WHERE user_id = ? AND playlist_id = ?", (user_id, playlist_id))
        result = c.fetchone()
        if result:
            c.execute(
                "DELETE FROM playlist_favorite WHERE user_id = ? AND playlist_id = ?", (user_id, playlist_id))
        else:
            c.execute(
                "INSERT INTO playlist_favorite (user_id, playlist_id) VALUES (?, ?)", (user_id, playlist_id))

        conn.commit()

        c.execute("""
                    SELECT DISTINCT p.playlist_id, p.playlist_name, p.genre, 
                                    CASE WHEN pl.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked,
                                    CASE WHEN pf.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite
                    FROM playlists p
                    JOIN users u ON p.creator_id = u.user_id
                    LEFT JOIN playlist_favorite pf ON p.playlist_id = pf.playlist_id AND pf.user_id = ?
                    LEFT JOIN playlist_likes pl ON p.playlist_id = pl.playlist_id AND pl.user_id = ?
                    WHERE (p.is_private = 0 OR p.creator_id = ? OR p.creator_id IN (
                        SELECT friend_id FROM friends WHERE user_id = ?
                    )) AND u.user_id IS NOT NULL
                    """, (user_id, user_id, user_id, user_id))
        playlist_results = c.fetchall()
        playlist_data = [dict(zip(["playlist_id", "playlist_name", "genre",
                              "is_liked", "is_favorite"], row)) for row in playlist_results]

        conn.close()

        return render_template("search.html", table_name="playlists", data=playlist_data)
    except sqlite3.Error as e:
        # Log the error
        logging.error(
            f"An error occurred while processing the favorite request: {e}")
        # Display a user-friendly error message
        return "An error occurred while processing your favorite request. Please try again later."


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/user")
def user():
    if "user_id" in session:
        user_id = session["user_id"]
        name = session["name"]
        balance = session["balance"]
        is_premium = session["is_premium"]
        is_artist = session["is_artist"]

        try:
            connect = get_db_connection()
            cursor = connect.cursor()
            
            # Fetching unexpired tickets only
            cursor.execute(
                """
                SELECT T.ticket_id, C.name, U.name AS singer_name, C.date, T.ticket_price 
                FROM TICKETS T
                JOIN concerts C ON T.concert_id = C.concert_id
                JOIN USERS U ON C.user_id = U.user_id
                WHERE T.user_id = ?
                AND C.date >= DATE('now')
                """,
                (user_id,)
            )
            tickets = cursor.fetchall()
            
                        # Fetching unexpired tickets only
            cursor.execute(
                """
                SELECT T.ticket_id, C.name, U.name AS singer_name, C.date, T.ticket_price 
                FROM TICKETS T
                JOIN concerts C ON T.concert_id = C.concert_id
                JOIN USERS U ON C.user_id = U.user_id
                WHERE T.user_id = ?
                AND C.date < DATE('now')
                """,
                (user_id,)
            )
            etickets = cursor.fetchall()
            
        except Exception as e:
            logging.error(f"Error fetching tickets: {e}")
            tickets = []
            etickets =[]
            friendship_requests = []

        try:
            # Fetching suggested songs
            cursor.execute(
                """
                SELECT s.name, u.name AS artist_name
                FROM songs s
                JOIN users u ON s.user_id = u.user_id
                WHERE s.genre IN (
                    SELECT DISTINCT genre
                    FROM songs
                    WHERE song_id IN (
                        SELECT song_id
                        FROM song_likes
                        WHERE user_id = ?
                    )    
                ) AND s.is_limited = 0
                GROUP BY s.song_id
                ORDER BY COUNT(s.song_id) DESC
                LIMIT 10;
                """,
                (user_id,)
            )
            suggested_songs = cursor.fetchall()

            # Fetching suggested albums
            cursor.execute(
                """
                SELECT a.name, u.name AS artist_name
                FROM album a
                JOIN users u ON a.user_id = u.user_id
                WHERE a.genre IN (
                    SELECT DISTINCT genre
                    FROM album
                    WHERE album_id IN (
                        SELECT album_id
                        FROM album_likes
                        WHERE user_id = ?
                    )
                )
                GROUP BY a.album_id
                ORDER BY COUNT(a.album_id) DESC
                LIMIT 10;
                """,
                (user_id,)
            )
            suggested_albums = cursor.fetchall()

            # Fetching friendship requests
            cursor.execute(
                """
                SELECT FR.sender_id, U.email AS sender_email
                FROM friendship_requests FR
                JOIN users U ON FR.sender_id = U.user_id
                WHERE FR.receiver_id = ?
                """,
                (user_id,)
            )
            friendship_requests = cursor.fetchall()
        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            suggested_songs = []
            suggested_albums = []

        
        with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()
        cursor.execute("SELECT user_id, friend_id, item_name, action, date FROM INBOX WHERE friend_id = ? ORDER BY date DESC", (user_id,))
        inbox_notices = []
        for row in cursor.fetchall():
            user_name = get_user_name(row[0])
            inbox_notices.append({
                'user_name': user_name,
                'action': row[3],
                'item_name': row[2],
                'date': row[4]
        })

        return render_template(
            "user.html",
            user_id=user_id,
            name=name,
            balance=balance,
            is_premium=is_premium,
            is_artist=is_artist,
            tickets=tickets,
            etickets=etickets,
            suggested_songs=suggested_songs,
            suggested_albums=suggested_albums,
            friendship_requests=friendship_requests,
            inbox_notices=inbox_notices
        )
    else:
        return redirect(url_for("login"))


def get_user_name(user_id):
    with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()
    # Fetch the user's name from the USERS table
    cursor.execute("SELECT name FROM USERS WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 'Unknown'
    
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
                    "UPDATE USERS SET is_premium = 1 WHERE user_id = ?", (
                        user_id,)
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
                name = request.form.get("name")
                date = request.form.get("date")
                price = request.form.get("price")
                ticket_number = request.form.get("tickets")  # Make sure this matches your HTML input name
    
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
                    
                        # Get concert details
                    cursor.execute("SELECT price, user_id FROM concerts WHERE concert_id = ?", (concert_id,))
                    concert = cursor.fetchone()
                    if not concert:
                        flash("Concert not found.")
                        return redirect(url_for("artist_page"))
                    
                    concert_price, singer_id = concert

                    # Get all tickets for the concert
                    cursor.execute("SELECT user_id, ticket_price FROM TICKETS WHERE concert_id = ?", (concert_id,))
                    tickets = cursor.fetchall()

                    ticket_count = len(tickets)
                    
                    # Refund each user
                    for ticket in tickets:
                        ticket_user_id, ticket_price = ticket
                        
                        # Update user's balance
                        cursor.execute("SELECT balance FROM USERS WHERE user_id = ?", (ticket_user_id,))
                        user_balance = cursor.fetchone()[0]
                        new_user_balance = user_balance + ticket_price
                        cursor.execute("UPDATE USERS SET balance = ? WHERE user_id = ?", (new_user_balance, ticket_user_id))
                        
                        # Create transaction for refund
                        transaction_id = "".join(random.choices(string.ascii_letters + string.digits, k=12))
                        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        cursor.execute(
                            "INSERT INTO TRANSACTIONS (transaction_id, user_id, recipient_id, amount, date) VALUES (?, ?, ?, ?, ?)",
                            (transaction_id, singer_id, ticket_user_id, ticket_price, date)
                        )
                    
                    # Delete tickets
                    cursor.execute("DELETE FROM TICKETS WHERE concert_id = ?", (concert_id,))
                    
                    # Refund admin's share to singer
                    admin_id = 1
                    admin_share_total = ticket_count * concert_price * 0.05
                    
                    cursor.execute("SELECT balance FROM USERS WHERE user_id = ?", (admin_id,))
                    admin_balance = cursor.fetchone()[0]
                    new_admin_balance = admin_balance - admin_share_total
                    cursor.execute("UPDATE USERS SET balance = ? WHERE user_id = ?", (new_admin_balance, admin_id))
                    
                    cursor.execute("SELECT balance FROM USERS WHERE user_id = ?", (singer_id,))
                    singer_balance = cursor.fetchone()[0]
                    new_singer_balance = singer_balance + admin_share_total
                    cursor.execute("UPDATE USERS SET balance = ? WHERE user_id = ?", (new_singer_balance, singer_id))

                    # Create transaction for admin to singer refund
                    transaction_id = "".join(random.choices(string.ascii_letters + string.digits, k=12))
                    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute(
                        "INSERT INTO TRANSACTIONS (transaction_id, user_id, recipient_id, amount, date) VALUES (?, ?, ?, ?, ?)",
                        (transaction_id, admin_id, singer_id, admin_share_total, date)
                    )

                    # Delete the concert
                    cursor.execute("DELETE FROM concerts WHERE concert_id = ? AND user_id = ?", (concert_id, user_id))

                    # Commit the transaction
                    connect.commit()
                    
                    flash("Concert and related tickets successfully deleted. Refunds have been processed.")
                except Exception as e:
                    logging.error(f"Error deleting concert: {e}")
                    flash("An error occurred while deleting the concert.")
                    
                    

            elif action== "add_song":
                song_name = request.form.get('song_name')
                file = request.form.get('file')
                lyrics = request.form.get('lyrics')
                release_date = request.form.get('release_date')
                age_rating = request.form.get('age_rating')
                genre = request.form.get('genre')
                duration = request.form.get('duration')
                user_id = session["user_id"]  # Replace with actual user_id retrieval logic

                try:
                    with sqlite3.connect('database.db') as connect:
                        cursor = connect.cursor()
                        cursor.execute(
                            """
                            INSERT INTO songs (album_id, name, file, lyrics, release_date, age_rating, genre, duration, is_limited, user_id)
                            VALUES ("1",?, ?, ?, ?, ?, ?, ?, "0", ?)
                            """,
                            (song_name, file, lyrics, release_date, age_rating, genre, duration, user_id)
                        )
                        connect.commit()
                        flash('Song successfully added.')
                except Exception as e:
                    logging.error(f'Error adding song: {e}')
                    flash('An error occurred while adding the song.')
           
            elif action == "delete_song":
                song_id = request.form["song_id"]

                try:
                    with sqlite3.connect("database.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(
                            "DELETE FROM songs WHERE song_id = ? AND user_id = ?",
                            (song_id, user_id),
                        )
                        connect.commit()
                        flash("Song successfully deleted.")
                except Exception as e:
                    logging.error(f"Error deleting song: {e}")
                    flash("An error occurred while deleting the song.")

            elif action == "delete_song":
                song_id = request.form["song_id"]

                try:
                    with sqlite3.connect("database.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(
                            "DELETE FROM songs WHERE song_id = ? AND user_id = ?",
                            (song_id, user_id),
                        )
                        connect.commit()
                        flash("Song successfully deleted.")
                except Exception as e:
                    logging.error(f"Error deleting song: {e}")
                    flash("An error occurred while deleting the song.")

            elif action == "toggle_limit":
                song_id = request.form["song_id"]

                try:
                    with sqlite3.connect("database.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(
                            "SELECT is_limited FROM songs WHERE song_id = ? AND user_id = ?",
                            (song_id, user_id),
                        )
                        is_limited = cursor.fetchone()[0]
                        new_status = 0 if is_limited else 1
                        cursor.execute(
                            "UPDATE songs SET is_limited = ? WHERE song_id = ? AND user_id = ?",
                            (new_status, song_id, user_id),
                        )
                        connect.commit()
                        flash("Song limit status successfully toggled.")
                except Exception as e:
                    logging.error(f"Error toggling song limit status: {e}")
                    flash("An error occurred while toggling the song limit status.")
 

            elif action == "add_songs_to_album":
                album_id = request.form["album_id"]
                song_id = request.form["song_id"]

                try:
                    with sqlite3.connect("database.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(
                            "UPDATE songs SET album_id = ? WHERE song_id = ? AND user_id = ?",
                            (album_id, song_id, user_id),
                        )
                        connect.commit()
                        flash("Song successfully added to the album.")
                except Exception as e:
                    logging.error(f"Error adding song to album: {e}")
                    flash("An error occurred while adding the song to the album.")

                    
            elif action == "delete_album":
                album_id = request.form["album_id"]

                try:
                    with sqlite3.connect("database.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(
                            "DELETE FROM ALBUM WHERE album_id = ? AND user_id = ?",
                            (album_id, user_id),
                        )
                        connect.commit()
                        flash("Album successfully deleted.")
                except Exception as e:
                    logging.error(f"Error deleting album: {e}")
                    flash("An error occurred while deleting the album.")

            elif action == "add_album":
                name = request.form["album_name"]
                release_date = request.form["release_date"]
                genre = request.form["genre"]

                try:
                    with sqlite3.connect("database.db") as connect:
                        cursor = connect.cursor()

                        cursor.execute(
                            "INSERT INTO ALBUM (name, release_date, genre, user_id) VALUES (?, ?, ?, ?)",
                            (name, release_date, genre, user_id),
                        )
                        connect.commit()
                        flash("Album successfully added.")
                except Exception as e:
                    logging.error(f"Error adding album: {e}")
                    flash("An error occurred while adding the album.")

            return redirect(url_for("artist_page"))

        try:
            with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()
                cursor.execute(
                    "SELECT concert_id, name, date, price, ticket_number FROM concerts WHERE user_id = ?",
                    (user_id,),
                )
                concerts = cursor.fetchall()

                cursor.execute(
                    "SELECT song_id, name, album_id, release_date, genre, duration, is_limited FROM songs WHERE user_id = ?",
                    (user_id,),
                )
                songs = cursor.fetchall()

                cursor.execute(
                    "SELECT album_id, name, release_date, genre FROM ALBUM WHERE user_id = ?",
                    (user_id,),
                )
                albums = cursor.fetchall()

            return render_template(
                "artist.html",
                concerts=concerts,
                songs=songs,
                albums=albums,
                user_id=user_id,
            )

        except Exception as e:
            logging.error(f"Error fetching artist page: {e}")
            flash("An error occurred while fetching the artist page.")
            return redirect(url_for("user"))
    else:
        flash("Access denied: You are not an artist.")
        return redirect(url_for("user"))


@app.route("/buy_ticket", methods=["POST"])
def buy_ticket():
    if "user_id" in session:
        user_id = session["user_id"]
        concert_id = request.form["concert_id"]
        transaction_id = "".join(random.choices(string.ascii_letters + string.digits, k=12))
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()

                # Get the concert details
                cursor.execute(
                    "SELECT name, price, ticket_number, user_id, date FROM concerts WHERE concert_id = ?",
                    (concert_id,)
                )
                concert = cursor.fetchone()
                if not concert:
                    flash("Concert not found.")
                    return redirect(url_for("user"))

                name, price, ticket_number, singer_id, concert_date = concert

                # Check if user has enough balance
                cursor.execute(
                    "SELECT balance FROM USERS WHERE user_id = ?",
                    (user_id,)
                )
                balance = cursor.fetchone()[0]
                if balance < price:
                    flash("Insufficient balance.")
                    return redirect(url_for("user"))

                # Check the number of tickets already sold
                cursor.execute(
                    "SELECT COUNT(*) FROM TICKETS WHERE concert_id = ?",
                    (concert_id,)
                )
                sold_tickets = cursor.fetchone()[0]
                if sold_tickets >= ticket_number:
                    flash("No more tickets available for this concert.")
                    return redirect(url_for("user"))

                # Deduct the ticket price from user's balance
                new_balance = balance - price
                cursor.execute(
                    "UPDATE USERS SET balance = ? WHERE user_id = ?",
                    (new_balance, user_id)
                )

                # Add the ticket price to the singer's balance
                cursor.execute(
                    "SELECT balance FROM USERS WHERE user_id = ?",
                    (singer_id,)
                )
                singer_balance = cursor.fetchone()[0]
                new_singer_balance = singer_balance + price
                cursor.execute(
                    "UPDATE USERS SET balance = ? WHERE user_id = ?",
                    (new_singer_balance, singer_id)
                )

                # Create a transaction record for the user to singer transaction
                cursor.execute(
                    "INSERT INTO TRANSACTIONS (transaction_id, user_id, recipient_id, amount, date) VALUES (?, ?, ?, ?, ?)",
                    (transaction_id, user_id, singer_id, price, date)
                )

                # Add 10% of the ticket price to the admin's balance (assuming admin has user_id = 1)
                admin_id = 1
                admin_share = price * 0.1
                cursor.execute(
                    "SELECT balance FROM USERS WHERE user_id = ?",
                    (admin_id,)
                )
                admin_balance = cursor.fetchone()[0]
                new_admin_balance = admin_balance + admin_share
                cursor.execute(
                    "UPDATE USERS SET balance = ? WHERE user_id = ?",
                    (new_admin_balance, admin_id)
                )

                # Deduct the 10% from singer's balance
                new_singer_balance -= admin_share
                cursor.execute(
                    "UPDATE USERS SET balance = ? WHERE user_id = ?",
                    (new_singer_balance, singer_id)
                )

                transaction_id = "".join(random.choices(string.ascii_letters + string.digits, k=12))
                # Create a transaction record for the singer to admin transaction
                cursor.execute(
                    "INSERT INTO TRANSACTIONS (transaction_id, user_id, recipient_id, amount, date) VALUES (?, ?, ?, ?, ?)",
                    (transaction_id, singer_id, admin_id, admin_share, date)
                )

                # Generate the ticket
                cursor.execute(
                    "INSERT INTO TICKETS (concert_id, user_id, ticket_price) VALUES (?, ?, ?)",
                    (concert_id, user_id, price)
                )

                # Commit the transaction
                connect.commit()
                session["balance"] = new_balance
                flash("Ticket successfully purchased.")
                return redirect(url_for("user"))
        except Exception as e:
            logging.error(f"Error purchasing ticket: {e}")
            flash("An error occurred while purchasing the ticket.")
            return redirect(url_for("user"))
    else:
        return redirect(url_for("login"))


@app.route("/create_playlist", methods=["GET", "POST"])
def create_playlist():
    if request.method == "POST":
        if "user_id" in session:
            user_id = session["user_id"]
            playlist_name = request.form["playlist_name"]
            genre = request.form["genre"]
            is_private = request.form.get("is_private") == "on"

            try:
                with sqlite3.connect("database.db") as connect:
                    cursor = connect.cursor()
                    cursor.execute(
                        "INSERT INTO playlists (creator_id, playlist_name, genre, is_private) VALUES (?, ?, ?, ?)",
                        (user_id, playlist_name, genre, is_private),
                    )
                    connect.commit()
                    flash("Playlist successfully created.")
                    return redirect(url_for("create_playlist"))
            except Exception as e:
                logging.error(f"Error creating playlist: {e}")
                flash("An error occurred while creating the playlist.")

    if "user_id" in session:
        user_id = session["user_id"]
        try:
            with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()
                cursor.execute(
                    "SELECT playlist_id, playlist_name FROM playlists WHERE creator_id = ?",
                    (user_id,)
                )
                playlists = cursor.fetchall()

                def get_songs_in_playlist(playlist_id):
                    cursor.execute(
                        """
                        SELECT songs.song_id, songs.name, songs.genre, songs.duration
                        FROM songs
                        INNER JOIN playlist_songs ON songs.song_id = playlist_songs.song_id
                        WHERE playlist_songs.playlist_id = ?
                        """,
                        (playlist_id,)
                    )
                    return cursor.fetchall()

            return render_template("create_playlist.html", playlists=playlists, get_songs_in_playlist=get_songs_in_playlist)

        except Exception as e:
            logging.error(f"Error fetching playlists: {e}")
            flash("An error occurred while fetching playlists.")
            return redirect(url_for("user"))

    else:
        flash("You are not authorized to access this page.")
        return redirect(url_for("home_page"))


@app.route("/add_song_to_playlist", methods=["POST"])
def add_song_to_playlist():
    if "user_id" in session:
        user_id = session["user_id"]
        playlist_id = request.form["playlist_id"]
        song_id = request.form["song_id"]

        try:
            with sqlite3.connect("database.db") as connect:
                cursor = connect.cursor()

                # Check if the song is limited
                cursor.execute(
                    "SELECT is_limited FROM songs WHERE song_id = ?",
                    (song_id,)
                )
                is_limited = cursor.fetchone()[0]

                if is_limited:
                    flash("Cannot add a limited song to the playlist.")
                    return redirect(url_for("create_playlist"))

                # Add the song to the playlist
                cursor.execute(
                    "INSERT INTO playlist_songs (playlist_id, song_id) VALUES (?, ?)",
                    (playlist_id, song_id)
                )
                connect.commit()
                flash("Song successfully added to the playlist.")
                return redirect(url_for("create_playlist"))

        except Exception as e:
            logging.error(f"Error adding song to playlist: {e}")
            flash("An error occurred while adding the song to the playlist.")
            return redirect(url_for("create_playlist"))

    else:
        flash("You are not authorized to perform this action.")
        return redirect(url_for("home_page"))

@app.route('/follows', methods=['GET', 'POST'])
def follows():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        # Handle follow/unfollow/request actions
        if request.method == 'POST':
            if 'user_id_to_follow' in request.form:
                user_id_to_follow = request.form['user_id_to_follow']
                if user_id != user_id_to_follow:
                    cursor.execute("INSERT INTO FOLLOWS (user_id1, user_id2) VALUES (?, ?)", (user_id, user_id_to_follow))
                    conn.commit()
            elif 'user_id_to_unfollow' in request.form:
                user_id_to_unfollow = request.form['user_id_to_unfollow']
                cursor.execute("DELETE FROM FOLLOWS WHERE user_id1 = ? AND user_id2 = ?", (user_id, user_id_to_unfollow))
                conn.commit()
            elif 'friend_id' in request.form:
                friend_id = request.form['friend_id']
                cursor.execute("INSERT INTO FRIENDS (user_id, friend_id) VALUES (?, ?)", (user_id, friend_id))
                conn.commit()

        # Fetch followers
        cursor.execute("""
            SELECT u.user_id, u.name FROM USERS u 
            JOIN FOLLOWS f ON u.user_id = f.user_id1 
            WHERE f.user_id2 = ?
        """, (user_id,))
        followers = cursor.fetchall()

        # Fetch followings
        cursor.execute("""
            SELECT u.user_id, u.name FROM USERS u 
            JOIN FOLLOWS f ON u.user_id = f.user_id2 
            WHERE f.user_id1 = ?
        """, (user_id,))
        following = cursor.fetchall()

        cursor.execute("""
        SELECT u.user_id, u.name FROM USERS u
        JOIN FRIENDS f ON u.user_id = f.friend_id
        WHERE f.user_id = ?
    """, (user_id,))
        friends = cursor.fetchall()

        # Fetch all pending friendship requests
        cursor.execute("""
            SELECT u.user_id, u.name FROM USERS u
            JOIN friendship_requests f ON u.user_id = f.sender_id
            WHERE f.receiver_id = ?
        """, (user_id,))
        pending_requests = cursor.fetchall()

        # Fetch all premium users with action buttons
        cursor.execute("""
            SELECT user_id, name FROM USERS
            WHERE user_id != ? AND is_premium = 1
        """, (user_id,))
        all_users = cursor.fetchall()

        # Check if premium users are already friends
        cursor.execute("""
            SELECT u.user_id FROM USERS u
            JOIN FRIENDS f ON u.user_id = f.friend_id
            WHERE f.user_id = ?
        """, (user_id,))
        friends_set = {row[0] for row in cursor.fetchall()}

    finally:
        conn.close()

    following_set = {follow[0] for follow in following}

    return render_template('follows.html', followers=followers, following=following, all_users=all_users,
    following_set=following_set, friends=friends, pending_requests=pending_requests, friends_set=friends_set)


@app.route('/send_friendship_request', methods=['POST'])
def send_friendship_request():
    if "user_id" not in session:
        return redirect(url_for("login"))

    sender_id = session["user_id"]
    receiver_id = request.form['friend_id']

    if sender_id == receiver_id:
        flash("You cannot send a request to yourself.")
        return redirect(url_for("follows"))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, is_premium FROM users WHERE user_id = ?", (receiver_id,))
        receiver = cursor.fetchone()

        if not receiver:
            flash("Invalid user ID.")
            return redirect(url_for("follows"))

        if not session["is_premium"] or not receiver["is_premium"]:
            flash("Both sender and receiver must be premium users.")
            return redirect(url_for("follows"))

        cursor.execute(
            "SELECT * FROM friendship_requests WHERE sender_id = ? AND receiver_id = ?",
            (sender_id, receiver_id)
        )
        if cursor.fetchone():
            flash("Friendship request already sent.")
            return redirect(url_for("follows"))

        cursor.execute(
            "SELECT * FROM friends WHERE user_id = ? AND friend_id = ?",
            (sender_id, receiver_id)
        )
        if cursor.fetchone():
            flash("You are already friends with this user.")
            return redirect(url_for("follows"))

        cursor.execute(
            "INSERT INTO friendship_requests (sender_id, receiver_id) VALUES (?, ?)",
            (sender_id, receiver_id)
        )
        conn.commit()
        conn.close()
        flash("Friendship request sent.")
    except Exception as e:
        logging.error(f"Error sending friendship request: {e}")
        flash("An error occurred.")

    return redirect(url_for("follows"))


@app.route('/accept_friendship_request', methods=['POST'])
def accept_friendship_request():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    sender_id = request.form['sender_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO friends (user_id, friend_id) VALUES (?, ?)",
            (user_id, sender_id)
        )
        cursor.execute(
            "INSERT INTO friends (user_id, friend_id) VALUES (?, ?)",
            (sender_id, user_id)
        )
        cursor.execute(
            "DELETE FROM friendship_requests WHERE sender_id = ? AND receiver_id = ?",
            (sender_id, user_id)
        )
        conn.commit()
        conn.close()
        flash("Friendship request accepted.")
    except Exception as e:
        logging.error(f"Error accepting friendship request: {e}")
        flash("An error occurred.")

    return redirect(url_for("follows"))

@app.route('/decline_friendship_request', methods=['POST'])
def decline_friendship_request():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    sender_id = request.form['sender_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM friendship_requests WHERE sender_id = ? AND receiver_id = ?",
            (sender_id, user_id)
        )
        conn.commit()
        conn.close()
        flash("Friendship request declined.")
    except Exception as e:
        logging.error(f"Error declining friendship request: {e}")
        flash("An error occurred.")

    return redirect(url_for("follows"))



@app.route('/chat', methods=['GET', 'POST'])
def chat():
    current_user_id = session.get('user_id')
    friend_id = request.args.get('friend_id')

    if not current_user_id or not friend_id:
        return redirect(url_for('follows'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        text = request.form['text']
        date = datetime.now()
        cursor.execute("""
            INSERT INTO messages (sender_id, receiver_id, text, date)
            VALUES (?, ?, ?, ?)
        """, (current_user_id, friend_id, text, date))
        conn.commit()

    cursor.execute("SELECT name FROM users WHERE user_id = ?", (friend_id,))
    friend_name = cursor.fetchone()['name']

    cursor.execute("""
        SELECT m.text, m.date, u.name AS sender_name
        FROM messages m
        JOIN users u ON m.sender_id = u.user_id
        WHERE (m.sender_id = ? AND m.receiver_id = ?) OR (m.sender_id = ? AND m.receiver_id = ?)
        ORDER BY m.date ASC
    """, (current_user_id, friend_id, friend_id, current_user_id))
    messages = cursor.fetchall()

    conn.close()

    return render_template('chat.html', friend_name=friend_name, friend_id=friend_id, messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    current_user_id = session.get('user_id')
    receiver_id = request.form.get('receiver_id')
    text = request.form.get('text')

    if not current_user_id or not receiver_id or not text:
        return redirect(url_for('chat', friend_id=receiver_id))

    conn = get_db_connection()
    cursor = conn.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("""
            INSERT INTO messages (sender_id, receiver_id, text, date)
            VALUES (?, ?, ?, ?)
        """, (current_user_id, receiver_id, text, date))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

    return redirect(url_for('chat', friend_id=receiver_id))

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    song_id = request.args.get('song_id', None)
    playlist_id = request.args.get('playlist_id', None)
    album_id = request.args.get('album_id', None)

    if request.method == 'POST':
        user_id = request.form['user_id']
        comment_text = request.form['comment']

        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()

            if song_id:
                c.execute("INSERT INTO song_comments (user_id, song_id, comment) VALUES (?, ?, ?)",
                          (user_id, song_id, comment_text))
            elif playlist_id:
                c.execute("INSERT INTO playlist_comments (user_id, playlist_id, comment) VALUES (?, ?, ?)",
                          (user_id, playlist_id, comment_text))
            elif album_id:
                c.execute("INSERT INTO album_comments (user_id, album_id, comment) VALUES (?, ?, ?)",
                          (user_id, album_id, comment_text))

            conn.commit()
            conn.close()

            return redirect(url_for('comment', song_id=song_id, playlist_id=playlist_id, album_id=album_id))
        except sqlite3.Error as e:
            logging.error(f"An error occurred while saving the comment: {e}")
            return "An error occurred while saving your comment. Please try again later."

    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        if song_id:
            song_comments = c.execute(
                "SELECT * FROM song_comments WHERE song_id = ?", (song_id,)).fetchall()
            playlist_comments = []
            album_comments = []
        elif playlist_id:
            song_comments = []
            playlist_comments = c.execute(
                "SELECT * FROM playlist_comments WHERE playlist_id = ?", (playlist_id,)).fetchall()
            album_comments = []
        elif album_id:
            song_comments = []
            playlist_comments = []
            album_comments = c.execute(
                "SELECT * FROM album_comments WHERE album_id = ?", (album_id,)).fetchall()
        else:
            song_comments = c.execute("SELECT * FROM song_comments").fetchall()
            playlist_comments = c.execute(
                "SELECT * FROM playlist_comments").fetchall()
            album_comments = c.execute(
                "SELECT * FROM album_comments").fetchall()

        conn.close()

        return render_template('comment.html', song_comments=song_comments, playlist_comments=playlist_comments, album_comments=album_comments, user_id=session['user_id'], song_id=song_id, playlist_id=playlist_id, album_id=album_id)
    except sqlite3.Error as e:
        logging.error(f"An error occurred while fetching the comments: {e}")
        return "An error occurred while fetching the comments. Please try again later."



    return redirect(url_for('chat', friend_id=receiver_id))


if __name__ == "__main__":
    app.run(debug=True)
