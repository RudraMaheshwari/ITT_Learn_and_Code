from data_processing_system.domain.processing_statistics import ProcessingStatistics

class StatisticsCalculator:

    def calculate(self, records):
        total_value = sum(record.value for record in records)
        record_count = len(records)
        average_value = int(total_value / record_count) if record_count > 0 else 0

        return ProcessingStatistics(
            total_records=record_count,
            total_value=int(total_value),
            average_value=average_value
        )
