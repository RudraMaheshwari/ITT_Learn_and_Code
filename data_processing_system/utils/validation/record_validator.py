class RecordValidator:
    """Validates records."""

    def is_valid(self, record):
        if not record.record_id:
            return False
        if not record.name:
            return False
        if record.value is None:
            return False
        return True
