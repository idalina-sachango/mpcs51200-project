from database.tournament_database import get_all_teams, get_all_tournaments
from backend.users import print_user

LINE_DELIMITER = "*" * 40

def print_tournaments():
    tournaments = get_all_tournaments()
    if not tournaments:
        print("\nNo tournaments currently.")

    for tournament in tournaments.values():
        print(LINE_DELIMITER)
        print(f"Tournament Name: {tournament['name']}\n")
        print(f"Eligible Gender: {tournament['eligible_gender']}\n")
        print(f"Eligible Age Range: {tournament['eligible_age_min']}-" +
            f"{tournament['eligible_age_max']}\n")
        print(f"Date Range: ({str(tournament['start_date'])})-" +
            f"({tournament['end_date']})\n")
        print("Registered Teams")
        print("-" * 20)
        for team in tournament['registered_teams']:
            print(f"Team Name: {team['name']}")
        print(LINE_DELIMITER)

def print_teams():
    teams = get_all_teams()
    if not teams:
        print("\nNo teams currently.")

    for team in teams.values():
        print(LINE_DELIMITER)
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
            f"{player['age']} years old")