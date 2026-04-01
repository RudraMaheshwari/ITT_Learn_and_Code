from src.config.constants import (
    EXPENSE_FILE_PATH,
    FILE_MODE_READ_APPEND,
    FILE_MODE_APPEND,
    FILE_MODE_WRITE,
    NEWLINE,
)

class FileHandler:

    def read_lines(self) -> list:
        file = open(EXPENSE_FILE_PATH, FILE_MODE_READ_APPEND)
        try:
            file.seek(0)
            lines = file.readlines()
        finally:
            file.close()
        return lines

    def append_line(self, line: str) -> None:
        file = open(EXPENSE_FILE_PATH, FILE_MODE_APPEND)
        try:
            file.write(line + NEWLINE)
        finally:
            file.close()

    def clear_contents(self) -> None:
        file = open(EXPENSE_FILE_PATH, FILE_MODE_WRITE)
        try:
            file.write("")
        finally:
            file.close()

