from dispute_sql import *

O = DatabaseHandler("database.db")
O.GetEntireTable("user")
O.ResetEntireDatabase()
O.GetEntireTable("user")
print("GNEUGNEU")

U = User()
U.name = "test"
U.hash = sha256("test")
U.email = "test@test"

O.CreateUser(U)

U = User()
U.name = "jean"
U.hash = sha256("jean")
U.email = "jean@jean"

O.CreateUser(U)

U = User()
U.name = "lea"
U.hash = sha256("lea")
U.email = "lea@lea"

O.CreateUser(U)

O.GetEntireTable("user")

print(NewToken())