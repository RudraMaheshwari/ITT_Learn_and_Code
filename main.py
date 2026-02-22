from data_processing_system.config import ProcessorConfig
from data_processing_system.utils.io import FileReader, SampleDataGenerator
from data_processing_system.utils.parsing import RecordParser
from data_processing_system.utils.validation import RecordValidator
from data_processing_system.core.transformation import RecordTransformer
from data_processing_system.statistics import StatisticsCalculator
from data_processing_system.utils.exporters import JsonExporter, XmlExporter, CsvExporter
from data_processing_system.utils.filtering import ValueFilter
from data_processing_system.core.services import DataProcessingService

def create_processing_config():
    return ProcessorConfig(
        validate=True,
        transform=True,
        date_format="%m/%d/%Y",
        batch_size=50
    )

def build_processing_service(config):
    return DataProcessingService(
        reader=FileReader(),
        parser=RecordParser(),
        validator=RecordValidator(),
        transformer=RecordTransformer(),
        statistics_calculator=StatisticsCalculator(),
        exporter=JsonExporter(),
        config=config
    )

def display_results(statistics, filtered_records):
    print("Processing complete")
    print(f"Statistics: {statistics}")
    print("Exported to JSON, XML, and CSV")
    print(f"Filtered records (value >= 100): {len(filtered_records)}")

def main():
    SampleDataGenerator().generate("input.csv", 50)

    config = create_processing_config()
    service = build_processing_service(config)

    records, statistics = service.process(
        input_file="input.csv",
        output_file="output.json"
    )

    XmlExporter().export(records, "output.xml")
    CsvExporter().export(records, "output.csv")

    filtered_records = ValueFilter().filter_min(records, 100)

    display_results(statistics, filtered_records)

if __name__ == "__main__":
    main()
