def is_valid_guess(user_input):
    """ Checks if the user input is a valid guess """
    return user_input.isdigit() and 1 <= int(user_input) <= 100
