from datetime import datetime

class Record:

    def __init__(self, record_id, name, value, date=None):
        self._record_id = record_id
        self._name = name
        self._value = value
        self._date = date
        self._doubled_value = None
        self._squared_value = None

    @property
    def record_id(self):
        return self._record_id

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def date(self):
        return self._date

    @property
    def doubled_value(self):
        return self._doubled_value

    @property
    def squared_value(self):
        return self._squared_value

    def capitalize_name(self):
        self._name = self._name.upper()

    def format_date(self, date_format):
        if self._date:
            parsed_date = datetime.fromisoformat(self._date)
            self._date = parsed_date.strftime(date_format)

    def compute_derived_values(self):
        self._doubled_value = self._value * 2
        self._squared_value = self._value ** 2

    def to_dict(self):
        return {
            "record_id": self._record_id,
            "name": self._name,
            "value": self._value,
            "date": self._date,
            "doubled_value": self._doubled_value,
            "squared_value": self._squared_value
        }

    def to_csv_row(self):
        return (
            f"{self._record_id},{self._name},{self._value},"
            f"{self._date},{self._doubled_value},{self._squared_value}"
        )

    def __repr__(self):
        return (
            f"Record(record_id={self._record_id}, "
            f"name={self._name}, value={self._value})"
        )
