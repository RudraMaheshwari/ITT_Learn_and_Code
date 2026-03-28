from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class PaymentRequest:
    """Represents a payment request."""
    customer_id: str
    amount: Decimal

@dataclass
class PaymentResult:
    """Represents the result of a payment operation."""
    success: bool
    message: str
    transaction_id: Optional[str]

@dataclass
class PaymentRecord:
    """Represents a record of a completed payment."""
    customer_id: str
    amount: Decimal
    timestamp: datetime
