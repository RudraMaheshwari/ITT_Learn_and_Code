class PaymentException(Exception):
    """Exception raised when a payment operation fails."""
    
    def __init__(self, message: str = "Payment processing failed"):
        """Initialize the PaymentException with a message."""
        self.message = message
        super().__init__(self.message)
