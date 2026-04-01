from src.config.constants import CURRENCY_SYMBOL, AMOUNT_DISPLAY_FORMAT

class Account:

    def __init__(self, account_id: str, balance: float):
        self.account_id = account_id
        self._balance = balance

    def has_sufficient_funds(self, amount: float) -> bool:
        return self._balance >= amount

    def deduct(self, amount: float) -> None:
        self._balance -= amount

    def current_balance(self) -> float:
        return self._balance

    def formatted_balance(self) -> str:
        return f"{CURRENCY_SYMBOL}{format(self._balance, AMOUNT_DISPLAY_FORMAT)}"

