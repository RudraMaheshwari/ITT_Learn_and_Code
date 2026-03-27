from data_processing_system.config.constants import (
    DEFAULT_VALIDATE,
    DEFAULT_TRANSFORM,
    DEFAULT_DATE_FORMAT,
    DEFAULT_BATCH_SIZE,
)

class ProcessorConfig:

    def __init__(self,
                    validate=DEFAULT_VALIDATE,
                    transform=DEFAULT_TRANSFORM,
                    date_format=DEFAULT_DATE_FORMAT,
                    batch_size=DEFAULT_BATCH_SIZE):
        self.validate = validate
        self.transform = transform
        self.date_format = date_format
        self.batch_size = batch_size
