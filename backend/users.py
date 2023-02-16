from database.user_database import get_all_users, get_user_by_id

# Logs the user in by returning the type and id of the user that was logged in
# or None if the log in failed
def log_in(username: str, password: str) -> str:
    users = get_all_users()

    if username in users:
        user_data = users[username]
        if user_data["password"] == password:
            return user_data["user_id"], user_data["user_type"]
    else:
        return None

# Takes in a user dict, such as from the get_user_by_id function
# As an example:
# {
#     'user_id': 2, 
#     'name': 'Coach Coach', 
#     'username': 'originalcoach', 
#     'password': 'password', 
#     'user_type': 'TeamManager'
# }
def print_user(user: dict):
    print(f"Name: {user['name']}")
    print(f"Username: {user['username']}")
    print(f"User Type: {user['user_type']}")

# Example test cases for log_in function:
# # Should be TournamentManager
# print(log_in("tm123", "password"))
# # Should be None
# print(log_in("tm123", "wrongpassword"))
# # Should be None
# print(log_in("tm1234", "password"))
# # Should be Other
# print(log_in("soccerfan01", "password"))