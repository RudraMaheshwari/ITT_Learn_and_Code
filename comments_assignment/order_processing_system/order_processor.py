from services import PaymentGatewayService, InventoryService, NotificationService
from repositories import OrderRepository

class OrderProcessor:
    """ Order processor """

    def __init__(self):
        """ Initializes the order processor """
        self.payment_gateway = PaymentGatewayService()
        self.inventory_service = InventoryService()
        self.notification_service = NotificationService()
        self.order_repository = OrderRepository()

    async def place_order(self, order):
        """ Places the order """
        self._validate_order(order)

        if not await self.inventory_service.check_availability(order["items"]):
            return self._order_failed("Insufficient inventory")

        await self.inventory_service.reserve_items(order["items"])

        try:
            payment_result = await self._process_payment(order)

            if payment_result["success"]:
                await self._finalize_order(order, payment_result["transaction_id"])
                return self._order_success(payment_result["transaction_id"])

            await self.inventory_service.release_reservation(order["items"])
            return self._order_failed("Payment failed")

        except Exception:
            await self.inventory_service.release_reservation(order["items"])
            raise

    async def cancel_order(self, order_id):
        """ Cancels the order """
        order = await self.order_repository.get_order_by_id(order_id)

        if order["status"] == "PAID":
            await self.payment_gateway.refund_payment(order["transaction_id"])
            await self.inventory_service.restore_inventory(order["items"])

        order["status"] = "CANCELLED"
        await self.order_repository.save_order(order)

    def _validate_order(self, order):
        """ Validates the order """
        if not order or not order.get("items") or order.get("total_amount", 0) <= 0:
            raise ValueError("Invalid order")

    async def _process_payment(self, order):
        """ Processes the payment """
        return await self.payment_gateway.process_payment(
            order["customer_id"],
            order["total_amount"],
            order["payment_method"]
        )

    async def _finalize_order(self, order, transaction_id):
        """ Finalizes the order """
        await self.inventory_service.commit_reservation(order["items"])
        await self.notification_service.send_order_confirmation(order)
        order["transaction_id"] = transaction_id

    def _order_success(self, transaction_id):
        """ Returns the order success message """
        return {"status": "SUCCESS", "transaction_id": transaction_id}

    def _order_failed(self, message):
        """ Returns the order failed message """
        return {"status": "FAILED", "message": message}
