class ProcessorConfig:

    def __init__(self,
                    validate=True,
                    transform=True,
                    date_format="%Y-%m-%d",
                    batch_size=100):
        self.validate = validate
        self.transform = transform
        self.date_format = date_format
        self.batch_size = batch_size
