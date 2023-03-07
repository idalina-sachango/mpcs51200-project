from database.tournament_database import (
    create_game_score,
    create_team,
    create_tournament,
    create_game,
    get_tournaments_by_manager,
<<<<<<< HEAD
    get_games_by_tournament,
    get_all_teams)
=======
    get_teams_by_manager,
    get_games_by_tournament,
    get_team_by_id,
    create_player,
    get_players_by_team,
    delete_player)
>>>>>>> 85a2075932a208ba18029e22ea058fa4bc149990
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
SELECT_TEAM = "Select a team."
SELECT_PLAYER = "Select a player."

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

def team_selection(user_id):
    # Add team player
    teams = get_teams_by_manager(user_id)
    if not teams:
        return
    # Create a dictionary where the keys are the string options that a user
    # will select on the menu, and the values are the corresponding teams
    # IDs. Example: { "ID: 1, Name: Test Name": 1 }
    team_options_dict = {}
    for team in teams.values():
        team_id = team["team_id"]
        key = f"ID: {team_id}, Name: {team['name']}"
        team_options_dict[key] = team_id
    # Options to display are in the format "[ID] Name" created above
    team_options = list(team_options_dict.keys())
    terminal_menu = TerminalMenu(team_options, title=SELECT_TEAM)
    menu_entry_index = terminal_menu.show()
    # This is the string the user selected, which is the key for options_dict
    team_key = team_options[menu_entry_index]
    print(f"You selected team: {team_key}")
    # Use the key to get the tournament ID
    team_id = team_options_dict[team_key]
    return team_id

def player_selection(team_id):
    # Add team player
    players = get_players_by_team(team_id)
    if not players:
        return
    # Create a dictionary where the keys are the string options that a user
    # will select on the menu, and the values are the corresponding teams
    # IDs. Example: { "ID: 1, Name: Test Name": 1 }
    player_options_dict = {}
    for player in players.values():
        player_id = player["player_id"]
        key = f"ID: {player_id}, Name: {player['name']}"
        player_options_dict[key] = player_id
    # Options to display are in the format "[ID] Name" created above
    player_options = list(player_options_dict.keys())
    terminal_menu = TerminalMenu(player_options, title=SELECT_PLAYER)
    menu_entry_index = terminal_menu.show()
    # This is the string the user selected, which is the key for options_dict
    player_key = player_options[menu_entry_index]
    print(f"You selected team: {player_key}")
    # Use the key to get the tournament ID
    player_id = player_options_dict[player_key]
    return player_id

def do_add_player(user_id):
    # Add team player
    team_id = team_selection(user_id)
    if not team_id:
        print("You don't have any teams.")
        return

    name = input("Enter player name: ")

    terminal_menu = TerminalMenu(
        ["M", "F"],
        multi_select=True,
        show_multi_select_hint=True,
    )
    terminal_menu.show()
    input_genders = terminal_menu.chosen_menu_entries
    if len(input_genders) == 2:
        gender = "co-ed"
    else:
        gender = input_genders[0].lower()

    # Check if gender is allowed in team
    allowed_genders = get_team_by_id(team_id)["team_gender"]
    if not allowed_genders == "co-ed" and not allowed_genders == gender:
        print("Gender ineligible for team.")
        return


    age = input("Enter player age: ")

    try:
        age = int(age)
    except:
        print("Age must be a integer.")
        return
        
    # Check if age is eligible for team
    team_min_age = get_team_by_id(team_id)["team_age_min"]
    team_max_age = get_team_by_id(team_id)["team_age_max"]

    if age < team_min_age or age > team_max_age:
        print("Age ineligible for team.")
        return

    try:
        create_player(name, gender, age, team_id)
    except Exception as err:
        print("There was an error:")
        print(err)
        return
    
    print("Player created successfully.")

def do_delete_player(user_id):
    team_id = team_selection(user_id)
    if not team_id:
        print("You don't have any teams.")
        return
    player_id = player_selection(team_id)
    if not player_id:
        print("You don't have any players.")
        return
    
    # Check if deletion of player was succesful.
    try:
        delete_player(player_id)
        print("\nDeletion successful.")
    except Exception as err:
        print("There was an error:")
        print(err)


def do_input_score_command(user_id):
    tournament_id = grab_tournament_id(user_id)

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

<<<<<<< HEAD
def do_create_game_command(user_id):
    tournament_id = grab_tournament_id(user_id)
    teams = get_all_teams()

    # Create game
    team_options = list(teams.values())
    team_ids = []
    team_names = []
    for team in teams.values():
        team_ids.append(team["team_id"])
        team_names.append(team["name"])

    team_menu = TerminalMenu(team_names, title="Select home team: ")
    menu_entry_index = team_menu.show()
    home_team_id = team_ids[menu_entry_index]

    team_menu = TerminalMenu(team_names, title="Select away team: ")
    menu_entry_index = team_menu.show()
    away_team_id = team_ids[menu_entry_index]

    time = input(f"Enter game start time in the format 'HH:MM': ")
    location = input("Enter field location of the game: ")

    try:
        time = datetime.strptime(time, 
            "%H:%M")
    except:
        command = input("Time must be datetime")
        return

    try:
        create_game(time, tournament_id, location, home_team_id, away_team_id)
        print("\nGame successfully created.")
    except Exception as err:
        print("There was an error")
        print(err)
        return

=======
def do_register_tournament(user_id):
    pass
>>>>>>> 85a2075932a208ba18029e22ea058fa4bc149990

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
        do_create_game_command(user_id)
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
        do_create_team_command(user_id)
    elif command == ADD_PLAYER:
        do_add_player(user_id)
    elif command == DELETE_PLAYER:
        do_delete_player(user_id)
    elif command == REGISTER_FOR_TOURNAMENT:
        do_register_tournament(user_id)

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

def grab_tournament_id(user_id):
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
    return tournament_id



