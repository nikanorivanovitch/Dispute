import sqlite3
import os
import hashlib
import random
import json
from datetime import datetime

def NewToken():

    out = ""

    for x in range(64):

        out+=chr(ord('A')+random.randint(0,64))

    return sha256(out)

def NewFileToken():

    out = ""

    for x in range(64):

        i = (random.randint(0,50))

        if(i<25):
            out+=chr(ord('A')+i)
        else:
            out+=chr(ord('a')+i-25)

    return out

def sha256(input):

    return hashlib.sha256(input.encode()).hexdigest()

def allowed_extension(path, allowed_extensions):

    for extension in allowed_extensions:

        if(path.endswith(extension)):

            return True

    return False

def extension_of(path, allowed_extensions):

    for extension in allowed_extensions:

        if(path.endswith(extension)):

            return '.' + extension

    return None




# Objet qui va gérer les demandes d'amitié en temp réel
class FriendshipHandler:

    def __init__(self):
        self.Invites = {}

# Objet qui va gérer les sessions ouvertes et fermer les sessions inactives
class SessionHandler:

    def __init__(self):
        self.Sessions = {}
        self.InvertSessions = {}

    def OpenSession(self, User):

        UserAlreadyPresent = False

        for token in self.Sessions:

            if(self.Sessions[token].id == User.id):
                return False

        NT = NewToken()
        self.Sessions[NT] = User
        self.InvertSessions[User.id] = NT

        return NT

    def CloseSession(self, Token):

        if(Token in self.Sessions):
            self.InvertSessions.pop(self.Sessions[Token].id)
            self.Sessions.pop(Token)
            return True

        return False

    def IsValidSession(self, Token):

        return (Token in self.Sessions)

    def IsUserConnected(self, user_id):

        print(user_id)
        print(self.InvertSessions)

        if(user_id in self.InvertSessions):

            return self.InvertSessions[user_id]
            
        return False

class User:

    def __init__(self):

        self.id=None
        self.name=None
        self.hash=None
        self.email=None
        self.discriminant=None
        self.picture_token='default-picture'

class Server:

    def __init__(self):

        self.id=None
        self.name=None
        self.channels=None
        self.creator=None
        self.picture_token='default-server-picture'
        self.token=None

class Channel:

    def __init__(self):

        self.id=None
        self.name=None
        self.users=None
        self.server_id=None

class Message:

    def __init__(self):

        self.id=None
        self.content=None
        self.sender_id=None
        self.channel_id=None
        self.timestamp=None

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

        user.discriminant = random.randint(1,9999)

        print("user to add : ",user.__dict__)

        request = "INSERT INTO user(user_id, user_name, user_hash,  user_email, user_discriminant, user_picture_token) VALUES (?, ?, ?, ?, ?, ?);"
        self.cursor.execute(request, (user.id, user.name, sha256(str(user.hash)+str(user.email)+str("CecientEstMon__Secret56SAGIPognonDedingue")), user.email, user.discriminant, user.picture_token))

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

            print(result)

            result=result[0]
            user.id = result[0]
            user.name = result[1]
            user.discriminant = result[4]
            user.picture_token = result[5]
            return user

        return False

    def ChangeProfilePictureOfUser(self, user_id, picture_token):

        request = "UPDATE user SET user_picture_token = (?) WHERE user_id = (?);"
        self.cursor.execute(request, (picture_token, user_id))

    def GetUserFromId(self, user_id):

        print(user_id)

        request = "SELECT * FROM user WHERE user_id = (?);"
        self.cursor.execute(request, (user_id,))

        result = self.cursor.fetchall()

        if(len(result)==0):
            return None

        if(len(result)>1):
            print("DATABASE ERROR : Il existe plusieurs utilisateurs d'ID " + str(user_id))
            
        else:
            return result[0]

    def GetUserApparenceFromId(self, user_id):

        request = "SELECT * FROM user WHERE user_id=(?);"
        result = self.cursor.execute(request, (user_id,)).fetchall()

        if(len(result)==1):
        
            line = result[0]
            output = {"id" : line[0], "name" : line[1], "picture_token" : line[5]}

            return output

        return None

    def GetServersOfUser(self, user_id):

        request = "SELECT * FROM server WHERE server_id IN (SELECT server_id FROM membership WHERE user_id = (?));"

        result = self.cursor.execute(request, (user_id,)).fetchall()

        print(result)

        output = []

        for line in result:

            channel_dictionnary = self.GetChannelsOfServer(line[0])
            output.append({"id" : line[0], "name" : line[1], "image_token" : line[3], "channels" : channel_dictionnary, "users" : self.GetUserApparenceOfServer(line[0]), "token" : line[4]})

        print(output)

        return output

    def GetChannelsOfServer(self, server_id):

        request = "SELECT *  FROM channel WHERE channel_server_id = (?);"
        result = self.cursor.execute(request, (server_id,)).fetchall()

        output = []

        for line in result:
            output.append({"id" : line[0], "name" : line[1], "last_messages" : self.GetLastMessages(line[0])})

        return output

    def GetFriendsOfUser(self, user_id):

        request = "SELECT * FROM user WHERE user_id IN (SELECT friend1_id FROM friendship WHERE friend2_id = (?)) OR user_id IN (SELECT friend2_id FROM friendship WHERE friend1_id = (?));"

        result = self.cursor.execute(request, (user_id,user_id)).fetchall()

        print(result)

        output = []

        for line in result:
            output.append({"id" : line[0], "name" : line[1], "image_token" : line[5]})

        return output

    def GetUserOfServer(self, server_id):

        request = "SELECT user_id FROM membership WHERE server_id = (?);"
        result = self.cursor.execute(request, (server_id,)).fetchall()

        output = []

        for line in result:
            output.append(line[0])

        return output

    def GetUserOfServerFromToken(self, server_token):

        request = "SELECT user_id FROM membership WHERE server_id IN (SELECT server_id FROM server WHERE server_token = (?));"
        result = self.cursor.execute(request, (server_token,)).fetchall()

        output = []

        for line in result:
            output.append(line[0])

        return output

    def GetServerIdFromToken(self, server_token):

        request = "SELECT server_id FROM server WHERE server_token=(?);"
        result = self.cursor.execute(request, (server_token,)).fetchall()

        if(len(result)!=1):
            return None

        return int(result[0][0])

    def GetUserApparenceOfServer(self, server_id):

        request = "SELECT * FROM user WHERE user_id IN (SELECT user_id FROM membership WHERE server_id = (?));"
        result = self.cursor.execute(request, (server_id,)).fetchall()

        output = []

        for line in result:
            output.append({"id" : line[0], "name" : line[1], "image_token" : line[5], "discriminant" : line[4]})

        return output


    def GetServerOfChannel(self, channel_id):

        print(channel_id)
        print(type(channel_id))

        request = "SELECT channel_server_id FROM channel WHERE channel_id = (?);"
        result = self.cursor.execute(request, (channel_id,)).fetchall()

        if(len(result)==1):
            return result[0][0]

        return False

    def GetRelativesOfUser(self, user_id):

        print(self.GetFriendsOfUser(user_id))

        relatives_id = [x["id"] for x in self.GetFriendsOfUser(user_id)]

        print("FRIENDS : ",relatives_id)

        servers_id = [x["id"] for x in self.GetServersOfUser(user_id)]

        for server_id in servers_id:

            users_id = self.GetUserOfServer(server_id)

            for user_server_id in users_id:

                if(not user_server_id in relatives_id and user_server_id != user_id):

                    relatives_id.append(user_server_id)

        return relatives_id

    ###########
    # Serveur #
    ###########

    def GetServerToken(self):

        exitloop = False

        while(not exitloop):

            token = NewFileToken()

            request = "SELECT * FROM server WHERE server_token=(?)"
            result = self.cursor.execute(request, (token,)).fetchall()

            if(len(result)==0):

                exitloop = True

        return token

    def CreateServer(self, server):

        server.token = self.GetServerToken()

        request = "INSERT INTO server(server_id, server_name, server_creator_id, server_picture_token, server_token) VALUES (?, ?, ?, ?, ?);"
        self.cursor.execute(request, (server.id, server.name, server.creator.id, server.picture_token, server.token));

        server.id = self.GetIncrementOfTable("server")

        self.AddUserToServer(server.creator.id, server.id)

        self.GetEntireTable("server")
        self.GetEntireTable("membership")

        return server

    def RenameServer(self, server):

        request = "UPDATE server SET server_name = (?) WHERE server_id = (?);"
        self.cursor.execute(request, (server.name, server.id))

        return server

    def RemoveServer(self, server_id):

        request = "DELETE FROM server WHERE server_id = (?);"
        self.cursor.execute(request, (server_id,))

        request = "DELETE FROM channel WHERE channel_server_id = (?);"
        self.cursor.execute(request, (server_id,))

        request = "DELETE FROM message WHERE message_channel_id IN (SELECT channel_id FROM channel WHERE channel_server_id = (?));"
        self.cursor.execute(request, (server_id,))

        return True

    def IsServerAdmin(self, server_id, user):

        request = "SELECT * FROM server WHERE server_id = (?) AND server_creator_id = (?);"
        result = self.cursor.execute(request, (server_id, user.id)).fetchall()

        if(len(result)==1):
            return True

        return False


    ###########
    # Channel #
    ###########

    def CreateChannel(self, channel):

        request = "INSERT INTO channel(channel_id, channel_name, channel_server_id) VALUES (?, ?, ?);"
        self.cursor.execute(request, (channel.id, channel.name, channel.server_id))

        channel.id = self.GetIncrementOfTable("channel")

        return channel 

    def RenameChannel(self, channel):

        request = "UPDATE channel SET channel_name = (?) WHERE channel_id = (?);"
        self.cursor.execute(request, (channel.name, channel.id))

        return channel

    def RemoveChannel(self, channel_id):

        request = "DELETE FROM channel WHERE channel_id = (?);"
        self.cursor.execute(request, (channel_id,))

        return True

    ###########
    # Message #
    ###########

    def CreateMessage(self, message):

        request = "INSERT INTO message(message_id, message_timestamp, message_sender_id, message_content, message_channel_id) VALUES (?, ?, ?, ?, ?);"
        self.cursor.execute(request, (message.id, message.timestamp, message.sender_id, message.content, message.channel_id))

        message.id = self.GetIncrementOfTable("message")

        pass

    def UpdateMessage(self, message):

        request = "UPDATE message SET message_content = (?) WHERE message_id = (?);"
        self.cursor.execute(request, (message.content, message.id))

        return message

    def IsChannelAdmin(self, channel_id, user):

        request = "SELECT * FROM channel WHERE channel_id = (?) AND channel_server_id IN (SELECT server_id FROM server WHERE server_creator_id = (?));"
        result = self.cursor.execute(request, (channel_id, user.id)).fetchall()

        if(len(result)==1):
            return True

        return False

    def IsChannelMember(self, channel_id, user):

        request = "SELECT * FROM channel WHERE channel_id = (?) AND channel_server_id IN (SELECT server_id FROM membership WHERE user_id = (?));"
        result = self.cursor.execute(request, (channel_id, user.id)).fetchall()

        if(len(result)==1):
            return True

        return False

    def GetLastMessages(self, channel_id):

        request = "SELECT * FROM message INNER JOIN user ON user.user_id = message.message_sender_id AND message.message_channel_id = (?);"
        messages = self.cursor.execute(request, (channel_id,)).fetchall()

        output = []

        for message in messages:
            print(message[1])
            output.append({ "id" : message[0], "timestamp" : str(datetime.fromtimestamp(int(message[1]))).replace(' ','@').replace('-','/') ,"user_id" : message[5], "name" : message[6], "image_token" : message[10], "content" : message[3]})

        return output


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

    def AddUserToServerFromToken(self, user_id, server_token):

        request = "SELECT * FROM server WHERE server_token=(?);"
        result = self.cursor.execute(request, (server_token,)).fetchall()

        if(len(result)!=1):
            return False

        server_id = result[0][0]

        request = "SELECT * FROM membership WHERE user_id = (?) AND server_id = (?);"
        self.cursor.execute(request, (user_id, server_id))

        result = self.cursor.fetchall()

        if(len(result)!=0):
            return False

        request = "INSERT INTO membership(user_id, server_id) VALUES (?, ?);"
        self.cursor.execute(request, (user_id, server_id))

        return True

    def AddFriendship(self, user1_id, user2_id):

        if(user1_id!=user2_id):

            request = "INSERT INTO friendship(friend1_id, friend2_id) VALUES (?, ?);"
            self.cursor.execute(request, (user1_id, user2_id))

    def RemoveFriendship(self, remover_id, removed_id):

        request = "DELETE FROM friendship WHERE friend1_id = (?) and friend2_id = (?);"
        self.cursor.execute(request, (remover_id, removed_id))
        self.cursor.execute(request, (removed_id, remover_id))

    def DoesFriendshipExists(self, friend1_id, friend2_id):

        request = "SELECT * FROM friendship WHERE friend1_id = (?) AND friend2_id = (?);"
        
        if(len(self.cursor.execute(request, (friend1_id, friend2_id)).fetchall())==1):
            return 1

        if(len(self.cursor.execute(request, (friend2_id, friend1_id)).fetchall())==1):
            return 2

        return False

    def DoesFriendshipRequestExists(self, sender_id, receiver_id):

        request = "SELECT * FROM pending_friend_request WHERE sender_id = (?) AND receiver_id = (?);"

        if(len(self.cursor.execute(request, (sender_id, receiver_id)).fetchall())==1):
            return True

        return False

    def AddFriendshipRequest(self, user_sender_id, user_receiver_id):

        if(not self.DoesFriendshipExists(user_sender_id, user_receiver_id) and not self.DoesFriendshipRequestExists(user_sender_id, user_receiver_id)):

            request = "INSERT INTO pending_friend_request(sender_id, receiver_id) VALUES (?,?);"

            self.cursor.execute(request, (user_sender_id, user_receiver_id))

    def RemoveFriendshipRequest(self, user_sender_id, user_receiver_id):

        request = "DELETE FROM pending_friend_request WHERE sender_id=(?) AND receiver_id=(?);"
        self.cursor.execute(request, (user_sender_id, user_receiver_id))
        self.cursor.execute(request, (user_receiver_id, user_sender_id))

    def GetPotentialFriend(self, searcher_id, friend_name, friend_discriminant):

        print("GET POTENTIAL FRIEND")
        print(friend_name, friend_discriminant)

        request = "SELECT * FROM user WHERE user_name LIKE (?) AND user_discriminant = (?) AND user_id NOT IN (SELECT friend1_id FROM friendship WHERE friend2_id = (?)) AND user_id NOT IN (SELECT friend2_id FROM friendship WHERE friend1_id = (?));"
        print(request)
        result = self.cursor.execute(request, ('%' + friend_name + '%', friend_discriminant, searcher_id, searcher_id)).fetchall()

        output = []

        print(result)

        for line in result:

            output.append({"id" : line[0], "name" : line[1], "image_token" : line[5]})

        return output

    def GetFriendRequestsOfUser(self, user_id):

        request = "SELECT * FROM user WHERE user_id IN (SELECT sender_id FROM pending_friend_request WHERE receiver_id=(?));"
        result = self.cursor.execute(request, (user_id,))

        output = []

        for line in result:

            output.append({"id" : line[0], "name" : line[1], "image_token" : line[5]})

        return output

    ###########
    # Fichier #
    ###########

    def DoesTokenFileExists(self, FileToken):

        request = "SELECT * FROM files WHERE file_token = (?);"

        result = self.cursor.execute(request, (FileToken,)).fetchall()

        if(len(result)==1):

            return True

        return False

    def AddTokenFile(self, FileToken, FileExtension):

        request = "INSERT INTO files(file_token, file_extension) VALUES (?, ?);"

        self.cursor.execute(request, (FileToken,FileExtension))

    def GetExtensionOfFileToken(self, FileToken):

        request = "SELECT file_extension FROM files WHERE file_token = (?);"

        result = self.cursor.execute(request, (FileToken,)).fetchall()

        return result[0][0]



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


