import sqlite3
from typing import Dict

DB_NAME = "users.db"

def init_users_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            phone TEXT,
            house TEXT,
            entrance TEXT,
            apartment TEXT,
            floor TEXT,
            door_code TEXT,
            latitude REAL DEFAULT 0.0,
            longitude REAL DEFAULT 0.0,
            language TEXT DEFAULT 'ru'
        )
    """)
    conn.commit()
    conn.close()


def save_user_data(user_id: int, **kwargs):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    exists = cursor.fetchone()

    if exists:
        fields = ", ".join([f"{k}=?" for k in kwargs.keys()])
        values = list(kwargs.values())
        values.append(user_id)
        cursor.execute(f"UPDATE users SET {fields} WHERE user_id=?", values)
    else:
        fields = ", ".join(kwargs.keys())
        placeholders = ", ".join("?" for _ in kwargs)
        values = list(kwargs.values())
        cursor.execute(
            f"INSERT INTO users (user_id, {fields}) VALUES (?, {placeholders})",
            [user_id] + values
        )

    conn.commit()
    conn.close()

def get_user(user_id: int) -> Dict:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {}

    return {
        "user_id": row[0],
        "first_name": row[1],
        "last_name": row[2],
        "username": row[3],
        "phone": row[4],
        "house": row[5],
        "entrance": row[6],
        "apartment": row[7],
        "floor": row[8],
        "door_code": row[9],
        "latitude": row[10] if len(row) > 10 else 0.0,
        "longitude": row[11] if len(row) > 11 else 0.0,
        "language": row[12] if len(row) > 12 else "ru"
    }
