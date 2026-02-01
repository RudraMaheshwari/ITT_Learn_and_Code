from billing.domain.wallet import Wallet
from billing.domain.customer import Customer
from billing.services.paperboy_collector import PaperboyCollector

INITIAL_WALLET_BALANCE = 100.0
NEWSPAPER_SUBSCRIPTION_FEE = 25.0

class PaymentWorkflow:
    """Orchestrates the payment collection workflow"""
    
    def _create_customer(self) -> Customer:
        """Create a customer with a wallet"""
        wallet = Wallet(balance=INITIAL_WALLET_BALANCE)
        return Customer("John", "Doe", wallet)

    def _process_payment(self, customer: Customer) -> bool:
        """Process payment collection from customer"""
        collector = PaperboyCollector()
        return collector.collect_payment(customer, NEWSPAPER_SUBSCRIPTION_FEE)

    def _report_payment_result(self, payment_successful: bool) -> None:
        """Report the payment result"""
        if payment_successful:
            print("Payment collected successfully")
        else:
            print("Customer does not have enough money")

    def execute(self) -> None:
        """Execute the payment collection workflow"""
        customer = self._create_customer()
        payment_successful = self._process_payment(customer)
        self._report_payment_result(payment_successful)

def collect_payment():
    """Entry point for payment collection"""
    workflow = PaymentWorkflow()
    workflow.execute()
