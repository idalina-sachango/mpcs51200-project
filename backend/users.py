from database.user_database import get_current_users

# Logs the user in by returning the type of the user that was logged in
# or None if the log in failed
def log_in(username: str, password: str) -> str:
    users = get_current_users()

    if username in users:
        user_data = users[username]
        if user_data["password"] == password:
            return user_data["user_type"]
    else:
        return None
