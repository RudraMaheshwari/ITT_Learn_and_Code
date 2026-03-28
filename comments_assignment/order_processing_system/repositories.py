class OrderRepository:
    """ Order repository """
    
    async def get_order_by_id(self, order_id):
        """ Gets the order by id """
        return {
            "id": order_id,
            "status": "PAID",
            "transaction_id": "TXN123",
            "items": []
        }

    async def save_order(self, order):
        """ Saves the order """
        pass
