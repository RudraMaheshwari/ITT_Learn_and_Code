class ValueFilter:

    def filter_min(self, records, min_value):
        return [record for record in records if record.value >= min_value]
