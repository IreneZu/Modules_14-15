# # Выбор элементов и функции в SQL запросах
# # Задача "Средний баланс пользователя":

import sqlite3

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

cursor.execute("DELETE FROM Users")

for i in range(1, 10+1):
    cursor.execute(" INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f"User{i}", f"example{i}@gmail.com", i * 10, 1000))

cursor.execute("UPDATE Users SET balance = ? WHERE (age / 10) % 2 = ?", (500, 1))

cursor.execute("DELETE FROM Users WHERE (age / 10) % 3 = ?", (1,))
cursor.execute("DELETE FROM Users WHERE id == ?", (6,))

cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchone()[0]

cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = cursor.fetchone()[0]

print(all_balances / total_users)

connection.commit()
connection.close()