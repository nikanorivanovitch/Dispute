import sqlite3
import os
import hashlib
import random
import json

'''os.remove("database.db")
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
#print(auth_user("mama","mdp"))'''

def NewToken():

    out = ""

    for x in range(64):

        out+=chr(ord('A')+random.randint(0,64))

    return sha256(out)

def sha256(input):

    return hashlib.sha256(input.encode()).hexdigest()

class Cookies:

    def __init__(self):

        self.Token=None

class SessionHandler:

    def __init__(self):
        self.Sessions = {}

    def OpenSession(self, User):

        UserAlreadyPresent = False

        for token in self.Sessions:

            if(self.Sessions[token].id == User.id):
                return False

        NT = NewToken()
        self.Sessions[NT] = User

        return NT

    def CloseSession(self, Token):

        if(Token in self.Sessions):
            self.Sessions.pop(Token)
            return True

        return False

    def IsValidSession(self, Token):

        return (Token in self.Sessions)

class User:

    def __init__(self):

        self.id=None
        self.name=None
        self.hash=None
        self.email=None

class Server:

    def __init__(self):

        self.id=None
        self.name=None
        self.channels=None
        self.creator=None
        self.user=None

class Channel:

    def __init__(self):

        self.id=None
        self.name=None
        self.users=None

class Message:

    def __init__(self):

        pass

class DatabaseHandler:

    def __init__(self, filename):

        self.filename = filename

        self.connection = sqlite3.connect(self.filename, check_same_thread=False, isolation_level=None)
        self.cursor = self.connection.cursor()

    def ResetDatabaseConnection(self):

        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()

    def ResetEntireDatabase(self):

        self.connection.close()

        os.remove(self.filename)
        with open(self.filename, "w") as fp:
            pass

        self.ResetDatabaseConnection()

        sql_file = open("sqlite3_init.sql")
        sql_as_string = sql_file.read()
        self.cursor.executescript(sql_as_string)

    def GetEntireTable(self, tablename):

        request = "SELECT * FROM " + tablename + ";"
        self.cursor.execute(request)
        print(self.cursor.fetchall())

    def GetIncrementOfTable(self, table):

        request = "SELECT last_insert_rowid() FROM" + table + ";"
        self.cursor.execute(request)

        return int(self.cursor.fetchall()[0][0])

    ################
    # Utilisateurs #
    ################

    def CanUserBeCreated(self, user):

        request = "SELECT * FROM user WHERE user_email=(?)"
        self.cursor.execute(request, (user.email,))

        result = self.cursor.fetchall()

        if(len(result)==0):
            return True

        return False

    def CreateUser(self, user):

        if(not self.CanUserBeCreated(user)):
            return False

        print("user to add : ",user.__dict__)

        request = "INSERT INTO user(user_id, user_name, user_hash,  user_email) VALUES (?, ?, ?, ?);"
        self.cursor.execute(request, (user.id, user.name, sha256(str(user.hash)+str(user.email)+str("CecientEstMon__Secret56SAGIPognonDedingue")), user.email))

        user.id = self.GetIncrementOfTable("user")

        return user

    def RenameUser(self, user):

        request = "UPDATE user SET user_name = (?) WHERE user_id = (?);"
        self.cursor.execute(request, (user.name, user.id))

    def DoesThisUserExist(self, user):

        request = "SELECT * FROM user WHERE user_email = (?) AND user_hash = (?);"
        print(sha256(str(user.hash)+str(user.email)+str("CecientEstMon__Secret56SAGIPognonDedingue")))
        self.cursor.execute(request, (user.email, sha256(str(user.hash)+str(user.email)+str("CecientEstMon__Secret56SAGIPognonDedingue"))))

        result = self.cursor.fetchall()

        if(len(result)==1):
            result=result[0]
            user.id = result[0]
            user.name = result[1]
            return user

        return False

    def GetUserFromId(self, user_id):

        request = "SELECT * FROM user WHERE user_id = (?);"
        self.cursor.execute(request, (sql_hash))

    ###########
    # Serveur #
    ###########

    def CreateServer(self, server):

        server.id = self.GetIncrementOfTable("server") + 1

        request = "INSERT INTO user(server_id, server_name, server_creator_id) VALUES (?, ?, ?);"
        self.cursor.execute(request, (server.id, server.name, server.creator.id));

        return server

    def RenameServer(self, server):

        request = "UPDATE server SET server_name = (?) WHERE server_id = (?);"
        self.cursor.execute(request, (server.name, server.id))

        pass

    ###########
    # Channel #
    ###########

    def CreateChannel(self, channel):

        pass

    def RenameChannel(self, channel):

        pass

    ###########
    # Message #
    ###########

    def CreateMessage(self, message):

        pass

    def UpdateMessage(self, message):

        pass



'''O = SQL_DAO("database.db")
O.ResetEntireDatabase()
O.GetEntireTable("user")

U = User()
U.name = "Dédé la fripouille"
U.hash = "gneugneu"
U.email = "dede@fripouillon.com"
U.id = 1

O.CreateUser(U)
O.GetEntireTable("user")
U.name = "Gneugneu"
O.RenameUser(U)
O.GetEntireTable("user")
O.GetIncrementOfTable("user")

print(NewToken())'''


