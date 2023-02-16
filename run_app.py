from database.user_database import setup_user_database, get_all_users
from database.tournament_database import setup_tournament_database, create_tournament, register_team_in_tournament, create_team, create_game, create_player
from backend.users import log_in
from backend.tournaments import print_teams
from datetime import datetime, timedelta
import re

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
TOURNAMENT_NAME_MENU = '''
Enter the tournament name:

> '''
TOURNAMENT_GENDERS_MENU = '''
Enter the genders eligible to play:

> '''
TOURNAMENT_AGEMIN_MENU = '''
Enter the minimum age required to play:

> '''
TOURNAMENT_AGEMAX_MENU = '''
Enter the maximum age of play:

> '''
TOURNAMENT_DATESTART_MENU = '''
Enter start date. Must be written in the following form:
MM-DD-YYYY HH:MM

Start date input:

> '''
TOURNAMENT_DATEEND_MENU = '''
Enter end date. Must be written in the following form: 
MM-DD-YYYY HH:MM

End date input:

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
                            tournament_creation_failed = False

                            name = input(TOURNAMENT_NAME_MENU)
                            genders = input(TOURNAMENT_GENDERS_MENU)
                            if (name == 'quit') or (genders == 'quit'):
                                command = 'quit'
                                continue

                            # check genders are entered correctly
                            if genders not in ['m', 'f', 'co-ed']:
                                command = input("Eligible genders entered in incorrect format. Returning to tournament menu. Press 'enter' to continue.")
                                continue
                            # Check ages
                            age_min = input(TOURNAMENT_AGEMIN_MENU)
                            if age_min == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    age_min = int(age_min)
                                except:
                                    command = input("Minimum age entered in incorrect format. Returning to tournament menu. Press 'enter' to continue.")
                                    continue
                            age_max = input(TOURNAMENT_AGEMAX_MENU)
                            if age_max == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    age_max = int(age_max)
                                except:
                                    command = input("Maximum age entered in incorrect format. Returning to tournament menu. Press 'enter' to continue.")
                                    continue
                            # Check date formats
                            start_date = input(TOURNAMENT_DATESTART_MENU)
                            if start_date == 'quit':
                                    command = 'quit'
                                    continue
                            else:
                                try: 
                                    start_date = datetime.strptime(start_date, "%m-%d-%Y %H:%M")
                                except:
                                    command = input("\nDate entered in incorrect format. Returning to tournament page. Press 'enter' to continue.")
                                    continue
                            
                            end_date = input(TOURNAMENT_DATEEND_MENU)
                            if end_date == 'quit':
                                    command = 'quit'
                                    continue
                            else:
                                try:
                                    end_date = datetime.strptime(end_date, "%m-%d-%Y %H:%M")
                                except:
                                    command = input("\nDate entered in incorrect format. Returning to tournament page.. Press 'enter' to continue.")
                                    continue

                            # Check creation of tournament was succesful. If so, break loop.
                            try:
                                create_tournament(name, genders, int(age_min), int(age_max), start_date, end_date)
                                print("\nTournament successfully created.")
                                command = "quit"
                            except:
                                print("\nTournament could not be created. Returning to tournament main page. Press 'enter' to continue.")
                                continue

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
