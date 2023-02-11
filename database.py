import sqlite3
from datetime import datetime, timedelta
# Constants
db_filename = "tounament.db"

# Creates the tournaments table in the database
def create_tournaments_table():
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()

    tournament_create = ("CREATE TABLE if not exists Tournaments " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(250), " +
        "eligible_gender VARCHAR(5), eligible_age_min INT, " +
        "eligible_age_max INT, start_date DATETIME, end_date DATETIME)")

    curs.execute("DROP TABLE if exists Tournaments")
    curs.execute(tournament_create)

    conn.commit()
    curs.close()
    conn.close()

def insert_example_tournament():
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()

    name = "UChicago Tournament"
    eligible_gender = "Co-Ed"
    eligible_age_min = 18
    eligible_age_max = 24
    start_date = datetime.now()
    end_date = datetime.now() + timedelta(days=2)

    tournament_insert = ("INSERT INTO Tournaments (name, eligible_gender, " +
        "eligible_age_min, eligible_age_max, start_date, end_date) VALUES " +
        "(?,?,?,?,?,?)")
    tournament_data = (name, eligible_gender, eligible_age_min,
        eligible_age_max, start_date, end_date)

    curs.execute(tournament_insert, tournament_data)

    conn.commit()
    curs.close()
    conn.close()

def print_current_tournaments():
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()

    curs.execute("SELECT * FROM Tournaments")
    rows = curs.fetchall()
    print("Current Tournaments table:")
    for row in rows:
        print(f"Tournament {row[0]}: {row[1]}, {row[2]}, {row[3]}-{row[4]}, " +
            f"{row[5]}-{row[6]}")

    curs.close()
    conn.close()

def delete_tournament(tournament_id: int):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()

    curs.execute("DELETE FROM Tournaments WHERE id = {}".format(tournament_id))

    conn.commit()
    curs.close()
    conn.close()

if __name__ == "__main__":
    print("Creating table")
    create_tournaments_table()
    print("Table created")
    print("Inserting 2 example tournments (same metadata)")
    insert_example_tournament()
    insert_example_tournament()
    print("Example tournaments inserted")
    print_current_tournaments()
    print("Deleting first tournament")
    delete_tournament(1)
    print("First tournament deleted")
    print_current_tournaments()