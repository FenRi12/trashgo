import sqlite3

DB_NAME = "orders.db"

def reset_orders_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Удаляем таблицу
    cursor.execute("DROP TABLE IF EXISTS orders;")

    # Создаем заново
    cursor.execute("""
        CREATE TABLE orders (
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
        );
    """)

    conn.commit()
    conn.close()
    print("✅ Таблица orders успешно сброшена и создана заново!")


if __name__ == "__main__":
    reset_orders_table()
