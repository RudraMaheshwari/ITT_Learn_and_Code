from datetime import datetime
from data_processing_system.config.constants import DEFAULT_LOG_FILE_PATH, LOG_TIMESTAMP_FORMAT

class Logger:
    """Simple file logger for processing events."""

    def __init__(self, log_file_path=DEFAULT_LOG_FILE_PATH):
        self._log_file_path = log_file_path
        self._buffer = []

    def log(self, message):
        timestamp = datetime.now().strftime(LOG_TIMESTAMP_FORMAT)
        self._buffer.append(f"[{timestamp}] {message}")

    def flush(self):
        with open(self._log_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self._buffer))
        self._buffer.clear()
