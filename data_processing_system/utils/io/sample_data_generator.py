import random
from datetime import datetime, timedelta

MIN_VALUE = 10
MAX_VALUE = 1000
MAX_DATE_OFFSET_DAYS = 365

class SampleDataGenerator:

    def generate(self, file_path, record_count):
        with open(file_path, "w", encoding="utf-8") as output_file:
            for index in range(1, record_count + 1):
                record_id = f"ID{index:04d}"
                name = f"Item{index}"
                value = random.randint(MIN_VALUE, MAX_VALUE)
                date = datetime.now() - timedelta(
                    days=random.randint(0, MAX_DATE_OFFSET_DAYS)
                )

                output_file.write(
                    f"{record_id},{name},{value},{date.strftime('%Y-%m-%d')}\n"
                )
