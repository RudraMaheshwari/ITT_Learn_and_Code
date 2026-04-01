from src.models.account import Account
from src.models.device import Device
from src.services.withdrawal_service import WithdrawalService
from src.core.exceptions import (
    DeviceLockedException,
    NetworkConnectionException,
    InsufficientFundsException,
)
from src.config.constants import (
    MSG_WITHDRAWAL_SUCCESS,
    MSG_DEVICE_LOCKED,
    MSG_NO_CONNECTION,
    MSG_INSUFFICIENT_FUNDS,
)

class AtmController:

    def __init__(self):
        self.withdrawal_service = WithdrawalService()

    def withdraw(self, device: Device, account: Account, amount: float) -> None:
        try:
            self.withdrawal_service.process_withdrawal(device, account, amount)
            print(MSG_WITHDRAWAL_SUCCESS)
        except DeviceLockedException:
            print(MSG_DEVICE_LOCKED)
        except NetworkConnectionException:
            print(MSG_NO_CONNECTION)
        except InsufficientFundsException:
            print(MSG_INSUFFICIENT_FUNDS)
