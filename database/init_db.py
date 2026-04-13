from database.db import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
                   user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   bio TEXT) ''')

    # followers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS followers (
                   follower_id INTEGER,
                   following_id INTEGER,
                   PRIMARY KEY (follower_id, following_id),
                   FOREIGN KEY (follower_id) REFERENCES users(user_id),
                   FOREIGN KEY (following_id) REFERENCES users(user_id))''')
    
    # posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
                   post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   content TEXT,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY(user_id) REFERENCES users(user_id))''')
    
    # interactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
                   interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   post_id INTEGER,
                   like INTEGER DEFAULT 0,
                   comment TEXT,
                   FOREIGN KEY(user_id) REFERENCES users(user_id),
                   FOREIGN KEY(post_id) REFERENCES posts(post_id)) ''')
    
    conn.commit()
    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()