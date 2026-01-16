from infrastructure import db, write_to_file

def is_valid_user(user):
    """Checks if the user is valid."""
    return user.name != "" and user.email != ""

def save_user_to_database(user):
    """Saves the user to the database."""
    db.insert("Users", user)

def backup_user_to_file(user):
    """Backups the user to a file."""
    file_path = f"/backup/users/{user.id}.txt"
    write_to_file(file_path, user)

def save_user(user):
    """Saves the user to the database and backups to a file."""
    if not is_valid_user(user):
        print("Invalid user data")
        return

    save_user_to_database(user)
    backup_user_to_file(user)
