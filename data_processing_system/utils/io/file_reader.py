class FileReader:
    """Reads text files."""

    def read_lines(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
