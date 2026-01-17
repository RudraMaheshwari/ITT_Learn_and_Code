DISCOUNT_RATE = 0.10
TAX_RATE = 0.18
INVALID_ORDER_THRESHOLD = 0

def place_order(order_id, order_amount):
    """ Places the order """
    if is_order_invalid(order_id):
        show_invalid_order_message()
        return

    final_amount = calculate_final_amount(order_amount)
    save_order(order_id, final_amount)
    show_order_success_message()

def calculate_final_amount(order_amount):
    """ Calculates the final amount """
    discount = calculate_discount(order_amount)
    tax = calculate_tax(order_amount)
    return (order_amount + tax) - discount

def calculate_discount(order_amount):
    """ Calculates the discount """
    return order_amount * DISCOUNT_RATE

def calculate_tax(amount):
    """ Calculates the tax """
    return amount * TAX_RATE

def is_order_invalid(order_id):
    """ Checks if the order is invalid """
    return order_id <= INVALID_ORDER_THRESHOLD

def show_invalid_order_message():
    """ Shows the invalid order message """
    print("Order cannot be empty")

def show_order_success_message():
    """ Shows the order success message """
    print("Order placed successfully")

def save_order(order_id, amount):
    """ Saves the order """
    print("Order saved in database")
