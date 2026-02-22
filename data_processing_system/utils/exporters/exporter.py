from abc import ABC, abstractmethod

class Exporter(ABC):
    """Exporter interface."""

    @abstractmethod
    def export(self, records, file_path):
        pass
