MIN_GUESS = 1
MAX_GUESS = 100

def is_valid_guess(user_input):
    """ Checks if the user input is a valid guess """
    return user_input.isdigit() and MIN_GUESS <= int(user_input) <= MAX_GUESS
