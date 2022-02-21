from dispute_sql import *

O = DatabaseHandler("database.db")
O.GetEntireTable("user")
O.ResetEntireDatabase()

O.ResetDatabaseConnection()

O = DatabaseHandler("database.db")

O.GetEntireTable("user")
print("GNEUGNEU")

U1 = User()
U1.name = "test"
U1.hash = sha256("test")
U1.email = "test@test"

U1 = O.CreateUser(U1)

U2 = User()
U2.name = "jean"
U2.hash = sha256("jean")
U2.email = "jean@jean"

U2 = O.CreateUser(U2)

U3 = User()
U3.name = "lea"
U3.hash = sha256("lea")
U3.email = "lea@lea"

U3 = O.CreateUser(U3)

print(U1.id)
print(U2.id)

#O.AddFriendShip(U1.id, U2.id)
#O.AddFriendShip(U1.id, U3.id)

O.GetEntireTable("user")

print(NewToken())