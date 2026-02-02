from billing.domain.wallet import Wallet
from billing.domain.customer import Customer
from billing.services.paperboy_collector import PaperboyCollector

NEWSPAPER_SUBSCRIPTION_FEE = 25.0

class PaymentWorkflow:
    """Orchestrates the payment collection workflow"""

    def __init__(self, customer: Customer, collector: PaperboyCollector):
        """Initialize with dependencies"""
        self._customer = customer
        self._collector = collector
    
    def execute(self) -> None:
        """Execute the payment collection workflow"""
        if self._process_payment():
            self._report_success()
        else:
            self._report_insufficient_funds()

    def _process_payment(self) -> bool:
        """Process payment collection from customer"""
        return self._collector.collect_payment(self._customer, NEWSPAPER_SUBSCRIPTION_FEE)

    def _report_success(self) -> None:
        """Report successful payment"""
        print("Payment collected successfully")

    def _report_insufficient_funds(self) -> None:
        """Report insufficient funds"""
        print("Customer does not have enough money")

def collect_payment(initial_balance: float):
    """Entry point for payment collection"""
    wallet = Wallet(balance=initial_balance)
    customer = Customer(first_name="John", last_name="Doe", wallet=wallet)
    collector = PaperboyCollector()
    
    workflow = PaymentWorkflow(customer=customer, collector=collector)
    workflow.execute()
