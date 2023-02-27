from database.tournament_database import (
    setup_tournament_database,
    clear_tournament_database, 
    create_tournament,
    create_team,
    register_team_in_tournament,
    create_game,
    create_game_score)
from database.user_database import setup_user_database
from datetime import datetime, timedelta
from sqlite3 import IntegrityError
import menu_prompts.prompts as prompt
import unittest

class TestCreateScores(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Confirm that the user wants to run tests, which will delete any data
        # created by using run_app.py
        confirmation = input(prompt.TEST_WARNING)
        if confirmation.lower() != "confirm":
            raise Exception("Confirmation not accepted.")
        setup_user_database()
        clear_tournament_database()
        setup_tournament_database()
        # Creates tournament with ID 1
        create_tournament("Test Name", 
                            "m", 
                            18, 
                            24, 
                            datetime.now(), 
                            datetime.now() + timedelta(days = 2),
                            1,
                            "Test Location")
        # Creates team with ID 1
        create_team("Test Name 1",
                    "m",
                    19,
                    20,
                    2)
        # Creates team with ID 2
        create_team("Test Name 2",
                    "m",
                    19,
                    20,
                    4)
        # Registers both teams in tournament
        register_team_in_tournament(1, 1)
        register_team_in_tournament(1, 2)
        # Creates game with ID 1
        create_game(datetime.now() + timedelta(hours=1),
                    1,
                    "Test Location",
                    1,
                    2)
        # Creates game with ID 2
        create_game(datetime.now() + timedelta(hours=3),
                    1,
                    "Test Location",
                    1,
                    None)
        
    def test_good(self):
        create_game_score(1, 4, 3)

    def test_game_does_not_exist(self):
        self.assertRaises(IntegrityError, create_game_score, 7, 4, 3)

    def test_game_id_not_int(self):
        self.assertRaises(AssertionError, 
                          create_game_score, 
                          "not an int", 4, 3)
        
    def test_home_team_score_not_int(self):
        self.assertRaises(AssertionError, 
                          create_game_score, 
                          1, "not an int", 3)
        
    def test_away_team_score_not_int(self):
        self.assertRaises(AssertionError, 
                          create_game_score, 
                          1, 4, "not an int")

if __name__ == "__main__":
    unittest.main()
