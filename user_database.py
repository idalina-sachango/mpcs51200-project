from util import get_conn_curs, commit_close

# Constants
DB_FILENAME = "users.db"

# Creates the users table in the database
def create_users_table():
    conn, curs = get_conn_curs(DB_FILENAME)

    user_create = ("CREATE TABLE if not exists Users " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(250), " +
        "username VARCHAR(250), password VARCHAR(250), " +
        "user_type VARCHAR(250))")

    curs.execute("DROP TABLE if exists Users")
    curs.execute(user_create)

    commit_close(conn, curs)

def insert_intial_users():
    conn, curs = get_conn_curs(DB_FILENAME)

    users = [("Tim Manager", "tm123", "password", "Tournament Manager"),
             ("Coach Coach", "originalcoach", "password", "Team Manager")]

    tournament_insert = ("INSERT INTO Users (name, username, password, " +
        "user_type) VALUES (?,?,?,?)")
    
    for user in users:
        curs.execute(tournament_insert, user)

    commit_close(conn, curs)

def print_current_users():
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Users")
    rows = curs.fetchall()
    print("Current Users table:")
    for row in rows:
        print(f"{row[2]}: {row[1]}, {row[3]}, {row[4]}")

    commit_close(conn, curs)

def delete_user(user_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("DELETE FROM Users WHERE id = {}".format(user_id))

    commit_close(conn, curs)

if __name__ == "__main__":
    print("Creating table")
    create_users_table()
    print("Table created")
    print("Inserting 2 initial users")
    insert_intial_users()
    print("Initial users inserted")
    print_current_users()
    print("Deleting first user")
    delete_user(1)
    print("First user deleted")
    print_current_users()