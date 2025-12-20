import random

def is_valid_guess(user_input):
    return user_input.isdigit() and 1 <= int(user_input) <= 100

def get_valid_guess():
    guess = input("Guess a number between 1 and 100:")
    while not is_valid_guess(guess):
        guess = input("I wont count this one Please enter a number between 1 to 100:")
    return int(guess)

def play_number_guessing_game():
    target_number = random.randint(1, 100)
    guess_count = 0
    while True:
        guess = get_valid_guess()
        guess_count += 1
        if guess < target_number:
            print("Too low. Guess again")
        elif guess > target_number:
            print("Too High. Guess again")
        else:
            print("You guessed it in", guess_count, "guesses!")
            break

play_number_guessing_game()
