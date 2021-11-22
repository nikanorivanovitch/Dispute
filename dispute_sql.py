import sqlite3
import os
import hashlib
import random
import json

def NewToken():

    out = ""

    for x in range(64):

        out+=chr(ord('A')+random.randint(0,64))

    return sha256(out)

def sha256(input):

    return hashlib.sha256(input.encode()).hexdigest()


# Objet qui va gérer les demandes d'amitié en temp réel
class FriendshipHandler:

    def __init__(self):
        self.Invites = {}

# Objet qui va gérer les sessions ouvertes et fermer les sessions inactives
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

class Channel:

    def __init__(self):

        self.id=None
        self.name=None
        self.users=None

class Message:

    def __init__(self):

        self.id=None
        self.content=None
        self.sender=None
        self.channel_id=None

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

        return user

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

        request = "INSERT INTO server(server_id, server_name, server_creator_id) VALUES (?, ?, ?);"
        self.cursor.execute(request, (server.id, server.name, server.creator.id));

        server.id = self.GetIncrementOfTable("server")

        self.AddUserToServer(server.creator.id, server.id)

        self.GetEntireTable("server")
        self.GetEntireTable("membership")

        return server

    def RenameServer(self, server):

        request = "UPDATE server SET server_name = (?) WHERE server_id = (?);"
        self.cursor.execute(request, (server.name, server.id))

        return server

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

    #############
    # Connexion #
    #############

    def AddUserToServer(self, user_id, server_id):

        request = "SELECT * FROM membership WHERE user_id = (?) AND server_id = (?);"
        self.cursor.execute(request, (user_id, server_id))

        result = self.cursor.fetchall()

        if(len(result)!=0):
            return False

        request = "INSERT INTO membership(user_id, server_id) VALUES (?, ?);"
        self.cursor.execute(request, (user_id, server_id))

        return True

    def AddFriendShip(user1_id, user2_id):

        request = "INSERT INTO friendship() VALUES (?, ?);"
        self.cursor.execute(request, (user1_id, user2_id))

    def RemoveFriendShip():

    def DoesFriendShipExists():

        request = "SELECT * FROM friendship WHERE friend1_id = (?) AND friend2_id = (?);"
        
        if(len(self.cursor.execute(request, (friend1_id, friend2_id)).fetchall())==1):
            return 1

        if(len(self.cursor.execute(request, (friend2_id, friend1_id)).fetchall())==1):
            return 2

        return False



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


