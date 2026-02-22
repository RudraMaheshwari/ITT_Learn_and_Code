class ProcessingStatistics:
    """Holds processing statistics as a domain object."""

    def __init__(self, total_records, total_value, average_value, error_count=0):
        self.total_records = total_records
        self.total_value = total_value
        self.average_value = average_value
        self.error_count = error_count

    def __repr__(self):
        return (
            f"ProcessingStatistics("
            f"total_records={self.total_records}, "
            f"total_value={self.total_value}, "
            f"average_value={self.average_value}, "
            f"error_count={self.error_count})"
        )
