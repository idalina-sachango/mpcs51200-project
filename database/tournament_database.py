from datetime import datetime, timedelta
from util.util import get_conn_curs, commit_close

# Constants
DB_FILENAME = "tournaments.db"

# Creates the tournaments-related tables in the database.
# *** Basic Tables ***
# Tournaments table:
# id: int, automatically increments on insert
# name: string, common name of tournament
# eligible_gender: string, ('m', 'f', or 'co-ed')
# eligible_age_min: int, minimum eligible age for tournament
# eligible_age_max: int, maximum eligible age for tournament
# start_date: datetime, starting date and time of the tournament
# end_date: datetime, ending date and time of the tournament
#
# Teams table:
# id: int, automatically increments on insert
# name: string, common name of team
# team_gender: string, ('m', 'f', or 'co-ed')
# team_age_min: int, minimum age of player on team
# team_age_max: int, maximum age of player on team
#
# Players table:
# id: int, automatically increments on insert
# name: string, player's name
# gender: string, ('m', 'f', or 'other')
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

    # Remove these lines for data persistence, but they are good for testing
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

# Creates a tournament
def insert_tournament(name: str, eligible_gender: str, eligible_age_min: int, 
        eligible_age_max: int, start_date: datetime, end_date: datetime):
    conn, curs = get_conn_curs(DB_FILENAME)

    # Ensures that each input is of the correct type, throws an AssertionError
    # with the provided message if not
    assert(isinstance(name, str)), "name must be a string"
    assert(isinstance(eligible_gender, str)), ("eligible_gender must be a " +
        "string")
    assert(isinstance(eligible_age_min, int)), ("eligible_age_min must be an " +
        "int")
    assert(isinstance(eligible_age_max, int)), ("eligible_age_max must be an " +
        "int")
    assert(isinstance(start_date, datetime)), "start_date must be a datetime"
    assert(isinstance(end_date, datetime)), "end_date must be a datetime"

    tournament_insert = ("INSERT INTO Tournaments (name, eligible_gender, " +
        "eligible_age_min, eligible_age_max, start_date, end_date) VALUES " +
        "(?,?,?,?,?,?)")
    tournament_data = (name, eligible_gender, eligible_age_min,
        eligible_age_max, start_date, end_date)

    curs.execute(tournament_insert, tournament_data)

    commit_close(conn, curs)

# Creates a team
def insert_team(name: str, team_gender: str, team_age_min: int,
        team_age_max: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    # Ensures that each input is of the correct type, throws an AssertionError
    # with the provided message if not
    assert(isinstance(name, str)), "name must be a string"
    assert(isinstance(team_gender, str)), "team_gender must be a string"
    assert(isinstance(team_age_min, int)), "team_age_min must be an int"
    assert(isinstance(team_age_max, int)), "team_age_max must be an int"

    team_insert = ("INSERT INTO Teams (name, team_gender, " +
        "team_age_min, team_age_max) VALUES (?,?,?,?)")
    team_data = (name, team_gender, team_age_min, team_age_max)

    curs.execute(team_insert, team_data)

    commit_close(conn, curs)

# Creates a game
def insert_game(time: datetime, home_team: int = None, 
        away_team: int = None):
    conn, curs = get_conn_curs(DB_FILENAME)

    # Ensures that each input is of the correct type, throws an AssertionError
    # with the provided message if not
    assert(isinstance(time, datetime)), "time must be a datetime"
    assert(isinstance(home_team, int) or home_team is None), ("home_team " +
        "must be an int or None")
    assert(isinstance(away_team, int) or away_team is None), ("away_team " +
        "must be an int or None")

    game_insert = ("INSERT INTO GAMES (home_team, away_team, time) VALUES " +
        "(?,?,?)")
    game_data = (home_team, away_team, time)

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

def setup_tournament_database():
    create_basic_tables()
    create_relational_tables()

if __name__ == "__main__":
    print("Creating tables")
    create_basic_tables()
    create_relational_tables()
    print("Table created")
    print("Inserting 2 example tournments")
    insert_tournament("UChicago Tournament", "co-ed", 18, 24, datetime.now(),
        datetime.now() + timedelta(days=2))
    insert_tournament("U12 Tournament", "f", 10, 12, datetime.now(),
        datetime.now() + timedelta(days=2))
    print("Example tournaments inserted")
    insert_team("UChicago", "co-ed", 18, 24)
    insert_team("Local School", "f", 10, 12)
    print("Example teams inserted")
    insert_game(datetime.now() + timedelta(days=1), None, 2)
    print("Example game inserted")
    # print_current_tournaments()
    # print("Deleting first tournament")
    # delete_tournament(1)
    # print("First tournament deleted")
    # print_current_tournaments()