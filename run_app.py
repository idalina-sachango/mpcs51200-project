from database.user_database import setup_user_database
from database.tournament_database import (
    setup_tournament_database, create_tournament,
    register_team_in_tournament, create_team, create_player,
    get_team_manager_id, get_team_ids, get_team_by_id, get_tournament_ids,
    delete_player, get_player_ids, get_team_by_player)
from backend.users import log_in
from backend.tournaments import (print_teams, print_tournaments,
    check_team_eligibility)
from datetime import datetime

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
2. View existing tournaments
3. Create a tournament

> '''
TOURNAMENT_NAME_MENU = '''
Enter the tournament name:

> '''
TOURNAMENT_GENDERS_MENU = '''
Enter the gender eligible to play. Must be 'm', 'f', or 'co-ed':

> '''
GENDER_ERROR_MESSAGE = '''
Eligible gender not recognized. Returning to tournament menu. 
Press 'enter' to continue.
'''
TOURNAMENT_AGE_MIN_MENU = '''
Enter the minimum age eligible to play:

> '''
TOURNAMENT_AGE_MAX_MENU = '''
Enter the maximum age eligible to play:

> '''
AGE_ERROR_MESSAGE = '''
Age entered in incorrect format. Returning to tournament menu. 
Press 'enter' to continue.
'''
TOURNAMENT_DATE_START_MENU = '''
Enter start date. Must be written in the following form:
MM-DD-YYYY HH:MM

Start date input:

> '''
TOURNAMENT_DATE_END_MENU = '''
Enter end date. Must be written in the following form: 
MM-DD-YYYY HH:MM

End date input:

> '''
DATE_ERROR_MESSAGE = '''
Date entered in incorrect format. Returning to tournament menu.
Press 'enter' to continue.
'''
TOURNAMENT_ERROR_MESSAGE = '''
Tournament could not be created. Returning to tournament menu. 
Press 'enter' to continue.
'''

TEAM_MANAGER_MENU = '''
Enter a number to begin the corresponding action.
Type 'quit' to quit.

1. View existing teams
2. Create a team
3. Delete a player from team
4. Add player to team
5. Register for tournament

> '''
TEAM_NAME_MENU = '''
Enter the team name:

> '''
TEAM_GENDERS_MENU = '''
Enter the gender eligible to play. Must be 'm', 'f', or 'co-ed':

> '''
TEAM_GENDER_ERROR_MESSAGE = '''
Eligible gender not recognized. Returning to team menu. 
Press 'enter' to continue.
'''
TEAM_AGE_MIN_MENU = '''
Enter the minimum age eligible to play:

> '''
TEAM_AGE_MAX_MENU = '''
Enter the maximum age eligible to play:

> '''
TEAM_AGE_ERROR_MESSAGE = '''
Age entered in incorrect format. Returning to team menu. 
Press 'enter' to continue.
'''
TEAM_MAX_AGE_ERROR_MESSAGE = '''
Max age must be greater than or equal to min age. Returning to team menu. 
Press 'enter' to continue.
'''
TEAM_ERROR_MESSAGE = '''
Team could not be created. Returning to team menu. 
Press 'enter' to continue.
'''
PLAYER_TEAM_ID_MENU = '''
Enter the team id to add player:

> '''
TEAM_ID_ERROR_MESSAGE = '''
Invalid team id entered. Returning to team menu. 
Press 'enter' to continue.
'''
NOT_AUTHORIZED_ERROR_MESSAGE = '''
Not authorized. Returning to team menu. 
Press 'enter' to continue.
'''
PLAYER_NAME_MENU = '''
Enter the player name:

> '''
PLAYER_GENDER_MENU = '''
Enter the player gender. Must be 'm' or 'f':

> '''
PLAYER_GENDER_ERROR_MESSAGE = '''
Eligible gender not recognized. Returning to team menu. 
Press 'enter' to continue.
'''
PLAYER_GENDER_INELIGIBLE_ERROR_MESSAGE = '''
Gender to eligible to join team. Returning to team menu. 
Press 'enter' to continue.
'''
PLAYER_AGE_MENU = '''
Enter the age of player:

> '''
PLAYER_AGE_ERROR_MESSAGE = '''
Age entered in incorrect format. Returning to team menu. 
Press 'enter' to continue.
'''
PLAYER_AGE_INELIGIBLE_ERROR_MESSAGE = '''
Age out of range. Returning to team menu. 
Press 'enter' to continue.
'''
PLAYER_ERROR_MESSAGE = '''
Player could not be added. Returning to team menu. 
Press 'enter' to continue.
'''
REGISTER_TEAM_ID_MENU = '''
Enter the team id:

> '''
REGISTER_TOURNAMENT_ID_MENU = '''
Enter the tournament id:

> '''
TOURNAMENT_ID_ERROR_MESSAGE = '''
Invalid tournament id entered. Returning to team menu. 
Press 'enter' to continue.
'''
TEAM_INELIGIBLE_ERROR_MESSAGE = '''
Some player in team is not eligible for this tournament. 
Returning to team menu. 
Press 'enter' to continue.
'''
REGISTER_ERROR_MESSAGE = '''
Registration cannot be completed. Returning to team menu. 
Press 'enter' to continue.
'''
DELETE_PLAYER_ID_MENU = '''
Enter the player id:

> '''
DELETE_PLAYER_ID_ERROR_MESSAGE = '''
Invalid player id entered. Returning to team menu. 
Press 'enter' to continue.
'''
DELETE_PLAYER_ERROR_MESSAGE = '''
Deletion cannot be completed. Returning to team menu. 
Press 'enter' to continue.
'''

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
            user_id, user_type = log_in(username, password)
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
                            print_tournaments()
                        elif command == "3":
                            # Create a tournament
                            name = input(TOURNAMENT_NAME_MENU)
                            genders = input(TOURNAMENT_GENDERS_MENU)

                            if (name == 'quit') or (genders == 'quit'):
                                command = 'quit'
                                continue

                            # Check genders are entered correctly
                            if genders not in ['m', 'f', 'co-ed']:
                                command = input(GENDER_ERROR_MESSAGE)
                                continue
                            # Check ages
                            age_min = input(TOURNAMENT_AGE_MIN_MENU)
                            if age_min == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    age_min = int(age_min)
                                except:
                                    command = input(AGE_ERROR_MESSAGE)
                                    continue
                            age_max = input(TOURNAMENT_AGE_MAX_MENU)
                            if age_max == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    age_max = int(age_max)
                                except:
                                    command = input(AGE_ERROR_MESSAGE)
                                    continue
                            # Check date formats
                            start_date = input(TOURNAMENT_DATE_START_MENU)
                            if start_date == 'quit':
                                    command = 'quit'
                                    continue
                            else:
                                try: 
                                    start_date = datetime.strptime(start_date, 
                                        "%m-%d-%Y %H:%M")
                                except:
                                    command = input(DATE_ERROR_MESSAGE)
                                    continue
                            
                            end_date = input(TOURNAMENT_DATE_END_MENU)
                            if end_date == 'quit':
                                    command = 'quit'
                                    continue
                            else:
                                try:
                                    end_date = datetime.strptime(end_date, 
                                        "%m-%d-%Y %H:%M")
                                except:
                                    command = input(DATE_ERROR_MESSAGE)
                                    continue

                            # Check creation of tournament was succesful.
                            # If so, break loop.
                            try:
                                create_tournament(name, genders, int(age_min),
                                    int(age_max), start_date, end_date)
                                print("\nTournament successfully created.")
                            except:
                                print(TOURNAMENT_ERROR_MESSAGE)
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
                            name = input(TEAM_NAME_MENU)
                            genders = input(TEAM_GENDERS_MENU)

                            if (name == 'quit') or (genders == 'quit'):
                                command = 'quit'
                                continue

                            # Check genders are entered correctly
                            if genders not in ['m', 'f', 'co-ed']:
                                command = input(TEAM_GENDER_ERROR_MESSAGE)
                                continue
                            # Check ages
                            age_min = input(TEAM_AGE_MIN_MENU)
                            if age_min == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    age_min = int(age_min)
                                except:
                                    command = input(TEAM_AGE_ERROR_MESSAGE)
                                    continue
                            age_max = input(TEAM_AGE_MAX_MENU)
                            if age_max == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    age_max = int(age_max)
                                except:
                                    command = input(TEAM_AGE_ERROR_MESSAGE)
                                    continue
                                if age_max < age_min:
                                    command = input(TEAM_MAX_AGE_ERROR_MESSAGE)
                                    continue                                    

                            # Check if creation of team was succesful.
                            # If so, break loop.
                            try:
                                create_team(name, genders, int(age_min),
                                    int(age_max), user_id)
                                print("\nTeam successfully created.")
                            except:
                                print(TEAM_ERROR_MESSAGE)
                                continue                            
                            
                        elif command == "3":
                            # Delete player
                            player_id = input(DELETE_PLAYER_ID_MENU)
                            if player_id == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    player_id = int(player_id)
                                except:
                                    command = input(DELETE_PLAYER_ID_ERROR_MESSAGE)
                                    continue

                                # Check if player id is valid
                                player_ids = get_player_ids()
                                if not player_id in player_ids:
                                    command = input(DELETE_PLAYER_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if player is on a team managed by user
                                player_team_id = get_team_by_player(player_id)
                                if not get_team_manager_id(player_team_id) == user_id:
                                    command = input(NOT_AUTHORIZED_ERROR_MESSAGE)
                                    continue
                                  
                            # Check if deletion of player was succesful.
                            # If so, break loop.
                            try:
                                delete_player(player_id)
                                print("\nDeletion successful.")
                            except:
                                print(DELETE_PLAYER_ERROR_MESSAGE)
                                continue   
                            
                        elif command == "4":
                            # Add team player
                            team_id = input(PLAYER_TEAM_ID_MENU)
                            if team_id == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    team_id = int(team_id)
                                except:
                                    command = input(TEAM_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if team number is valid
                                team_ids = get_team_ids()
                                if not team_id in team_ids:
                                    command = input(TEAM_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if team belongs to manager
                                if not get_team_manager_id(team_id) == user_id:
                                    command = input(NOT_AUTHORIZED_ERROR_MESSAGE)
                                    continue

                            name = input(PLAYER_NAME_MENU)
                            gender = input(PLAYER_GENDER_MENU)

                            if (name == 'quit') or (gender == 'quit'):
                                command = 'quit'
                                continue

                            # Check genders are entered correctly
                            if gender not in ['m', 'f']:
                                command = input(PLAYER_GENDER_ERROR_MESSAGE)
                                continue

                            # Check if gender is allowed in team
                            allowed_genders = get_team_by_id(team_id)["team_gender"]
                            if not allowed_genders == "co-ed" and not allowed_genders == gender:
                                command = input(PLAYER_GENDER_INELIGIBLE_ERROR_MESSAGE)
                                continue  

                            # Check ages
                            age = input(PLAYER_AGE_MENU)
                            if age == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    age = int(age)
                                except:
                                    command = input(PLAYER_AGE_ERROR_MESSAGE)
                                    continue
                                
                                # Check if age is eligible for team
                                team_min_age = get_team_by_id(team_id)["team_age_min"]
                                team_max_age = get_team_by_id(team_id)["team_age_max"]

                                if age < team_min_age or age > team_max_age:
                                    command = input(PLAYER_AGE_INELIGIBLE_ERROR_MESSAGE)
                                    continue   

                            # Check if creation of player was succesful.
                            # If so, break loop.
                            try:
                                create_player(name, gender, age, team_id)
                                print("\nPlayer successfully added.")
                            except:
                                print(PLAYER_ERROR_MESSAGE)
                                continue       
                                                  
                        elif command == "5":
                            # Register for tourament
                            team_id = input(REGISTER_TEAM_ID_MENU)
                            if team_id == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    team_id = int(team_id)
                                except:
                                    command = input(TEAM_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if team number is valid
                                team_ids = get_team_ids()
                                if not team_id in team_ids:
                                    command = input(TEAM_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if team belongs to manager
                                if not get_team_manager_id(team_id) == user_id:
                                    command = input(NOT_AUTHORIZED_ERROR_MESSAGE)
                                    continue

                            tournament_id = input(REGISTER_TOURNAMENT_ID_MENU)
                            if tournament_id == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    tournament_id = int(tournament_id)
                                except:
                                    command = input(TOURNAMENT_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if tournament_id is valid
                                tournament_ids = get_tournament_ids()
                                if not tournament_id in tournament_ids:
                                    command = input(TOURNAMENT_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if all team members meet gender and age requirments
                                if not check_team_eligibility(team_id, tournament_id):
                                    command = input(TEAM_INELIGIBLE_ERROR_MESSAGE)
                                    continue

                            # Check if registration was succesful.
                            # If so, break loop.
                            try:
                                register_team_in_tournament(tournament_id, team_id)
                                print("\nRegistration successful.")
                            except:
                                print(REGISTER_ERROR_MESSAGE)
                                continue 

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
    control_loop()
