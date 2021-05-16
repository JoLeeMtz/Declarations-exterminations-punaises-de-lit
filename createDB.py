import sqlite3

DATA_BASE_NAME_DECLARATIONS = "database/declarations_punaises_lit.db"
# DATA_BASE_NAME_DECLARATIONS = "database/declarations_punaises_lit_vide.db"
SQL_FILE_DECLARATIONS = "database/declarations_punaises_lit.sql"
DATA_BASE_NAME_USERS = "database/users.db"
SQL_FILE_USERS = "database/users.sql"

# Create Database for declarations_punaises_lit
connection = sqlite3.connect(DATA_BASE_NAME_DECLARATIONS)
cursor = connection.cursor()

sql_file = open(SQL_FILE_DECLARATIONS)
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)

connection.close()
# ----------------------------------------------------------------------------


# Create Database for users
connection = sqlite3.connect(DATA_BASE_NAME_USERS)
cursor = connection.cursor()

sql_file = open(SQL_FILE_USERS)
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)

connection.close()
# ----------------------------------------------------------------------------
