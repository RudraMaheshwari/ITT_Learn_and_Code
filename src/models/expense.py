from src.config.constants import FIELD_SEPARATOR, CURRENCY_SYMBOL, AMOUNT_DISPLAY_FORMAT

class Expense:

    def __init__(self, description: str, amount: float):
        self.description = description
        self.amount = amount

    def format_for_display(self) -> str:
        formatted_amount = format(self.amount, AMOUNT_DISPLAY_FORMAT)
        return f"{self.description}: {CURRENCY_SYMBOL}{formatted_amount}"

    def format_for_storage(self) -> str:
        return f"{self.description}{FIELD_SEPARATOR}{self.amount}"

