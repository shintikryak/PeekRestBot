import sqlite3

def initialize_db():
    conn = sqlite3.connect("restaurants.db")
    cursor = conn.cursor()

    # Таблица для локаций
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    # Таблица для ресторанов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location_id INTEGER,
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
    """)

    # Таблица для столиков
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER,
        capacity INTEGER,
        available BOOLEAN,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
    )
    """)

    # Очистка таблиц
    cursor.execute("DELETE FROM locations")
    cursor.execute("DELETE FROM restaurants")
    cursor.execute("DELETE FROM tables")

    # Тестовые данные
    locations = [
        (1, "Центр"),
        (2, "Север"),
        (3, "Юг"),
    ]
    cursor.executemany("INSERT INTO locations (id, name) VALUES (?, ?)", locations)

    restaurants = [
        (1, "Ресторан А", 1),  # Центр
        (2, "Ресторан Б", 2),  # Север
        (3, "Ресторан В", 1),  # Центр
        (4, "Ресторан Г", 3),  # Юг
    ]
    cursor.executemany("INSERT INTO restaurants (id, name, location_id) VALUES (?, ?, ?)", restaurants)

    tables = [
        (1, 2, 1), (1, 4, 1), (1, 6, 0),  # Столики для ресторана А
        (2, 2, 1), (2, 4, 1), (2, 6, 1),  # Столики для ресторана Б
        (3, 2, 1), (3, 4, 0), (3, 8, 1),  # Столики для ресторана В
        (4, 2, 1), (4, 6, 1), (4, 8, 1),  # Столики для ресторана Г
    ]
    cursor.executemany("INSERT INTO tables (restaurant_id, capacity, available) VALUES (?, ?, ?)", tables)

    conn.commit()
    conn.close()

# Инициализация базы данных
initialize_db()
