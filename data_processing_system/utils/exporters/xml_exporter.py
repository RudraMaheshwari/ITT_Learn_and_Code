from data_processing_system.utils.exporters.exporter import Exporter

class XmlExporter(Exporter):

    def export(self, records, file_path):
        with open(file_path, "w", encoding="utf-8") as output_file:
            output_file.write("<records>\n")

            for record in records:
                output_file.write("  <record>\n")
                for field_name, field_value in record.to_dict().items():
                    output_file.write(
                        f"    <{field_name}>{field_value}</{field_name}>\n"
                    )
                output_file.write("  </record>\n")

            output_file.write("</records>")
