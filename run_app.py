from database.user_database import setup_user_database
from database.tournament_database import (
    setup_tournament_database, create_tournament,
    register_team_in_tournament, create_team, create_player,
    get_team_manager_id, get_team_ids, get_team_by_id, get_tournament_ids,
    delete_player, get_player_ids, get_team_by_player, get_tournament_by_name,
    create_game)
from backend.users import log_in
from backend.tournaments import (print_teams, print_tournaments,
    check_team_eligibility)
from datetime import datetime
import menu_prompts.prompts as prompt

# Loops for input
def control_loop():
    command = input(prompt.LOG_IN_MENU).strip()
    is_logged_in = False
    log_in_failed = False
    while command != "quit":
        if not is_logged_in:
            username = command
            password = input(prompt.PASSWORD_MENU)
            user_id, user_type = log_in(username, password)
            if not user_type:
                log_in_failed = True
            else:
                print("\nLog in successful.")
                print(f"You are logged in as type: {user_type}")
                while command != "quit":
                    if user_type == "TournamentManager":
                        command = input(prompt.TOURNAMENT_MANAGER_MENU)
                        if command == "1":
                            print_teams()
                        elif command == "2":
                            print_tournaments()
                        elif command == "3":
                            # Create a tournament
                            name = input(prompt.TOURNAMENT_NAME_MENU)
                            genders = input(prompt.TOURNAMENT_GENDERS_MENU)

                            if (name == 'quit') or (genders == 'quit'):
                                command = 'quit'
                                continue

                            # Check genders are entered correctly
                            if genders not in ['m', 'f', 'co-ed']:
                                command = input(prompt.GENDER_ERROR_MESSAGE)
                                continue
                            # Check ages
                            age_min = input(prompt.TOURNAMENT_AGE_MIN_MENU)
                            if age_min == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    age_min = int(age_min)
                                except:
                                    command = input(prompt.AGE_ERROR_MESSAGE)
                                    continue
                            age_max = input(prompt.TOURNAMENT_AGE_MAX_MENU)
                            if age_max == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    age_max = int(age_max)
                                except:
                                    command = input(prompt.AGE_ERROR_MESSAGE)
                                    continue
                            # Check date formats
                            start_date = input(prompt.TOURNAMENT_DATE_START_MENU)
                            if start_date == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try: 
                                    start_date = datetime.strptime(start_date, 
                                        "%m-%d-%Y %H:%M")
                                except:
                                    command = input(prompt.DATE_ERROR_MESSAGE)
                                    continue
                            
                            end_date = input(prompt.TOURNAMENT_DATE_END_MENU)
                            if end_date == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    end_date = datetime.strptime(end_date, 
                                        "%m-%d-%Y %H:%M")
                                except:
                                    command = input(prompt.DATE_ERROR_MESSAGE)
                                    continue
                            location = input(prompt.TOURNAMENT_LOCATION_MENU)
                            if location == 'quit':
                                command = 'quit'
                                continue

                            # Check creation of tournament was succesful.
                            # If so, break loop.
                            try:
                                create_tournament(name, genders, int(age_min),
                                    int(age_max), start_date, end_date, int(user_id), location)
                                print("\nTournament successfully created.")
                            except:
                                print(prompt.TOURNAMENT_ERROR_MESSAGE)
                                continue
                        elif command == "4":
                            # Create game
                            time = input(prompt.GAME_TIME_MENU)
                            tournament_name = input(prompt.TOURNAMENT_NAME_MENU)
                            home_team = input(prompt.GAME_HOMETEAM_MENU)
                            away_team = input(prompt.GAME_AWAYTEAM_MENU)
                            location = input(prompt.GAME_LOCATION)
                            tournament_id = get_tournament_by_name(tournament_name)
                            try:
                                time = datetime.strptime(time, 
                                    "%H:%M")
                            except:
                                command = input(prompt.TIME_ERROR)
                                continue
                            try:
                                tournament_id = int(tournament_id)
                            except:
                                command = input(prompt.INT_ERROR)
                                continue
                            try:
                                if home_team:
                                    home_team = int(home_team)
                            except:
                                command = input(prompt.INT_ERROR)
                                continue
                            try:
                                if away_team:
                                    away_team = int(away_team)
                            except:
                                command = input(prompt.INT_ERROR)
                                continue
                            if (time == 'quit') or (home_team == 'quit') or (away_team == 'quit') or (tournament_name == 'quit'):
                                command = 'quit'
                                continue
                            else:
                                try:
                                    create_game(time, tournament_id, location, home_team, away_team)
                                    print("\nGame successfully created.")
                                except:
                                    print(prompt.GAME_ERROR_MESSAGE)
                                    continue
                        elif command == "5":
                            # 5. Input scores
                            continue
                        elif command == "6":
                            # 6. Set tournament location
                            continue
                        elif command == "quit":
                            log_in_failed = False
                            break
                        else:
                            print("\nCommand not found.\n")
                    elif user_type == "TeamManager":
                        command = input(prompt.TEAM_MANAGER_MENU)
                        if command == "1":
                            print_teams()
                        elif command == "2":
                            # Create a team
                            name = input(prompt.TEAM_NAME_MENU)
                            genders = input(prompt.TEAM_GENDERS_MENU)

                            if (name == 'quit') or (genders == 'quit'):
                                command = 'quit'
                                continue

                            # Check genders are entered correctly
                            if genders not in ['m', 'f', 'co-ed']:
                                command = input(prompt.TEAM_GENDER_ERROR_MESSAGE)
                                continue
                            # Check ages
                            age_min = input(prompt.TEAM_AGE_MIN_MENU)
                            if age_min == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    age_min = int(age_min)
                                except:
                                    command = input(prompt.TEAM_AGE_ERROR_MESSAGE)
                                    continue
                            age_max = input(prompt.TEAM_AGE_MAX_MENU)
                            if age_max == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    age_max = int(age_max)
                                except:
                                    command = input(prompt.TEAM_AGE_ERROR_MESSAGE)
                                    continue
                            if age_max < age_min:
                                command = input(prompt.TEAM_MAX_AGE_ERROR_MESSAGE)
                                continue                                    

                            # Check if creation of team was succesful.
                            # If so, break loop.
                            try:
                                create_team(name, genders, int(age_min),
                                    int(age_max), user_id)
                                print("\nTeam successfully created.")
                            except:
                                print(prompt.TEAM_ERROR_MESSAGE)
                                continue                            
                            
                        elif command == "3":
                            # Delete player
                            player_id = input(prompt.DELETE_PLAYER_ID_MENU)
                            if player_id == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    player_id = int(player_id)
                                except:
                                    command = input(prompt.DELETE_PLAYER_ID_ERROR_MESSAGE)
                                    continue

                                # Check if player id is valid
                                player_ids = get_player_ids()
                                if not player_id in player_ids:
                                    command = input(prompt.DELETE_PLAYER_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if player is on a team managed by user
                                player_team_id = get_team_by_player(player_id)
                                if not get_team_manager_id(player_team_id) == user_id:
                                    command = input(prompt.NOT_AUTHORIZED_ERROR_MESSAGE)
                                    continue
                                  
                            # Check if deletion of player was succesful.
                            # If so, break loop.
                            try:
                                delete_player(player_id)
                                print("\nDeletion successful.")
                            except:
                                print(prompt.DELETE_PLAYER_ERROR_MESSAGE)
                                continue   
                            
                        elif command == "4":
                            # Add team player
                            team_id = input(prompt.PLAYER_TEAM_ID_MENU)
                            if team_id == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    team_id = int(team_id)
                                except:
                                    command = input(prompt.TEAM_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if team number is valid
                                team_ids = get_team_ids()
                                if not team_id in team_ids:
                                    command = input(prompt.TEAM_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if team belongs to manager
                                if not get_team_manager_id(team_id) == user_id:
                                    command = input(prompt.NOT_AUTHORIZED_ERROR_MESSAGE)
                                    continue

                            name = input(prompt.PLAYER_NAME_MENU)
                            gender = input(prompt.PLAYER_GENDER_MENU)

                            if (name == 'quit') or (gender == 'quit'):
                                command = 'quit'
                                continue

                            # Check genders are entered correctly
                            if gender not in ['m', 'f']:
                                command = input(prompt.PLAYER_GENDER_ERROR_MESSAGE)
                                continue

                            # Check if gender is allowed in team
                            allowed_genders = get_team_by_id(team_id)["team_gender"]
                            if not allowed_genders == "co-ed" and not allowed_genders == gender:
                                command = input(prompt.PLAYER_GENDER_INELIGIBLE_ERROR_MESSAGE)
                                continue  

                            # Check ages
                            age = input(prompt.PLAYER_AGE_MENU)
                            if age == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    age = int(age)
                                except:
                                    command = input(prompt.PLAYER_AGE_ERROR_MESSAGE)
                                    continue
                                
                                # Check if age is eligible for team
                                team_min_age = get_team_by_id(team_id)["team_age_min"]
                                team_max_age = get_team_by_id(team_id)["team_age_max"]

                                if age < team_min_age or age > team_max_age:
                                    command = input(prompt.PLAYER_AGE_INELIGIBLE_ERROR_MESSAGE)
                                    continue   

                            # Check if creation of player was succesful.
                            # If so, break loop.
                            try:
                                create_player(name, gender, age, team_id)
                                print("\nPlayer successfully added.")
                            except:
                                print(prompt.PLAYER_ERROR_MESSAGE)
                                continue       
                                                  
                        elif command == "5":
                            # Register for tourament
                            team_id = input(prompt.REGISTER_TEAM_ID_MENU)
                            if team_id == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    team_id = int(team_id)
                                except:
                                    command = input(prompt.TEAM_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if team number is valid
                                team_ids = get_team_ids()
                                if not team_id in team_ids:
                                    command = input(prompt.TEAM_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if team belongs to manager
                                if not get_team_manager_id(team_id) == user_id:
                                    command = input(prompt.NOT_AUTHORIZED_ERROR_MESSAGE)
                                    continue

                            tournament_id = input(prompt.REGISTER_TOURNAMENT_ID_MENU)
                            if tournament_id == 'quit':
                                command = 'quit'
                                continue
                            else:
                                try:
                                    tournament_id = int(tournament_id)
                                except:
                                    command = input(prompt.TOURNAMENT_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if tournament_id is valid
                                tournament_ids = get_tournament_ids()
                                if not tournament_id in tournament_ids:
                                    command = input(prompt.TOURNAMENT_ID_ERROR_MESSAGE)
                                    continue
                                
                                # Check if all team members meet gender and age requirments
                                if not check_team_eligibility(team_id, tournament_id):
                                    command = input(prompt.TEAM_INELIGIBLE_ERROR_MESSAGE)
                                    continue

                            # Check if registration was succesful.
                            # If so, break loop.
                            try:
                                register_team_in_tournament(tournament_id, team_id)
                                print("\nRegistration successful.")
                            except:
                                print(prompt.REGISTER_ERROR_MESSAGE)
                                continue 

                        elif command == "quit":
                            log_in_failed = False
                            break
                        else:
                            print("\nCommand not found.\n")
                    else:
                        command = input(prompt.OTHER_MENU)
                        if command == "1":
                            print_teams()
                        elif command == "quit":
                            log_in_failed = False
                            break
                        else:
                            print("\nCommand not found.\n")
        if log_in_failed:
            command = input("\nLog in failed.\n" + prompt.LOG_IN_MENU)
        else:
            break
    print("\nGoodbye")

if __name__ == "__main__":
    setup_user_database()
    setup_tournament_database()
    control_loop()
