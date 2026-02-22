class RecordTransformer:

    def transform(self, records, date_format):
        for record in records:
            record.capitalize_name()
            record.format_date(date_format)
            record.compute_derived_values()

        return records
