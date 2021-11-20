from dispute_sql import *

O = DatabaseHandler("database.db")
#O.ResetEntireDatabase()
O.GetEntireTable("user")

U = User()
U.name = "test"
U.hash = sha256("test")
U.email = "test@test"

O.CreateUser(U)

O.GetEntireTable("user")

print(NewToken())