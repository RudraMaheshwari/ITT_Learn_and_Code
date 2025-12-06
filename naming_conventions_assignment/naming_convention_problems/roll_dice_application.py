import random

def roll_dice(max_value):
    result = random.randint(1, max_value)
    return result

def roll_dice_application():
    dice_sides = 6
    dice_rolled = True

    while dice_rolled:
        user_input = input("Ready to roll the dice? Enter Q to Quit: ")

        if user_input.lower() != "q":
            rolled_value = roll_dice(dice_sides)
            print("You have rolled a", rolled_value)
        else:
            dice_rolled = False

roll_dice_application()
