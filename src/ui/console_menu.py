from src.services.expense_service import ExpenseService
from src.config.constants import (
    MENU_ADD_EXPENSE,
    MENU_VIEW_EXPENSES,
    MENU_CLEAR_EXPENSES,
    MENU_EXIT,
    APP_TITLE,
    DIVIDER,
    CURRENCY_SYMBOL,
    AMOUNT_DISPLAY_FORMAT,
    PROMPT_ENTER_CHOICE,
    PROMPT_DESCRIPTION,
    PROMPT_AMOUNT,
    MSG_EXPENSE_SAVED,
    MSG_NO_EXPENSES,
    MSG_EXPENSES_CLEARED,
    MSG_GOODBYE,
    LABEL_TOTAL,
)

class ConsoleMenu:

    def __init__(self):
        self.expense_service = ExpenseService()

    def start(self) -> None:
        print(APP_TITLE)
        is_running = True
        while is_running:
            self.display_menu()
            choice = self.read_menu_choice()
            is_running = self.handle_choice(choice)

    def display_menu(self) -> None:
        print(f"\n{MENU_ADD_EXPENSE}. Add Expense")
        print(f"{MENU_VIEW_EXPENSES}. View All Expenses")
        print(f"{MENU_CLEAR_EXPENSES}. Clear All Expenses")
        print(f"{MENU_EXIT}. Exit")

    def read_menu_choice(self) -> int:
        raw_input = input(PROMPT_ENTER_CHOICE)
        return int(raw_input)

    def handle_choice(self, choice: int) -> bool:
        if choice == MENU_ADD_EXPENSE:
            self.add_expense()
        elif choice == MENU_VIEW_EXPENSES:
            self.display_all_expenses()
        elif choice == MENU_CLEAR_EXPENSES:
            self.clear_expenses()
        elif choice == MENU_EXIT:
            self.exit_application()
            return False
        return True

    def add_expense(self) -> None:
        description = input(PROMPT_DESCRIPTION)
        raw_amount = input(PROMPT_AMOUNT)
        amount = float(raw_amount)
        self.expense_service.add_expense(description, amount)
        print(MSG_EXPENSE_SAVED)

    def display_all_expenses(self) -> None:
        expenses = self.expense_service.fetch_all_expenses()
        if not expenses:
            print(MSG_NO_EXPENSES)
            return
        print(f"\n{DIVIDER}")
        for expense in expenses:
            print(expense.format_for_display())
        print(DIVIDER)
        total = self.expense_service.calculate_total(expenses)
        formatted_total = format(total, AMOUNT_DISPLAY_FORMAT)
        print(f"{LABEL_TOTAL}: {CURRENCY_SYMBOL}{formatted_total}")

    def clear_expenses(self) -> None:
        self.expense_service.clear_all_expenses()
        print(MSG_EXPENSES_CLEARED)

    def exit_application(self) -> None:
        print(MSG_GOODBYE)

