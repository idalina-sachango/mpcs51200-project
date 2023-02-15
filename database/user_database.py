from util.util import get_conn_curs, commit_close
import csv

# Constants
DB_FILENAME = "users.db"

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

# Gets the current users in the database
# Return format is dictionary where key is username (string) and value is 
# another dictionary with name, password, and user_type as strings
# As an example, the return might look like:
# {
#     'tm123': {
#         'name': 'Tim Manager',
#         'password': 'password',
#         'user_type': 'TournamentManager'
#     },
#     'originalcoach': {
#         'name': 'CoachCoach', 
#         'password': 'password', 
#         'user_type': 'TeamManager'
#     },
# }
def get_current_users():
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Users")
    rows = curs.fetchall()

    users = {}

    for row in rows:
        entry_information = {"name": row[1], "password": row[3], "user_type": row[4]}
        users[row[2]] = entry_information

    commit_close(conn, curs)

    return users

# Deletes the user with the given ID from the database
def delete_user(user_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("DELETE FROM Users WHERE id = {}".format(user_id))

    commit_close(conn, curs)

def setup_user_database():
    create_users_table()
    insert_intial_users()


if __name__ == "__main__":
    print("Creating table")
    create_users_table()
    print("Table created")
    print("Inserting 2 initial users")
    insert_intial_users()
    print("Initial users inserted")
    print(get_current_users())
    # print("Deleting first user")
    # delete_user(1)
    # print("First user deleted")
    # print_current_users()