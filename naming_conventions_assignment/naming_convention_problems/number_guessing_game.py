import random

def check_valid_guess(user_input):
    if user_input.isdigit() and 1 <= int(user_input) <= 100:
        return True
    else:
        return False

def number_guessing_game():
    secret_number = random.randint(1,100)
    guessed_number = False
    guess = input("Guess a number between 1 and 100:")
    number_of_guesses = 0

    while not guessed_number:
        if not check_valid_guess(guess):
            guess = input("I won't count this one. Please enter a number between 1 to 100")
            continue
        else:
            number_of_guesses += 1
            guess = int(guess)

        if guess < secret_number:
            guess = input("Too low. Guess again")
        elif guess > secret_number:
            guess = input("Too High. Guess again")
        else:
            print("You guessed it in", number_of_guesses, "guesses!")
            guessed_number = True

number_guessing_game()
