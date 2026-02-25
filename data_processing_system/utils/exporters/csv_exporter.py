from data_processing_system.utils.exporters.exporter import Exporter
from data_processing_system.config.constants import CSV_HEADER

class CsvExporter(Exporter):

    def export(self, records, file_path):
        with open(file_path, "w", encoding="utf-8") as output_file:
            output_file.write(CSV_HEADER + "\n")

            for record in records:
                output_file.write(record.to_csv_row() + "\n")
