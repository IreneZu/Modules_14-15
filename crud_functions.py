# # План написания админ панели
# # Задача "Продуктовая база":

import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')


def fill_in_products():
    cursor.execute("DELETE FROM Products")
    tit = {1: 'Пекинский салат (16 к/кал)', 2: 'Редис (25 к/кал)', 3: 'Брокколи (34 к/кал)',
           4: 'Зеленый горошек (55 к/кал)'}
    for i in range(1, 5):
        cursor.execute(" INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                       (f"Product{i}", tit[i], i * 100))
    connection.commit()


def get_all_products():
    products = cursor.execute("SELECT * FROM Products").fetchall()
    return products
