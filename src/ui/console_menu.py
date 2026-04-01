from src.controllers.atm_controller import AtmController
from src.models.account import Account
from src.models.device import Device
from src.config.constants import (
    MENU_WITHDRAW,
    MENU_CHECK_BALANCE,
    MENU_EXIT,
    MENU_LABEL_WITHDRAW,
    MENU_LABEL_CHECK_BALANCE,
    MENU_LABEL_EXIT,
    APP_TITLE,
    PROMPT_ENTER_CHOICE,
    PROMPT_AMOUNT,
    MSG_GOODBYE,
    LABEL_ACCOUNT,
    LABEL_BALANCE,
    DEVICE_ID_PRIMARY,
    DEVICE_STATUS_ACTIVE,
    WIFI_STATUS_CONNECTED,
    DEMO_ACCOUNT_ID,
    DEMO_INITIAL_BALANCE,
)

class ConsoleMenu:

    def __init__(self):
        self.controller = AtmController()
        self.device = Device(DEVICE_ID_PRIMARY, DEVICE_STATUS_ACTIVE, WIFI_STATUS_CONNECTED)
        self.account = Account(DEMO_ACCOUNT_ID, DEMO_INITIAL_BALANCE)

    def start(self) -> None:
        print(APP_TITLE)
        is_running = True
        while is_running:
            self.display_menu()
            choice = self.read_menu_choice()
            is_running = self.handle_choice(choice)

    def display_menu(self) -> None:
        print(f"\n{MENU_WITHDRAW}. {MENU_LABEL_WITHDRAW}")
        print(f"{MENU_CHECK_BALANCE}. {MENU_LABEL_CHECK_BALANCE}")
        print(f"{MENU_EXIT}. {MENU_LABEL_EXIT}")

    def read_menu_choice(self) -> int:
        raw_input = input(PROMPT_ENTER_CHOICE)
        return int(raw_input)

    def handle_choice(self, choice: int) -> bool:
        if choice == MENU_WITHDRAW:
            self.perform_withdrawal()
        elif choice == MENU_CHECK_BALANCE:
            self.display_balance()
        elif choice == MENU_EXIT:
            self.exit_application()
            return False
        return True

    def perform_withdrawal(self) -> None:
        raw_amount = input(PROMPT_AMOUNT)
        amount = float(raw_amount)
        self.controller.withdraw(self.device, self.account, amount)

    def display_balance(self) -> None:
        print(f"{LABEL_ACCOUNT}: {self.account.account_id}")
        print(f"{LABEL_BALANCE}: {self.account.formatted_balance()}")

    def exit_application(self) -> None:
        print(MSG_GOODBYE)

