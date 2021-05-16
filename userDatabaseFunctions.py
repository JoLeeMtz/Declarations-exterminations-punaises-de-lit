import sqlite3
from declaration import Declaration

DB_USERS = "database/users.db"


class UserDB:
    def __init__(self):
        self.connection = None

# Connection to users database -----------------------------------------------
    def get_connection_users(self):
        if self.connection is None:
            self.connection = sqlite3.connect(DB_USERS)
        return self.connection

# Disconnect from database ---------------------------------------------------
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

# SELECT by email/pwd --------------------------------------------------------
    def select_user(self, email, pwd):
        cursor = self.get_connection_users().cursor()
        sql_select = "SELECT * FROM users WHERE email=? AND pwd=?;"
        parameters = (str(email), str(pwd))
        cursor.execute(sql_select, parameters)
        users = cursor.fetchall()
        self.disconnect()
        return users
# ----------------------------------------------------------------------------

# SELECT email ---------------------------------------------------------------
    def select_user_email(self, email):
        cursor = self.get_connection_users().cursor()
        sql_select = "SELECT * FROM users WHERE email=?;"
        cursor.execute(sql_select, (email,))
        users = cursor.fetchall()
        self.disconnect()
        return users
# ----------------------------------------------------------------------------

# INSERT user ----------------------------------------------------------------
    def insert_user(self, user):
        cursor = self.get_connection_users().cursor()
        sql_insert = "INSERT INTO users (name, email, list_nom_qr, pwd) " \
                     "VALUES (?,?,?,?);"
        parameters = (str(user.name), str(user.email),
                      str(user.list_nom_qr), str(user.pwd))
        cursor.execute(sql_insert, parameters)
        self.connection.commit()

        # Set id in user class
        cursor = self.get_connection_users().cursor()
        cursor.execute("SELECT last_insert_rowid()")
        result = cursor.fetchall()
        user.email = result[0][0]
        self.disconnect()
        return user
# ----------------------------------------------------------------------------

# UPDATE user ----------------------------------------------------------------
    def update_user(self, email, list_nom_qr, profile_picture):
        cursor = self.get_connection_users().cursor()
        sql_insert = "UPDATE users SET list_nom_qr=?, profile_picture=? "\
                     "WHERE email=?;"
        parameters = (str(list_nom_qr), profile_picture, str(email))
        cursor.execute(sql_insert, parameters)
        self.connection.commit()

        # Set id in user class
        cursor = self.get_connection_users().cursor()
        cursor.execute("SELECT last_insert_rowid()")
        result = cursor.fetchall()
        user_email = result[0][0]
        self.disconnect()
        return user_email
# ----------------------------------------------------------------------------

# UPDATE user ----------------------------------------------------------------
    def update_user_list(self, email, list_nom_qr):
        cursor = self.get_connection_users().cursor()
        sql_insert = "UPDATE users SET list_nom_qr=? "\
                     "WHERE email=?;"
        parameters = (str(list_nom_qr), str(email))
        cursor.execute(sql_insert, parameters)
        self.connection.commit()

        # Set id in user class
        cursor = self.get_connection_users().cursor()
        cursor.execute("SELECT last_insert_rowid()")
        result = cursor.fetchall()
        user_email = result[0][0]
        self.disconnect()
        return user_email
# ----------------------------------------------------------------------------
