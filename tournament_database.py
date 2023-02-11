from datetime import datetime, timedelta
from util import get_conn_curs, commit_close

# Constants
DB_FILENAME = "tounaments.db"

# Creates the tournaments-related tables in the database.
# *** Basic Tables ***
# Tournaments table:
# id: int, automatically increments on insert
# name: string, common name of tournament
# eligible_gender: string, ('M', 'F', or 'Co-ed')
# eligible_age_min: int, minimum eligible age for tournament
# eligible_age_max: int, maximum eligible age for tournament
# start_date: datetime, starting date and time of the tournament
# end_date: datetime, ending date and time of the tournament
#
# Teams table:
# id: int, automatically increments on insert
# name: string, common name of team
# team_gender: string, ('M', 'F', or 'Co-ed')
# team_age_min: int, minimum age of player on team
# team_age_max: int, maximum age of player on team
#
# Players table:
# id: int, automatically increments on insert
# name: string, player's name
# gender: string, ('M', 'F', or 'Other')
# age: int, player's age
#
# Games table:
# id: int, automatically increments on insert
# home_team: int, foreign key (Teams)
# away_team: int, foreign key (Teams)
# time: datetime, time that the game takes place
def create_basic_tables():
    conn, curs = get_conn_curs(DB_FILENAME)

    tournaments_create = ("CREATE TABLE if not exists Tournaments " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(250), " +
        "eligible_gender VARCHAR(5), eligible_age_min INT, " +
        "eligible_age_max INT, start_date DATETIME, end_date DATETIME)")
    
    teams_create = ("CREATE TABLE if not exists Teams " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(250), " +
        "team_gender VARCHAR(5), team_age_min INT, team_age_max INT)")

    players_create = ("CREATE TABLE if not exists Players " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(250), " +
        "gender VARCHAR(5), age INT)")

    games_create = ("CREATE TABLE if not exists Games " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, home_team INT, " +
        "away_team INT, time DATETIME, " +
        "FOREIGN KEY(home_team) REFERENCES Teams(id), " +
        "FOREIGN KEY(away_team) REFERENCES Teams(id))")

    # Remove these lines for persistence, but they are good for testing
    curs.execute("DROP TABLE if exists Tournaments")
    curs.execute("DROP TABLE if exists Games")
    curs.execute("DROP TABLE if exists Teams")
    curs.execute("DROP TABLE if exists Players")

    # Execute the statements
    statements = [tournaments_create, teams_create, players_create, 
        games_create]
    for statement in statements:
        curs.execute(statement)

    commit_close(conn, curs)

# *** Relational Tables ***
# TournamentRegistrations table:
# tournament_id: int, foreign key
# team_id: int, foreign key
#
# PlayersOnTeams table:
# team_id: int, foreign key
# player_id: int, foreign key
#
# GamesInTournaments table:
# tournament_id: int, foreign key
# game_id: int, foreign key
def create_relational_tables():
    conn, curs = get_conn_curs(DB_FILENAME)

    tournament_registrations_create = ("CREATE TABLE if not exists " +
        "TournamentRegistrations (tournament_id INT, team_id INT, " +
        "FOREIGN KEY(tournament_id) REFERENCES Tournaments(id), " +
        "FOREIGN KEY(team_id) REFERENCES Teams(id))")

    players_on_teams_create = ("CREATE TABLE if not exists PlayersOnTeams " +
        "(team_id INT, player_id INT, " +
        "FOREIGN KEY(team_id) REFERENCES Teams(id), " +
        "FOREIGN KEY(player_id) REFERENCES Players(id))")

    games_in_tournaments_create = ("CREATE TABLE if not exists " +
        "GamesInTournaments (tournament_id INT, game_id INT, " +
        "FOREIGN KEY(tournament_id) REFERENCES Tournaments(id), " +
        "FOREIGN KEY(game_id) REFERENCES Games(id))")

    # Execute the statements
    statements = [tournament_registrations_create, players_on_teams_create,
        games_in_tournaments_create]
    for statement in statements:
        curs.execute(statement)

    commit_close(conn, curs)

# Creates a fake tournament for testing
def insert_example_tournament():
    conn, curs = get_conn_curs(DB_FILENAME)

    name = "UChicago Tournament"
    eligible_gender = "Co-ed"
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

    commit_close(conn, curs)

# Creates a fake team for testing
def insert_example_team():
    conn, curs = get_conn_curs(DB_FILENAME)

    name = "UChicago Team"
    team_gender = "Co-Ed"
    team_age_min = 18
    team_age_max = 24

    team_insert = ("INSERT INTO Teams (name, team_gender, " +
        "team_age_min, team_age_max) VALUES (?,?,?,?)")
    team_data = (name, team_gender, team_age_min, team_age_max)

    curs.execute(team_insert, team_data)

    commit_close(conn, curs)

# Creates a fake game for testing
def insert_example_game():
    conn, curs = get_conn_curs(DB_FILENAME)

    game_insert = ("INSERT INTO GAMES (home_team, away_team, time) VALUES " +
        "(?,?,?)")
    game_data = (1, 2, datetime.now())

    curs.execute(game_insert, game_data)

    commit_close(conn, curs)

# Prints the current tournaments in the table
def print_current_tournaments():
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Tournaments")
    rows = curs.fetchall()
    print("Current Tournaments table:")
    for row in rows:
        print(f"Tournament {row[0]}: {row[1]}, {row[2]}, {row[3]}-{row[4]}, " +
            f"{row[5]}-{row[6]}")

    commit_close(conn, curs)

# Deletes the tournament with the given id
def delete_tournament(tournament_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("DELETE FROM Tournaments WHERE id = {}".format(tournament_id))

    commit_close(conn, curs)


if __name__ == "__main__":
    print("Creating tables")
    create_basic_tables()
    create_relational_tables()
    print("Table created")
    print("Inserting 2 example tournments (same metadata)")
    insert_example_tournament()
    insert_example_tournament()
    print("Example tournaments inserted")
    insert_example_team()
    insert_example_team()
    print("Example team inserted")
    insert_example_game()
    print("Example game inserted")
    # print_current_tournaments()
    # print("Deleting first tournament")
    # delete_tournament(1)
    # print("First tournament deleted")
    # print_current_tournaments()