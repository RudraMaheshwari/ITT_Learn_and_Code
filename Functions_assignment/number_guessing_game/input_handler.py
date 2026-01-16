def read_initial_guess():
    """ Reads the first guess from the user """
    return input("Guess a number between 1 and 100:").strip()

def read_retry_guess():
    """ Reads the retry guess from the user """
    return input("I won't count this one, please enter a number between 1 to 100:").strip()

def read_guess():
    """ Reads the guess from the user """
    return input().strip()
