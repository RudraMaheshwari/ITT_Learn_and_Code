class FileWriter:
    """Writes lines to a text file."""

    def write_lines(self, file_path, lines):
        with open(file_path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
