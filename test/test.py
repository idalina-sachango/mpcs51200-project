import pytest
from database.user_database import setup_user_database
from database.tournament_database import (
    setup_tournament_database, create_tournament,
    register_team_in_tournament, create_team, create_player,
    get_team_manager_id, get_team_ids, get_team_by_id, get_tournament_ids,
    delete_player, get_player_ids, get_team_by_player, get_tournament_by_name,
    create_game, get_tournament_by_id, get_tournament_manager_id, close_reg)
from backend.users import log_in
from backend.tournaments import (print_teams, print_tournaments,
    check_team_eligibility)
from datetime import datetime
import menu_prompts.prompts as prompt
import run_app as run
import os

def test_initialize():
    setup_user_database()
    setup_tournament_database()

def test_check_credentials():
    username, password = "tm123", "password"
    assert log_in(username, password) == (1, 'TournamentManager')
    username, password = "tm123", "passwor"
    assert log_in(username, password) == None
    username, password = "originalcoach", "password"
    assert log_in(username, password) == (2, 'TeamManager')

def test_createtournament():
    # correct tournament
    name, genders, age_min, age_max, start_date, end_date, user_id, location = "Chicago chargers", "m", 20, 30, datetime.strptime("04-01-2023 12:00", "%m-%d-%Y %H:%M"), datetime.strptime("06-01-2023 12:00", "%m-%d-%Y %H:%M"), 1, "Chicago"
    assert create_tournament(name, genders, int(age_min),
                                    int(age_max), start_date, end_date, int(user_id), location) == None
    name, genders, age_min, age_max, start_date, end_date, user_id, location = "Chicago bulls", "m", 20, 30, datetime.strptime("04-01-2023 12:00", "%m-%d-%Y %H:%M"), datetime.strptime("03-01-2023 12:00", "%m-%d-%Y %H:%M"), 1, "Chicago"
    try:
        create_tournament(name, genders, int(age_min),
                                    int(age_max), start_date, end_date, int(user_id), location)
    except AssertionError:
        assert True

    name, genders, age_min, age_max, start_date, end_date, user_id, location = "Chicago bulls", "m", 20, "him", datetime.strptime("04-01-2023 12:00", "%m-%d-%Y %H:%M"), datetime.strptime("06-01-2023 12:00", "%m-%d-%Y %H:%M"), 1, "Chicago"
    try:
        create_tournament(name, genders, int(age_min),
                                    int(age_max), start_date, end_date, int(user_id), location)
    except ValueError:
        assert True

def test_creategame():
    




def test_drop():
    os.remove("users.db")
    os.remove("tournaments.db")

    
