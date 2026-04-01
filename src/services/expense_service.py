from src.models.expense import Expense
from src.storage.file_handler import FileHandler
from src.config.constants import (
    FIELD_SEPARATOR,
    EXPECTED_FIELD_COUNT,
    DESCRIPTION_INDEX,
    AMOUNT_INDEX,
    INITIAL_TOTAL,
)

class ExpenseService:

    def __init__(self):
        self.file_handler = FileHandler()

    def add_expense(self, description: str, amount: float) -> None:
        expense = Expense(description, amount)
        self.file_handler.append_line(expense.format_for_storage())

    def fetch_all_expenses(self) -> list:
        lines = self.file_handler.read_lines()
        expenses = []
        for line in lines:
            expense = self.parse_line(line.strip())
            if expense:
                expenses.append(expense)
        return expenses

    def parse_line(self, line: str):
        if not line:
            return None
        parts = line.split(FIELD_SEPARATOR)
        if len(parts) != EXPECTED_FIELD_COUNT:
            return None
        description = parts[DESCRIPTION_INDEX]
        amount = float(parts[AMOUNT_INDEX])
        return Expense(description, amount)

    def calculate_total(self, expenses: list) -> float:
        total = INITIAL_TOTAL
        for expense in expenses:
            total += expense.amount
        return total

    def clear_all_expenses(self) -> None:
        self.file_handler.clear_contents()

