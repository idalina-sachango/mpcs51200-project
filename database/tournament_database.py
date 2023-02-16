from datetime import datetime, timedelta
from util.util import get_conn_curs, commit_close
from database.user_database import get_user_by_id

# Constants
DB_FILENAME = "tournaments.db"

###############################################################################
# CREATE
###############################################################################

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
# team_manager: int, ID of user who created team
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
        "team_gender VARCHAR(5), team_age_min INT, team_age_max INT, " +
        "team_manager INT)")

    players_create = ("CREATE TABLE if not exists Players " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(250), " +
        "gender VARCHAR(5), age INT)")

    games_create = ("CREATE TABLE if not exists Games " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, home_team INT, " +
        "away_team INT, time DATETIME, " +
        "FOREIGN KEY(home_team) REFERENCES Teams(id), " +
        "FOREIGN KEY(away_team) REFERENCES Teams(id))")

    # Remove these lines for data persistence, but they are good for testing
    # curs.execute("DROP TABLE if exists TournamentRegistrations")
    # curs.execute("DROP TABLE if exists PlayersOnTeams")
    # curs.execute("DROP TABLE if exists GamesInTournaments")
    # curs.execute("DROP TABLE if exists Players")
    # curs.execute("DROP TABLE if exists Games")
    # curs.execute("DROP TABLE if exists Teams")
    # curs.execute("DROP TABLE if exists Tournaments")

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
def create_tournament(name: str, eligible_gender: str, eligible_age_min: int, 
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
    assert(start_date < end_date, "start_date must be before end_date")

    tournament_insert = ("INSERT INTO Tournaments (name, eligible_gender, " +
    "eligible_age_min, eligible_age_max, start_date, end_date) VALUES " +
    "(?,?,?,?,?,?)")
    tournament_data = (name, eligible_gender, eligible_age_min,
        eligible_age_max, start_date, end_date)

    curs.execute(tournament_insert, tournament_data)
    
    commit_close(conn, curs)

# Creates a game in Games table and connects it to an existing tournament in
# GamesInTournaments table
# Potentially raises sqlite errors, they must be caught by calling function
def create_game(time: datetime, tournament_id: int, home_team: int = None, 
        away_team: int = None):
    conn, curs = get_conn_curs(DB_FILENAME)

    # Ensures that each input is of the correct type, throws an AssertionError
    # with the provided message if not
    assert(isinstance(time, datetime)), "time must be a datetime"
    assert(isinstance(tournament_id, int)), "tournament_id must be an int"
    assert(isinstance(home_team, int) or home_team is None), ("home_team " +
        "must be an int or None")
    assert(isinstance(away_team, int) or away_team is None), ("away_team " +
        "must be an int or None")

    game_insert = ("INSERT INTO Games (home_team, away_team, time) VALUES " +
        "(?,?,?)")
    game_data = (home_team, away_team, time)

    curs.execute(game_insert, game_data)
    game_id = curs.lastrowid

    game_tournament_insert = ("INSERT INTO GamesInTournaments " +
        "(tournament_id, game_id) VALUES (?,?)")
    game_tournament_data = (tournament_id, game_id)

    curs.execute(game_tournament_insert, game_tournament_data)

    commit_close(conn, curs)

# Creates a team in Teams table
def create_team(name: str, team_gender: str, team_age_min: int,
        team_age_max: int, team_manager: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    # Ensures that each input is of the correct type, throws an AssertionError
    # with the provided message if not
    assert(isinstance(name, str)), "name must be a string"
    assert(isinstance(team_gender, str)), "team_gender must be a string"
    assert(isinstance(team_age_min, int)), "team_age_min must be an int"
    assert(isinstance(team_age_max, int)), "team_age_max must be an int"
    assert(isinstance(team_manager, int)), "team_manager must be an int"

    team_insert = ("INSERT INTO Teams (name, team_gender, " +
        "team_age_min, team_age_max, team_manager) VALUES (?,?,?,?,?)")
    team_data = (name, team_gender, team_age_min, team_age_max, team_manager)

    curs.execute(team_insert, team_data)

    commit_close(conn, curs)

# Creates a player in Players table and connects it to an existing team in
# PlayersOnTeams table
# Potentially raises sqlite errors, they must be caught by calling function
def create_player(name: str, gender: str, age: int, team_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    # Ensures that each input is of the correct type, throws an AssertionError
    # with the provided message if not
    assert(isinstance(name, str)), "name must be a string"
    assert(isinstance(gender, str)), "gender must be a string"
    assert(isinstance(age, int)), "age must be an int"
    assert(isinstance(team_id, int)), "team_id must be an int"

    player_insert = "INSERT INTO Players (name, gender, age) VALUES (?,?,?)"
    player_data = (name, gender, age)

    curs.execute(player_insert, player_data)
    player_id = curs.lastrowid

    player_team_insert = ("INSERT INTO PlayersOnTeams (team_id, player_id) " +
        "VALUES (?,?)")
    player_team_data = (team_id, player_id)

    curs.execute(player_team_insert, player_team_data)

    commit_close(conn, curs)

# Registers an existing team in an existing tournament by inserting into
# TournamentRegistrations table
# Potentially raises sqlite errors, they must be caught by calling function
def register_team_in_tournament(tournament_id: int, team_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    # Ensures that each input is of the correct type, throws an AssertionError
    # with the provided message if not
    assert(isinstance(tournament_id, int)), "tournament_id must be an int"
    assert(isinstance(team_id, int)), "team_id must be an int"

    tournament_team_insert = ("INSERT INTO TournamentRegistrations " +
        "(tournament_id, team_id) VALUES (?,?)")
    tournament_team_data = (tournament_id, team_id)

    curs.execute(tournament_team_insert, tournament_team_data)

    commit_close(conn, curs)

###############################################################################
# READ
###############################################################################

# Gets all tournaments in the Tournaments table
# Return format is a dictionary where key is the ID of the tournament
# and value is another dictionary with tournament_id, name, eligible_gender, 
# eligible_age_min, eligible_age_max, start_date, end_date, and 
# registered_teams (which is a list of dictionaries of each team's information)
def get_all_tournaments():
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Tournaments")
    rows = curs.fetchall()
    
    tournaments = {}
    for row in rows:
        tournament_id = row[0]
        tournaments[tournament_id] = get_tournament_by_id(tournament_id)

    commit_close(conn, curs)

    return tournaments

# Gets all teams in the Teams table
# Return format is a dictionary where key is the ID of the team
# and value is another dictionary with team_id, name, team_gender, 
# team_age_min, team_age_max, team manager (which is a dictionary of that
# user's information), and roster (which is a list of dictionaries of each
# player's information)
def get_all_teams():
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Teams")
    rows = curs.fetchall()
    
    teams = {}
    for row in rows:
        team_id = row[0]
        teams[team_id] = get_team_by_id(team_id)

    commit_close(conn, curs)

    return teams

def get_tournament_by_id(tournament_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Tournaments WHERE id = ?", [tournament_id])
    rows = curs.fetchall()

    if len(rows) < 1:
        raise Exception("Tournament does not exist")

    select_registrations = ("SELECT * FROM TournamentRegistrations " +
        "WHERE tournament_id = ?")
    select_data = [tournament_id]

    curs.execute(select_registrations, select_data)
    registrations = curs.fetchall()

    teams = []
    for registration in registrations:
        team_id = registration[1]
        teams.append(get_team_by_id(team_id))

    tournament_info = rows[0]

    tournament = {
        "tournament_id": tournament_info[0],
        "name": tournament_info[1],
        "eligible_gender": tournament_info[2],
        "eligible_age_min": tournament_info[3],
        "eligible_age_max": tournament_info[4],
        "start_date": tournament_info[5],
        "end_date": tournament_info[6],
        "registered_teams": teams
    }

    commit_close(conn, curs)

    return tournament

def get_team_by_id(team_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Teams WHERE id = ?", [team_id])
    rows = curs.fetchall()

    if len(rows) < 1:
        raise Exception("Team does not exist")

    select_roster = "SELECT * FROM PlayersOnTeams WHERE team_id = ?"
    select_data = [team_id]

    curs.execute(select_roster, select_data)
    roster = curs.fetchall()

    players = []
    for roster_item in roster:
        player_id = roster_item[0]
        players.append(get_player_by_id(player_id))

    team_info = rows[0]

    team = {
        "team_id": team_info[0],
        "name": team_info[1],
        "team_gender": team_info[2],
        "team_age_min": team_info[3],
        "team_age_max": team_info[4],
        "team_manager": get_user_by_id(team_info[5]),
        "roster": players
    }

    commit_close(conn, curs)

    return team

def get_player_by_id(player_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Players WHERE id = ?", [player_id])
    rows = curs.fetchall()

    if len(rows) < 1:
        raise Exception("Player does not exist")

    player_info = rows[0]

    player = {
        "player_id": player_info[0],
        "name": player_info[1],
        "gender": player_info[2],
        "age": player_info[3]
    }

    commit_close(conn, curs)
    
    return player

###############################################################################
# UPDATE
###############################################################################

###############################################################################
# DELETE
###############################################################################

# Deletes the tournament with the given id
def delete_tournament(tournament_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("DELETE FROM Tournaments WHERE id = {}".format(tournament_id))

    commit_close(conn, curs)

###############################################################################
# SETUP
###############################################################################

def setup_tournament_database():
    create_basic_tables()
    create_relational_tables()

if __name__ == "__main__":
    print("Creating tables")
    create_basic_tables()
    create_relational_tables()
    print("Table created")
    print("Inserting 2 example tournments")
    create_tournament("UChicago Tournament", "co-ed", 18, 24, datetime.now(),
        datetime.now() + timedelta(days=2))
    create_tournament("U12 Tournament", "f", 10, 12, datetime.now(),
        datetime.now() + timedelta(days=2))
    print("Example tournaments inserted")
    create_team("UChicago", "co-ed", 18, 24, 1)
    create_team("Local School", "f", 10, 12, 1)
    print("Example teams inserted")
    create_game(datetime.now() + timedelta(days=1), None, 2)
    print("Example game inserted")
    # print_current_tournaments()
    # print("Deleting first tournament")
    # delete_tournament(1)
    # print("First tournament deleted")
    # print_current_tournaments()