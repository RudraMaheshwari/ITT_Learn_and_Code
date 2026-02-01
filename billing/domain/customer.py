from billing.domain.wallet import Wallet

class Customer:
    """Customer class"""
    
    def __init__(self, first_name: str, last_name: str, wallet: Wallet):
        """Initialize the customer"""
        self._first_name = first_name
        self._last_name = last_name
        self._wallet = wallet

    def get_first_name(self) -> str:
        """Get the first name of the customer"""
        return self._first_name

    def get_last_name(self) -> str:
        """Get the last name of the customer"""
        return self._last_name

    def pay(self, amount: float) -> bool:
        """Pay the amount"""
        return self._wallet.try_debit(amount)
