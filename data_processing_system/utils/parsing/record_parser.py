from data_processing_system.domain.record import Record

MINIMUM_FIELD_COUNT = 3

class RecordParser:

    def parse(self, lines):
        records = []

        for line in lines:
            parts = [part.strip() for part in line.split(",")]

            if len(parts) < MINIMUM_FIELD_COUNT:
                continue

            record = Record(
                record_id=parts[0],
                name=parts[1],
                value=float(parts[2]),
                date=parts[3] if len(parts) > MINIMUM_FIELD_COUNT else None
            )

            records.append(record)

        return records
