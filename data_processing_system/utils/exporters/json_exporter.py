import json
from data_processing_system.utils.exporters.exporter import Exporter

class JsonExporter(Exporter):

    def export(self, records, file_path):
        data = [record.to_dict() for record in records]

        with open(file_path, "w", encoding="utf-8") as output_file:
            json.dump(data, output_file, indent=2)
