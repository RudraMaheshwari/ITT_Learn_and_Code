def is_too_low(guess, target_number):
    """ Checks if the guess is too low """
    return guess < target_number

def is_too_high(guess, target_number):
    """ Checks if the guess is too high """
    return guess > target_number

def is_correct_guess(guess, target_number):
    """ Checks if the guess is correct """
    return guess == target_number
