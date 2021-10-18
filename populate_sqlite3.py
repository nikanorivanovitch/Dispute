import sqlite3
import os
import hashlib

os.remove("database.db")
with open("database", "w") as fp:
    pass

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# /!\ DONT USE IT IN PRODUCTION /!\
sql_file = open("sqlite3_init.sql")
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)
#connection.commit()

def username_exist(username): #return bool, when create an account first check if the user already exit
    for row in cursor.execute("SELECT username FROM user"):
        if(username == row):
            return True
    return False

def auth_user(username,passhash): #return bool, authenticate the user
    request = """ SELECT count(*) FROM user WHERE username = (?) AND hash = (?); """
    data_tuple = (username, passhash)
    cursor.execute(request,data_tuple)
    rep = cursor.fetchone()
    print(rep[0])
    if(rep[0] == 1):
        return True
    else :
        return False

def create_user(username,passhash,mail): #return null, create a user
    cursor.execute("SELECT max(user_id) FROM user")
    mama = cursor.fetchone()

    sqlite_insert_with_param = """INSERT INTO user(user_id, user_name, user_hash,  user_email) VALUES (?, ?, ?, ?);""" #https://pynative.com/python-sqlite-insert-into-table/

    data_tuple = (mama[0]+1, username, passhash,mail)
    cursor.execute(sqlite_insert_with_param, data_tuple)

def all_user():
    for row in cursor.execute("SELECT * FROM user"):
        print(row)

def matchHashedText(hashed_from_user, hash_from_db): #check if the hash from user correspond to the hash stock in db
    """
    Check for the text in the hashed text
    """
    _hashedText, salt = hashed_from_user.split(':')
    print(salt)
    return _hashedText == hashlib.sha256(salt.encode() + hash_from_db.encode()).hexdigest()

create_user("mama","mdp","mama@wanado.fr")
all_user()
#print(auth_user("mama","mdp"))

