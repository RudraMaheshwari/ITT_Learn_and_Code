from data_processing_system.config import ProcessorConfig
from data_processing_system.config.constants import (
    DEFAULT_RECORD_COUNT,
    DEFAULT_INPUT_FILE,
    DEFAULT_OUTPUT_JSON,
    DEFAULT_OUTPUT_XML,
    DEFAULT_OUTPUT_CSV,
    DISPLAY_DATE_FORMAT,
    FILTER_MIN_VALUE,
)
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
        date_format=DISPLAY_DATE_FORMAT,
        batch_size=DEFAULT_RECORD_COUNT
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
    print(f"Filtered records (value >= {FILTER_MIN_VALUE}): {len(filtered_records)}")

def main():
    SampleDataGenerator().generate(DEFAULT_INPUT_FILE, DEFAULT_RECORD_COUNT)

    config = create_processing_config()
    service = build_processing_service(config)

    records, statistics = service.process(
        input_file=DEFAULT_INPUT_FILE,
        output_file=DEFAULT_OUTPUT_JSON
    )

    XmlExporter().export(records, DEFAULT_OUTPUT_XML)
    CsvExporter().export(records, DEFAULT_OUTPUT_CSV)

    filtered_records = ValueFilter().filter_min(records, FILTER_MIN_VALUE)

    display_results(statistics, filtered_records)

if __name__ == "__main__":
    main()
