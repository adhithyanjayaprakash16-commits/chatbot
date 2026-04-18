import sqlite3
import os

DB_NAME = "adhibus_bookings.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Table for bookings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pnr TEXT UNIQUE,
            source TEXT,
            destination TEXT,
            travel_date TEXT,
            passengers INTEGER,
            amount REAL,
            status TEXT DEFAULT 'CONFIRMED',
            booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for user queries (Logs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT,
            intent_tag TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_booking(pnr, source, dest, date, passengers, amount):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bookings (pnr, source, destination, travel_date, passengers, amount)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (pnr, source, dest, date, int(passengers), amount))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"DB Error: {e}")
        return False

def log_query(msg, response, tag):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO logs (user_message, bot_response, intent_tag) VALUES (?, ?, ?)', (msg, response, tag))
        conn.commit()
        conn.close()
    except:
        pass

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
