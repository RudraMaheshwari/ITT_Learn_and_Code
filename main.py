from billing.workflows.collect_payment import collect_payment

def get_initial_balance() -> float:
    """Prompt the user for the initial wallet balance."""
    while True:
        try:
            user_input = input("Enter the starting wallet balance for the customer: ")
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a numerical value for the balance.")

if __name__ == "__main__":
    balance = get_initial_balance()
    collect_payment(initial_balance=balance)
