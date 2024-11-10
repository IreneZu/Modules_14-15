# # Создание БД, добавление, выбор и удаление элементов.
# # Задача "Первые пользователи":

import sqlite3
import random

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

for i in range(1, 10+1):
    cursor.execute(" INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f"User{i}", f"example{i}@gmail.com", i * 10, 1000))

cursor.execute("UPDATE Users SET balance = ? WHERE (age / 10) % 2 = ?", (500, 1))

cursor.execute("DELETE FROM Users WHERE (age / 10) % 3 = ?", (1,))
# SELECT FROM WHERE GROUP BY HAVING ORDER BY

cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))

users = cursor.fetchall()
for user in users:
    print(f'Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}')

connection.commit()
connection.close()