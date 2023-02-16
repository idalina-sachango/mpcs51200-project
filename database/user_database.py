from util.util import get_conn_curs, commit_close
import csv

# Constants
DB_FILENAME = "users.db"

###############################################################################
# CREATE
###############################################################################

# Creates the users table in the database
def create_users_table():
    conn, curs = get_conn_curs(DB_FILENAME)

    user_create = ("CREATE TABLE if not exists Users " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(250), " +
        "username VARCHAR(250), password VARCHAR(250), " +
        "user_type VARCHAR(250))")

    # Remove for data persistence, but good for testing
    curs.execute("DROP TABLE if exists Users")
    curs.execute(user_create)

    commit_close(conn, curs)

# Inserts initial set of users from file users.csv
# File has columns name, username, password, and user_type
def insert_intial_users():
    conn, curs = get_conn_curs(DB_FILENAME)

    users = []
    # https://realpython.com/python-csv/
    with open('database/users.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                user = (row[0], row[1], row[2], row[3])
                users.append(user)
                line_count += 1

    tournament_insert = ("INSERT INTO Users (name, username, password, " +
        "user_type) VALUES (?,?,?,?)")
    
    for user in users:
        curs.execute(tournament_insert, user)

    commit_close(conn, curs)

###############################################################################
# READ
###############################################################################

# Gets the current users in the database
# Return format is dictionary where key is username (string) and value is 
# another dictionary with user_id, name, username, password, and user_type.
# As an example, the return might look like:
# {
#     'tm123': {
#         'user_id': 1, 
#         'name': 'Tim Manager', 
#         'username': 'tm123', 
#         'password': 'password', 
#         'user_type': 'TournamentManager'
#     }, 
#     'originalcoach': {
#         'user_id': 2, 
#         'name': 'Coach Coach', 
#         'username': 'originalcoach', 
#         'password': 'password', 
#         'user_type': 'TeamManager'
#     }
# }
def get_all_users():
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Users")
    rows = curs.fetchall()

    users = {}

    for row in rows:
        user_id = row[0]
        users[row[2]] = get_user_by_id(user_id)

    commit_close(conn, curs)

    return users

def get_user_by_id(user_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Users WHERE id = ?", [user_id])
    rows = curs.fetchall()

    if len(rows) < 1:
        raise Exception("User does not exist")

    user_info = rows[0]

    user = {
        "user_id": user_info[0],
        "name": user_info[1],
        "username": user_info[2],
        "password": user_info[3],
        "user_type": user_info[4]
    }

    commit_close(conn, curs)

    return user

###############################################################################
# UPDATE
###############################################################################

###############################################################################
# DELETE
###############################################################################

# Deletes the user with the given ID from the database
def delete_user(user_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("DELETE FROM Users WHERE id = {}".format(user_id))

    commit_close(conn, curs)

###############################################################################
# SETUP
###############################################################################

def setup_user_database():
    create_users_table()
    insert_intial_users()
