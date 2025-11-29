import os
import database
import database_users

print("orders.db path:", os.path.abspath(database.DB_NAME))
print("users.db path:", os.path.abspath(database_users.DB_NAME))
