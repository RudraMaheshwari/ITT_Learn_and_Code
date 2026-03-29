from billing.domain.customer import Customer

class PaperboyCollector:
    """PaperboyCollector class"""
    
    def collect_payment(self, customer: Customer, amount: float) -> bool:
        """Collect payment from the customer"""
        return customer.pay(amount)
