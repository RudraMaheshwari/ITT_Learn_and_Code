class DataProcessingService:

    def __init__(self,
                    reader,
                    parser,
                    validator,
                    transformer,
                    statistics_calculator,
                    exporter,
                    config):
        self.reader = reader
        self.parser = parser
        self.validator = validator
        self.transformer = transformer
        self.statistics_calculator = statistics_calculator
        self.exporter = exporter
        self.config = config

    def process(self, input_file, output_file):
        lines = self.reader.read_lines(input_file)
        records = self.parser.parse(lines)

        if self.config.validate:
            records = [record for record in records
                        if self.validator.is_valid(record)]

        if self.config.transform:
            records = self.transformer.transform(
                records,
                self.config.date_format
            )

        statistics = self.statistics_calculator.calculate(records)

        self.exporter.export(records, output_file)

        return records, statistics
