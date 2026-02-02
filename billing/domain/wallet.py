class Wallet:
    """Wallet class"""
    
    def __init__(self, balance: float):
        """Initialize the wallet"""
        self._balance = balance

    def get_total_money(self) -> float:
        """Get the total money in the wallet"""
        return self._balance

    def reset_balance(self, new_value: float) -> None:
        """Reset the balance of the wallet"""
        self._balance = new_value

    def try_debit(self, amount: float) -> bool:
        """Try to debit the wallet"""
        if self._balance >= amount:
            self._balance -= amount
            return True
        return False
