import random
from input_handler import read_initial_guess, read_retry_guess
from validation import is_valid_guess, MIN_GUESS, MAX_GUESS
from game_rules import is_too_low, is_too_high, is_correct_guess

INITIAL_GUESS_COUNT = 0

def get_valid_guess():
    """Gets a valid guess from the user."""
    user_input = read_initial_guess()

    while not is_valid_guess(user_input):
        user_input = read_retry_guess()

    return int(user_input)

def provide_hint(guess, target_number):
    """Provides a hint based on the guess."""
    if is_too_low(guess, target_number):
        print("Too low. Guess again")
        
    elif is_too_high(guess, target_number):
        print("Too high. Guess again")

def play_number_guessing_game():
    """Plays the number guessing game."""
    target_number = random.randint(MIN_GUESS, MAX_GUESS)
    guess_count = INITIAL_GUESS_COUNT

    while True:
        guess = get_valid_guess()
        guess_count += 1

        if is_correct_guess(guess, target_number):
            print("You guessed it in", guess_count, "guesses!")
            break

        provide_hint(guess, target_number)

if __name__ == "__main__":
    play_number_guessing_game()
