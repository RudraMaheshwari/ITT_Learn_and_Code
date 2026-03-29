class Wallet:
    """Encapsulates balance and exposes behavior, not data."""
    
    def __init__(self, balance: float):
        """Initialize the wallet with a starting balance."""
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._balance = balance

    @property
    def total_money(self) -> float:
        """Return the current balance (for display/logging only)."""
        return self._balance

    def credit(self, amount: float) -> None:
        """Add a positive amount to the wallet."""
        if amount <= 0:
            raise ValueError("Credit amount must be positive")
        self._balance += amount

    def try_debit(self, amount: float) -> bool:
        """Attempt to debit the wallet; returns True if successful."""
        if amount <= 0:
            return False
        if self._balance >= amount:
            self._balance -= amount
            return True
        return False
