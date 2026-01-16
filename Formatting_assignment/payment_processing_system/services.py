class Logger:
    """Logging service."""
    
    def log(self, message: str) -> None:
        """Log a message."""
        print(message)

class NotificationService:
    """Notification service for sending messages to customers."""
    
    def send(self, customer_id: str, message: str) -> None:
        """Send a notification to a customer."""
        print(f"Notify {customer_id}: {message}")
