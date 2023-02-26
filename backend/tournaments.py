from database.tournament_database import (
    get_all_teams, 
    get_all_tournaments, 
    get_team_age_range, 
    get_tournament_by_id, 
    get_team_by_id, 
    get_team_gender_range,
    get_tournaments_by_manager,
    get_games_by_tournament)
from backend.users import print_user

LINE_DELIMITER = "*" * 40

def print_tournaments(tournaments: dict):
    for tournament in tournaments.values():
        print(LINE_DELIMITER)
        print(f"Tournament ID: {tournament['tournament_id']}\n")
        print(f"Tournament Name: {tournament['name']}\n")
        print(f"Eligible Gender: {tournament['eligible_gender']}\n")
        print(f"Eligible Age Range: {tournament['eligible_age_min']}-" +
            f"{tournament['eligible_age_max']}\n")
        print(f"Date Range: ({str(tournament['start_date'])})-" +
            f"({tournament['end_date']})\n")
        if (tournament['is_reg_open']):
            print(f"Registration Open\n")
        else:
            print(f"Registration Closed\n")
        print("Registered Teams")
        print("-" * 20)
        for team in tournament['registered_teams']:
            print(f"Team Name: {team['name']}")
        print(LINE_DELIMITER)

def print_games(games: dict):
    for game in games.values():
        print(LINE_DELIMITER)
        print(f"Game ID: {game['game_id']}\n")
        print(f"Home Team ID: {game['home_team']}\n")
        print(f"Away Team ID: {game['away_team']}\n")
        print(f"Time: {game['time']}\n")
        print(f"Location: {game['location']}")
        print(LINE_DELIMITER)

def print_all_tournaments():
    tournaments = get_all_tournaments()
    if not tournaments:
        print("\nNo tournaments currently.")

    print_tournaments(tournaments)

def print_manager_tournaments(manager_id: int):
    tournaments = get_tournaments_by_manager(manager_id)
    if not tournaments:
        print("\nNo tournaments currently.")

    print_tournaments(tournaments)

def print_tournament_games(tournament_id: int):
    games = get_games_by_tournament(tournament_id)
    if not games:
        print("\nNo games currently.")

    print_games(games)

def print_teams():
    teams = get_all_teams()
    if not teams:
        print("\nNo teams currently.")

    for team in teams.values():
        print(LINE_DELIMITER)
        print(f"Team ID: {team['team_id']}\n")
        print(f"Team Name: {team['name']}\n")
        print(f"Team Gender: {team['team_gender']}\n")
        print(f"Team Age Range: {team['team_age_min']}-" +
            f"{team['team_age_max']}\n")
        print("Team Manager: ")
        print_user(team["team_manager"])
        print("")
        print("Roster")
        print("-" * 20)
        print_roster(team["roster"])
        print(LINE_DELIMITER)

# Roster is a list of dicts which are players
def print_roster(roster: list):
    roster_num = 0
    for player in roster:
        roster_num += 1
        print(f"{roster_num}. {player['name']}, {player['gender']}, " +
            f"{player['age']} years old. ID: {player['player_id']}")

def check_team_eligibility(team_id: int, tournament_id: int):
    # Check empty teams
    if not get_team_by_id(team_id)["roster"]:
        return False

    # Check if all players fit age requirement
    eligible_age_min = get_tournament_by_id(tournament_id)["eligible_age_min"]
    eligible_age_max = get_tournament_by_id(tournament_id)["eligible_age_max"]
    team_min_age, team_max_age = get_team_age_range(team_id)

    if team_min_age < eligible_age_min or team_max_age > eligible_age_max:
        return False

    # Check if all players fir gender requirement
    eligible_gender = get_tournament_by_id(tournament_id)["eligible_gender"]
    team_gender = get_team_gender_range(team_id)

    if eligible_gender == team_gender or eligible_gender == "co-ed":
        return True
    else:
        return False
 