from database.user_database import get_all_users
from backend.users import log_in
from menu_backend.menu_backend import (
    MENU_TITLE,
    QUIT,
    TOURNAMENT_MANAGER_OPTIONS,
    TEAM_MANAGER_OPTIONS,
    OTHER_OPTIONS,
    do_tournament_manager_command,
    do_team_manager_command,
    do_other_command
)
from simple_term_menu import TerminalMenu

def log_in_menu():
    # Get all possible users, keys are the usernames
    user_dict = get_all_users()
    # Terminal menu options will be existing usernames
    options = list(user_dict.keys())
    is_logged_in = False
    # Create terminal menu with usernames as options
    terminal_menu = TerminalMenu(options, 
                                 title="Please select an existing user:")
    # Allows for retry if login fails
    while not is_logged_in:
        # Show terminal menu and save input index
        menu_entry_index = terminal_menu.show()
        username = options[menu_entry_index]
        # The menu will disappear from the screen, so we use prints to persist
        # important information
        print(f"You selected username: {username}")
        # Prompt for normal text input password
        password = input("Enter password: ")
        try:
            # Try to log in with the given information
            user_id, user_type = log_in(username, password)
            # If it works, set flag to true
            is_logged_in = True
        except TypeError:
            # If password was incorrect, there will be a type error, catch it
            # and allow the user to try again
            print("Password incorrect.")
    return user_id, user_type

def tournament_manager_menu(user_id):
    options = TOURNAMENT_MANAGER_OPTIONS
    terminal_menu = TerminalMenu(options, title=MENU_TITLE)
    command = None
    while command != QUIT:
        menu_entry_index = terminal_menu.show()
        command = options[menu_entry_index]
        do_tournament_manager_command(command, user_id)

def team_manager_menu(user_id):
    options = TEAM_MANAGER_OPTIONS
    terminal_menu = TerminalMenu(options, title=MENU_TITLE)
    command = None
    while command != QUIT:
        menu_entry_index = terminal_menu.show()
        command = options[menu_entry_index]
        do_team_manager_command(command, user_id)

def other_menu():
    options = OTHER_OPTIONS
    terminal_menu = TerminalMenu(options, title=MENU_TITLE)
    command = None
    while command != QUIT:
        menu_entry_index = terminal_menu.show()
        command = options[menu_entry_index]
        do_other_command(command)

if __name__ == "__main__":
    user_id, user_type = log_in_menu()
    print(f"You are logged in as a {user_type}.")
    if user_type == "TournamentManager":
        tournament_manager_menu(user_id)
    elif user_type == "TeamManager":
        team_manager_menu(user_id)
    else:
        other_menu()
