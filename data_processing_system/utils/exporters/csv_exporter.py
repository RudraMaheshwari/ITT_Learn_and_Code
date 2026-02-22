from data_processing_system.utils.exporters.exporter import Exporter

class CsvExporter(Exporter):

    def export(self, records, file_path):
        with open(file_path, "w", encoding="utf-8") as output_file:
            output_file.write("ID,NAME,VALUE,DATE,DOUBLED_VALUE,SQUARED_VALUE\n")

            for record in records:
                output_file.write(record.to_csv_row() + "\n")
