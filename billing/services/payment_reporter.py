from abc import ABC, abstractmethod

class PaymentReporter(ABC):
    """Interface for reporting payment results."""

    @abstractmethod
    def report_success(self) -> None:
        pass

    @abstractmethod
    def report_insufficient_funds(self) -> None:
        pass

class ConsolePaymentReporter(PaymentReporter):
    """Reports payment results to console."""

    def report_success(self) -> None:
        print("Payment collected successfully")

    def report_insufficient_funds(self) -> None:
        print("Customer does not have enough money")
