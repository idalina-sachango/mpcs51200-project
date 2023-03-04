# mpcs51200-project

To create and activate a virtual environment, run:
`python3 -m venv venv`
`source venv/bin/activate`

To download simple-term-menu in your environment, subsequently run:
`python3 -m pip install simple-term-menu`

Source: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

To run the app, run `python3 run_app.py`.

To run the app with our new and improved menu, run `python3 new_menu.py`.

To run tests, run `python3 -m unittest test.name_of_test_file`. For example, `python3 -m unittest test.test_games`. WARNING: Tests will delete the existing data in the databse in order to run tests which change the database.

See database/users.csv for possible users

This is a tournament management software with some features.
The files in database folder are to create two databases(.db) users.db and tournaments.db with multiple types of users like tournament manager, team manager, players and fans.
The separate functions are to take care of constraints, restrictions and to maintain order.
The files in folder backend are to check credentials(login module) and all tournaments currently in the system the teams and their players consolidated in the whole tournament database.
For Overview and Test plan
Software overview document
https://docs.google.com/document/d/1cmgMgVhJZOBizUwlZu8SHdac8o_1bjD4UsPneVKgX2s/edit?usp=sharing
Test plan
https://docs.google.com/document/d/18z4PDKVLoEohVIr65bYUGaajkL4EJprCRa3VwB6VqD8/edit?usp=sharing
