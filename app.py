from app import db, app  # Import both db and app

# Drop and create all tables
with app.app_context():
    db.engine.execute('''
        DROP TABLE IF EXISTS users
    ''')

    db.engine.execute('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL,
            balance INTEGER NOT NULL,
            password VARCHAR(50) NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL,
            address VARCHAR(100),
            profilepic BLOB,
            is_artist BOOLEAN,
            is_premium BOOLEAN
        )
    ''')

    db.engine.execute('''
        INSERT INTO users (name, balance, password, email, address, is_artist, is_premium) VALUES
        ('John Doe', 100, 'password123', 'john@example.com', '123 Main St', 0, 1),
        ('Jane Smith', 200, 'password456', 'jane@example.com', '456 Main St', 1, 0)
    ''')
