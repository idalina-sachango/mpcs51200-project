from database.tournament_database import (
    create_game_score,
    create_team,
    create_tournament,
    get_tournaments_by_manager,
    get_games_by_tournament)
from backend.tournaments import print_all_teams, print_all_tournaments
from simple_term_menu import TerminalMenu
from datetime import datetime, date

###############################################################################
# CONSTANT TITLES AND ERROR MESSAGES
###############################################################################

# Title to be displayed above all menus
MENU_TITLE = '''Please select an action using up/down arrows and enter.
Press q to quit.'''

SELECT_TOURNAMENT = "Select a tournament."

AGE_INT_ERROR = "Age must be an integer."
SCORE_INT_ERROR = "Score input must be an integer."
DATE_ERROR = "Date must be datetime"

###############################################################################
# CONSTANT MENU OPTIONS
###############################################################################

# Need by all user types
VIEW_ALL_TEAMS = "View all teams"
VIEW_ALL_TOURNAMENTS = "View all tournaments"
QUIT = "[q] Quit"

# Needed by tournament managers only
CREATE_TOURNAMENT = "Create a tournament"
CREATE_GAME = "Create a game"
INPUT_SCORE = "Input score for an existing game"
SET_TOURNAMENT_LOCATION = "Set tournament location"
CLOSE_REGISTRATION = "Close registration for an existing tournament"
# Probably want to refactor this one to show the tournament manager's
# tournaments and allow them to select, also probably should rename
# to "show tournament schedule" or something
SHOW_TOURNAMENT_STATUS = "Show tournament status by id"

# Needed by team managers only
CREATE_TEAM = "Create a team"
DELETE_PLAYER = "Delete a player from an existing team"
ADD_PLAYER = "Add a player to an existing team"
REGISTER_FOR_TOURNAMENT = "Register for a tournament"

# Options for viewing teams or tournaments, all user types have access
VIEW_OPTIONS = [VIEW_ALL_TEAMS, VIEW_ALL_TOURNAMENTS]

TOURNAMENT_MANAGER_OPTIONS = VIEW_OPTIONS + [
    CREATE_TOURNAMENT,
    CREATE_GAME,
    INPUT_SCORE,
    SET_TOURNAMENT_LOCATION,
    CLOSE_REGISTRATION,
    SHOW_TOURNAMENT_STATUS
] + [QUIT]

TEAM_MANAGER_OPTIONS = VIEW_OPTIONS + [
    CREATE_TEAM,
    ADD_PLAYER,
    DELETE_PLAYER,
    REGISTER_FOR_TOURNAMENT
] + [QUIT]

OTHER_OPTIONS = VIEW_OPTIONS + [QUIT]

###############################################################################
# COMMAND EXECUTION FUNCTIONS
###############################################################################

def do_create_team_command(user_id):
    name = input("Enter a team name: ")
    terminal_menu = TerminalMenu(
        ["M", "F"],
        multi_select=True,
        show_multi_select_hint=True,
    )
    terminal_menu.show()
    input_genders = terminal_menu.chosen_menu_entries
    if len(input_genders) == 2:
        genders = "co-ed"
    else:
        genders = input_genders[0].lower()
    
    age_min = input("Enter the minimum age eligible to play: ")
    try:
        age_min_int = int(age_min)
    except ValueError:
        print(AGE_INT_ERROR)
        return

    age_max = input("Enter the maximum age eligible to play: ")
    try:
        age_max_int = int(age_max)
    except ValueError:
        print(AGE_INT_ERROR)
        return
    
    if age_max_int < age_min_int:
        print("Maximum age must be larger than minimum age.")
        return
    
    try:
        create_team(name, genders, age_min_int, age_max_int, user_id)
    except Exception as err:
        print("There was an error:")
        print(err)
        return
    
    print("Team created successfully.")

def do_input_score_command(user_id):
    tournaments = get_tournaments_by_manager(user_id)
    # Create a dictionary where the keys are the string options that a user
    # will select on the menu, and the values are the corresponding tournament
    # IDs. Example: { "ID: 1, Name: Test Name": 1 }
    tournament_options_dict = {}
    for tournament in tournaments.values():
        tournament_id = tournament["tournament_id"]
        key = f"ID: {tournament_id}, Name: {tournament['name']}"
        tournament_options_dict[key] = tournament_id
    # Options to display are in the format "[ID] Name" created above
    tournament_options = list(tournament_options_dict.keys())
    terminal_menu = TerminalMenu(tournament_options, title=SELECT_TOURNAMENT)
    menu_entry_index = terminal_menu.show()
    # This is the string the user selected, which is the key for options_dict
    tournament_key = tournament_options[menu_entry_index]
    print(f"You selected tournament: {tournament_key}")
    # Use the key to get the tournament ID
    tournament_id = tournament_options_dict[tournament_key]

    # Same as above but for games
    games = get_games_by_tournament(tournament_id)
    game_options_dict = {}
    for game in games.values():
        game_id = game["game_id"]
        key = (f"ID: {game_id}, Time: {game['time']}, Location: " +
            f"{game['location']}")
        game_options_dict[key] = game_id
    game_options = list(game_options_dict.keys())
    terminal_menu = TerminalMenu(game_options, title=SELECT_TOURNAMENT)
    menu_entry_index = terminal_menu.show()
    game_key = game_options[menu_entry_index]
    print(f"You selected game: {game_key}")
    game_id = game_options_dict[game_key]

    # Basically same as run_app.py
    home_team_score = input("Enter home team score: ")
    try:
        home_team_score_int = int(home_team_score)
    except ValueError:
        print(SCORE_INT_ERROR)
        return

    away_team_score = input("Enter away team score: ")
    try:
        away_team_score_int = int(away_team_score)
    except ValueError:
        print(SCORE_INT_ERROR)
        return

    try:
        create_game_score(game_id, home_team_score_int, away_team_score_int)
    except Exception as err:
        print("There was an error:")
        print(err)
        return
    print("Score created successfully.")

def do_create_tournament_command(user_id):
    # Create a tournament
    name = input("Enter tournament name: ")
    gender_options = ["m", "f", "co-ed"]
    terminal_menu = TerminalMenu(gender_options, title="Select eligible genders: ")
    menu_entry_index = terminal_menu.show()
    gender = gender_options[menu_entry_index]

    age_min = input("Enter minimum eligible age: ")
    try:
        age_min = int(age_min)
    except:
        command = input(AGE_INT_ERROR)
        return
    age_max = input("Enter maximum eligible age: ")
    try:
        age_max = int(age_max)
    except:
        command = input(AGE_INT_ERROR)
        return
    # Check date formats
    # start_date = input("Enter tournament start date in the format 'MM-DD-YYYY HH:MM': ")
    start_date = create_date(start="START")
    try: 
        start_date = datetime.strptime(start_date, 
            "%B-%d-%Y %H:%M")
        print(f"Your entered tournament start date: {start_date}")
    except:
        command = input(DATE_ERROR)
        return
    
    end_date = create_date(start="END")
    try:
        end_date = datetime.strptime(end_date, 
            "%B-%d-%Y %H:%M")
        print(f"Your entered tournament end date: {start_date}")
    except:
        command = input(DATE_ERROR)
        return
    location = input("Enter tournament location in the format 'city, state': ")
    # Check creation of tournament was succesful.
    # If so, break loop.
    try:
        create_tournament(name, gender, age_min,
            age_max, start_date, end_date, user_id, location)
        print("\nTournament successfully created.")
    except Exception as err:
        print("There was an error")
        print(err)
        return


###############################################################################
# COMMAND CONTROL FLOW FUNCTIONS
###############################################################################

def do_view_command(command):
    if command == VIEW_ALL_TEAMS:
        print_all_teams()
    elif command == VIEW_ALL_TOURNAMENTS:
        print_all_tournaments()

def do_tournament_manager_command(command, user_id):
    if command in VIEW_OPTIONS:
        do_view_command(command)
    elif command == CREATE_TOURNAMENT:
        do_create_tournament_command(user_id)
        return
    elif command == CREATE_GAME:
        # TODO
        return
    elif command == INPUT_SCORE:
        do_input_score_command(user_id)
    elif command == SET_TOURNAMENT_LOCATION:
        # TODO
        return
    elif command == CLOSE_REGISTRATION:
        # TODO
        return
    elif command == SHOW_TOURNAMENT_STATUS:
        # TODO
        return

def do_team_manager_command(command, user_id):
    if command in VIEW_OPTIONS:
        do_view_command(command)
    elif command == CREATE_TEAM:
        # TODO
        do_create_team_command(user_id)
    elif command == ADD_PLAYER:
        # TODO
        return
    elif command == DELETE_PLAYER:
        # TODO
        return
    elif command == REGISTER_FOR_TOURNAMENT:
        # TODO
        return

def do_other_command(command):
    if command in VIEW_OPTIONS:
        do_view_command(command)

def create_date(start):
    month_options = ["January", "February", "March", "April", "May",
    "June", "July", "August", "September", "November", "December"]

    year = input(f"Enter tournament {start} year: ")
    month_menu = TerminalMenu(month_options, title=f"Select tournament {start} month: ")
    menu_entry_index = month_menu.show()
    day = input(f"Enter tournament {start} day in the format 'DD': ")
    time = input(f"Enter tournament {start} time in the format 'HH:MM': ")
    return f"{month_options[menu_entry_index]}-{day}-{year} {time}"



