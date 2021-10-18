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
    request = """ SELECT count(*) FROM user WHERE username = (?) AND hash = (?); """
    data_tuple = (username, passhash)
    cursor.execute(request,data_tuple)
    rep = cursor.fetchone()
    print(rep[0])
    if(rep[0] == 1):
        return True
    else :
        return False
    

def create_user(username,passhash):
    cursor.execute("SELECT max(user_id) FROM user")
    mama = cursor.fetchone()

    sqlite_insert_with_param = """INSERT INTO user(user_id, username, hash) VALUES (?, ?, ?);""" #https://pynative.com/python-sqlite-insert-into-table/

    data_tuple = (mama[0]+1, username, passhash)
    cursor.execute(sqlite_insert_with_param, data_tuple)

def all_user():
    for row in cursor.execute("SELECT * FROM user"):
        print("allez les bleus : ",row)

create_user("mama","mdp")
all_user()
print(auth_user("mama","mdp"))

