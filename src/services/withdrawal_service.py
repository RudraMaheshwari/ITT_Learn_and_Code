from src.models.account import Account
from src.models.device import Device
from src.core.exceptions import (
    DeviceLockedException,
    NetworkConnectionException,
    InsufficientFundsException,
)

class WithdrawalService:

    def process_withdrawal(self, device: Device, account: Account, amount: float) -> None:
        self.validate_device_is_active(device)
        self.validate_network_connection(device)
        self.validate_sufficient_funds(account, amount)
        self.dispense_cash(account, amount)

    def validate_device_is_active(self, device: Device) -> None:
        if not device.is_active():
            raise DeviceLockedException()

    def validate_network_connection(self, device: Device) -> None:
        if not device.is_connected():
            raise NetworkConnectionException()

    def validate_sufficient_funds(self, account: Account, amount: float) -> None:
        if not account.has_sufficient_funds(amount):
            raise InsufficientFundsException()

    def dispense_cash(self, account: Account, amount: float) -> None:
        account.deduct(amount)

