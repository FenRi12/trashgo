import sqlite3
from typing import List, Dict

DB_NAME = "orders.db"

# ----------------- Инициализация базы -----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            phone TEXT,
            house TEXT,
            entrance TEXT,
            apartment TEXT,
            floor TEXT,
            door_code TEXT,
            latitude REAL,
            longitude REAL,
            time_slot TEXT,
            bags INTEGER,
            payment TEXT,
            courier_id INTEGER,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

# ----------------- Добавление заказа -----------------
def add_order(**kwargs) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    fields = ", ".join(kwargs.keys())
    placeholders = ", ".join("?" for _ in kwargs)
    values = list(kwargs.values())
    cursor.execute(f"INSERT INTO orders ({fields}) VALUES ({placeholders})", values)
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    return order_id

# ----------------- Безопасные функции конверсии -----------------
def safe_int(value):
    try:
        return int(value)
    except:
        return 0

def safe_float(value):
    try:
        return float(value)
    except:
        return 0.0

def safe_str(value):
    if value is None:
        return ""
    return str(value)

# ----------------- Получение всех заказов пользователя -----------------
def get_orders_by_user(user_id):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY order_id DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    orders = []
    for row in rows:
        orders.append({
            "order_id": row[0],
            "user_id": row[1],
            "first_name": row[2],
            "last_name": row[3],
            "username": row[4],
            "phone": row[5],
            "house": row[6],
            "entrance": row[7],
            "apartment": row[8],
            "floor": row[9],
            "door_code": row[10],
            "latitude": row[11],
            "longitude": row[12],
            "time_slot": row[13],
            "bags": row[14],
            "payment": row[15],
            "courier_id": row[16],
            "status": row[17],
            "created_at": row[18],
        })
    return orders


# ----------------- Получение конкретного заказа -----------------
def get_order(order_id: int) -> Dict:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return {}
    return {
        "order_id": safe_int(row[0]),
        "user_id": safe_int(row[1]),
        "first_name": safe_str(row[2]),
        "last_name": safe_str(row[3]),
        "username": safe_str(row[4]),
        "phone": safe_str(row[5]),
        "house": safe_str(row[6]),
        "entrance": safe_str(row[7]),
        "apartment": safe_str(row[8]),
        "floor": safe_str(row[9]),
        "door_code": safe_str(row[10]),
        "latitude": safe_float(row[11]),
        "longitude": safe_float(row[12]),
        "time_slot": safe_str(row[13]),
        "bags": safe_int(row[14]),
        "payment": safe_str(row[15]),
        "courier_id": safe_int(row[16]),
        "status": safe_str(row[17]),
        "created_at": safe_str(row[18]),
    }

# ----------------- Обновление статуса заказа -----------------
def update_order_status(order_id: int, status: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status=? WHERE order_id=?", (status, order_id))
    conn.commit()
    conn.close()
