import sqlite3
import os

os.remove("database.db")
with open("database", "w") as fp:
    pass

connection = sqlite3.connect("database.db")
cursor = connection.cursor()


sql_file = open("sqlite3_init.sql")
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)

for row in cursor.execute("SELECT * FROM user"):
    print(row)