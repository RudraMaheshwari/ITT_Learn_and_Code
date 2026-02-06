from billing.domain.wallet import Wallet
from billing.domain.customer import Customer
from billing.services.paperboy_collector import PaperboyCollector
from billing.services.payment_reporter import PaymentReporter, ConsolePaymentReporter

NEWSPAPER_MONTHLY_SUBSCRIPTION_FEE = 25.0

class PaymentWorkflow:
    def __init__(
        self,
        customer: Customer,
        collector: PaperboyCollector,
        reporter: PaymentReporter
    ):
        self._customer = customer
        self._collector = collector
        self._reporter = reporter

    def execute(self) -> None:
        if self._process_payment():
            self._reporter.report_success()
        else:
            self._reporter.report_insufficient_funds()

    def _process_payment(self) -> bool:
        return self._collector.collect_payment(
            self._customer,
            NEWSPAPER_MONTHLY_SUBSCRIPTION_FEE
        )

def start_payment_flow(initial_balance: float) -> None:
    wallet = Wallet(balance=initial_balance)
    customer = Customer("John", "Doe", wallet)
    collector = PaperboyCollector()
    reporter = ConsolePaymentReporter()

    workflow = PaymentWorkflow(customer, collector, reporter)
    workflow.execute()
