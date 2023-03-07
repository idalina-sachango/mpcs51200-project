from database.tournament_database import (
    get_all_teams, 
    get_all_tournaments, 
    get_team_age_range, 
    get_tournament_by_id, 
    get_team_by_id, 
    get_team_gender_range,
    get_tournaments_by_manager,
    get_games_by_tournament,
    get_score_by_game)
from backend.users import print_user

LONG_LINE_DELIMITER = "*" * 40
MEDIUM_LINE_DELIMITER = "=" * 30
SHORT_LINE_DELIMITER = "-" * 20

def print_tournaments(tournaments: dict):
    print("*** VIEWING TOURNAMENTS ***")
    for tournament in tournaments.values():
        print(LONG_LINE_DELIMITER)
        print(f"Tournament ID: {tournament['tournament_id']}")
        print(f"Tournament Name: {tournament['name']}")
        print(f"Eligible Gender: {tournament['eligible_gender']}")
        print(f"Eligible Age Range: {tournament['eligible_age_min']}-" +
            f"{tournament['eligible_age_max']}")
        print(f"Date Range: ({str(tournament['start_date'])})-" +
            f"({tournament['end_date']})")
        print(f"Location: {tournament['location']}")
        if (tournament['is_reg_open']):
            print(f"Registration: Open")
        else:
            print(f"Registration: Closed")
        print("Registered Teams:")
        print(SHORT_LINE_DELIMITER)
        for team in tournament['registered_teams']:
            print(f"Team Name: {team['name']}")
        print(LONG_LINE_DELIMITER)

def print_games(games: dict):
    print("*** VIEWING GAMES ***")
    for game in games.values():
        print(LONG_LINE_DELIMITER)
        print(f"Game ID: {game['game_id']}")
        print(f"Home Team")
        home_team_id = game['home_team']
        print(MEDIUM_LINE_DELIMITER)
        if home_team_id:
            print_team(get_team_by_id(home_team_id))       
        else:
            print("No home team yet.")
        print(MEDIUM_LINE_DELIMITER)
        print(f"Away Team")
        away_team_id = game['away_team']
        print(MEDIUM_LINE_DELIMITER)
        if away_team_id:
            print_team(get_team_by_id(away_team_id))
        else:
            print("No away team yet.")
        print(MEDIUM_LINE_DELIMITER)
        print(f"Time: {game['time']}")
        print(f"Location: {game['location']}")

        score = get_score_by_game(game['game_id'])
        if score:
            print(f"Hometeam score: {score['homescore']}")
            print(f"Awayteam score: {score['awayscore']}")

        print(LONG_LINE_DELIMITER)
        
def print_teams(teams: dict):
    print("*** VIEWING TEAMS ***")
    for team in teams.values():
        print(LONG_LINE_DELIMITER)
        print_team(team)
        print(LONG_LINE_DELIMITER)

def print_team(team: dict):
    print(f"Team ID: {team['team_id']}")
    print(f"Team Name: {team['name']}")
    print(f"Team Gender: {team['team_gender']}")
    print(f"Team Age Range: {team['team_age_min']}-" +
        f"{team['team_age_max']}")
    print("Team Manager: ")
    print_user(team["team_manager"])
    print("Roster")
    print(SHORT_LINE_DELIMITER)
    print_roster(team["roster"])

def print_all_teams():
    teams = get_all_teams()
    if not teams:
        print("\nNo teams currently.")

    print_teams(teams)

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