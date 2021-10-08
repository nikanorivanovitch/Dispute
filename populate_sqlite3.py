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
connection.commit()

def username_exist(username): #return bool
    for row in cursor.execute("SELECT username FROM user"):
        if(username == row):
            return True
    return False

def auth_user(username,passhash): #return bool
    for row in cursor.execute("SELECT username,hash FROM user"):
        print(row[0],row[1])
        if(username == row[0] and passhash==row[1] ):
            return True
    return False

def create_user(username,passhash):
    cursor.execute("SELECT max(user_id) FROM user")
    print(cursor)
    for row in cursor.fetchall():
        print(type(row))
        print("yo : "+str(row))
    result = cursor.fetchmany(2)
    print(result)
    #cursor.execute("INSERT INTO user(user_id, username, hash) VALUES (?,?,?)",(cursor["user_id"],username,passhash))

def all_user():
    for row in cursor.execute("SELECT * FROM user"):
        print(row)

create_user("mama","mdp")
#all_user()
