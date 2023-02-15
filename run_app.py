from database.user_database import setup_user_database, get_all_users
from database.tournament_database import setup_tournament_database, create_tournament, register_team_in_tournament, create_team, create_game, create_player
from backend.users import log_in
from backend.tournaments import print_teams
from datetime import datetime, timedelta

# Constants
LOG_IN_MENU = '''
Please log in to start. Enter your username:
    
> '''
PASSWORD_MENU = '''
Enter your password:

> '''
TOURNAMENT_MANAGER_MENU = '''
Enter a number to begin the corresponding action.
Type 'quit' to quit.

1. View existing teams
2. Create a tournament

> '''
TEAM_MANAGER_MENU = '''
Enter a number to begin the corresponding action.
Type 'quit' to quit.

1. View existing teams
2. Create a team
3. Modify a team

> '''
OTHER_MENU = '''
Enter a number to begin the corresponding action.
Type 'quit' to quit.

1. View existing teams

> '''
# Loops for input
def control_loop():
    command = input(LOG_IN_MENU).strip()
    is_logged_in = False
    log_in_failed = False
    log_in_failed_message = None
    while command != "quit":
        if not is_logged_in:
            username = command
            password = input(PASSWORD_MENU)
            user_type = log_in(username, password)
            if not user_type:
                log_in_failed = True
            else:
                print("\nLog in successful.")
                print(f"You are logged in as type: {user_type}")
                while command != "quit":
                    if user_type == "TournamentManager":
                        command = input(TOURNAMENT_MANAGER_MENU)
                        if command == "1":
                            print_teams()
                        elif command == "2":
                            # Create a tournament
                            print("TODO")
                        elif command == "quit":
                            log_in_failed = False
                            break
                        else:
                            print("\nCommand not found.\n")
                    elif user_type == "TeamManager":
                        command = input(TEAM_MANAGER_MENU)
                        if command == "1":
                            print_teams()
                        elif command == "2":
                            # Create a team
                            print("TODO")
                        elif command == "3":
                            # Modify a team
                            print("TODO")
                        elif command == "quit":
                            log_in_failed = False
                            break
                        else:
                            print("\nCommand not found.\n")
                    else:
                        command = input(OTHER_MENU)
                        if command == "1":
                            print_teams()
                        elif command == "quit":
                            log_in_failed = False
                            break
                        else:
                            print("\nCommand not found.\n")
        if log_in_failed:
            command = input("\nLog in failed.\n" + LOG_IN_MENU)
        else:
            break
    print("\nGoodbye")

if __name__ == "__main__":
    setup_user_database()
    setup_tournament_database()
    # create_tournament("UChicago Tournament", "co-ed", 18, 24, datetime.now(),
    #     datetime.now() + timedelta(days=2))
    # create_team("UChicago", "co-ed", 18, 24, 2)
    # register_team_in_tournament(1, 1)
    # create_player("Player 1", "M", 20, 1)
    # print(get_all_tournaments())
    # print(get_all_teams())
    # create_game(datetime.now() + timedelta(days=1), 1)
    control_loop()


# Example test cases for log_in function:
# # Should be TournamentManager
# print(log_in("tm123", "password"))
# # Should be None
# print(log_in("tm123", "wrongpassword"))
# # Should be None
# print(log_in("tm1234", "password"))
# # Should be Other
# print(log_in("soccerfan01", "password"))